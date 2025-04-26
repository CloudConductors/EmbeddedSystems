import boto3
from boto3.dynamodb.conditions import Attr, And
from botocore.exceptions import ClientError
from datetime import datetime
import pickle
import json
import numpy as np
from sklearn.ensemble import IsolationForest
from network import ping_aws

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
schedule_table = dynamodb.Table('cc-metropt3-schedule')

def data_cleaner(unclean_data):
    """
    Cleans the unclean data by extracting relevant fields and converting them to a numpy array.

    Parameters:
        unclean_data (str or dict): The unclean data to be cleaned. It can be a JSON string or a dictionary.

    Returns:
        np.ndarray: A numpy array containing the cleaned data.
    """

    if isinstance(unclean_data, str):
        embedded_json = json.loads(unclean_data)
    else:
        embedded_json = unclean_data

    clean_data = np.array([])
    clean_data = np.append(clean_data, embedded_json["tp2"])
    clean_data = np.append(clean_data, embedded_json["tp3"])
    clean_data = np.append(clean_data, embedded_json["h1"])
    clean_data = np.append(clean_data, embedded_json["dv_pressure"])
    clean_data = np.append(clean_data, embedded_json["resevoirs"])
    clean_data = np.append(clean_data, embedded_json["oil_temperature"])
    clean_data = np.append(clean_data, embedded_json["motor_current"])
    clean_data = np.append(clean_data, embedded_json["COMP"])
    clean_data = np.append(clean_data, embedded_json["dv_electric"])
    clean_data = np.append(clean_data, embedded_json["towers"])
    clean_data = np.append(clean_data, embedded_json["mpg"])
    clean_data = np.append(clean_data, embedded_json["lps"])
    clean_data = np.append(clean_data, embedded_json["pressure_switch"])
    clean_data = np.append(clean_data, embedded_json["oil_level"])
    clean_data = np.append(clean_data, embedded_json["caudal_impulses"])
    return clean_data

def download_model_from_s3():
    """
    Downloads the anomaly detection model from S3.
    If the model is not reachable, it will return False.

    Returns:
        clf (IsolationForest): The loaded anomaly detection model.
        bool: False if the model is not reachable.
    """
    s3_client = boto3.client('s3')
    cloud_bucket = 'cloud-conductors'
    model_filename = 'anomaly_prediction.pkl' # I'm PICKLE RICK

    if ping_aws() == False:
        print("AWS is not reachable. Trying local model...")
        return False
    
    s3_client.download_file(cloud_bucket, model_filename, model_filename)

    # Load the model locally
    with open(model_filename, 'rb') as model_file:
        clf = pickle.load(model_file)
        return clf


def anomaly_prediction(embedded_data, clf, component_id, train_id):
    """
    Predicts if the embedded data is an anomaly using the Isolation Forest model.
    Updates the DynamoDB table if an anomaly is detected.

    Parameters:
        embedded_data (str or dict): The embedded data to be predicted. It can be a JSON string or a dictionary.
        clf (IsolationForest): The trained anomaly detection model.

    Returns:
        bool: True if an anomaly is detected and the schedule is updated, False otherwise.
    """
    # Cleaning data
    cleaned_data = data_cleaner(embedded_data).reshape(1, -1)

    # Run the model
    result = clf.predict(cleaned_data)

    if result == -1:
        # Test if schedule exists
        try:
            Component_Id = schedule_table.scan(
                FilterExpression=Attr('component_id').eq(str(component_id))
            )

            Train_Id = schedule_table.scan(
                FilterExpression=Attr('train_id').eq(str(train_id))
            )
        except ClientError as e:
            print("Error scanning table:", e.response['Error']['Message'], flush=True)
            return False

        # Update Schedule
        if 'Items' in Component_Id and len(Component_Id['Items']) > 0:
            try:
                # Check if item exists before inserting (in case you're replacing it)
                existing_item = schedule_table.get_item(
                    Key={'component_id': str(component_id), 'train_id': str(train_id)},
                )
                if 'Item' not in existing_item:
                    print("Item not in schedule table.", flush=True)
                    return False

                # Grabbing current time for update
                current_time = datetime.now().strftime('%m/%d/%Y')

                # Perform put_item (replaces the existing item with new values)
                schedule_table.update_item(
                    Key={'component_id': str(component_id), 'train_id': str(train_id)},
                    UpdateExpression="SET component_failure = :val1, manually_overridden = :val2, expected_repair_date = :val3, maintenance_scheduled = :val4",
                    ExpressionAttributeValues={
                        ':val1': True,
                        ':val2': True,
                        ':val3': current_time,
                        ':val4': True,
                    },
                )
                
                print("Anomaly detected!", flush=True)
                return True
            except ClientError as e:
                print("Error updating item:", e.response['Error']['Message'], flush=True)
                return False
        else:
            print("Item not found", flush=True)
            return False
    else:
        print("No anomalies detected.", flush=True)
        return False