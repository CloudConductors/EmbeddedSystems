import boto3
from boto3.dynamodb.conditions import Attr, And
from botocore.exceptions import ClientError
from datetime import datetime
import pickle
import json
import numpy as np
from sklearn.ensemble import IsolationForest

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
schedule_table = dynamodb.Table('cc-metropt3-schedule')

def data_cleaner(unclean_data):
    if isinstance(unclean_data, str):
        embedded_json = json.loads(unclean_data)
    else:
        embedded_json = unclean_data
    clean_data = None
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

def anomaly_prediction(embedded_data):
    #Cleaning data
    cleaned_data = data_cleaner(embedded_data)

    # Load anomally_prediction model from S3
    s3_client = boto3.client('s3')
    cloud_bucket = 'cloud-conductors'
    model_filename = 'anomaly_prediction.pkl'

    s3_client.download_file(cloud_bucket, model_filename, model_filename)

    # Load the model locally
    with open(model_filename, 'rb') as model_file:
        clf = pickle.load(model_file)

    # Run the model
    result = clf.predict(cleaned_data)

    if result == True:
        # Test if schedule exists
        try:
                Component_Id = schedule_table.scan(
                    FilterExpression=Attr('component_id').eq('1')
                )
        except ClientError as e:
            return print({'error': 'ID not found'})

        # Update Schedule
        if 'Items' in Component_Id and len(Component_Id['Items']) > 0:
            try:
                if 'Items' in Component_Id and len(Component_Id['Items']) > 0:
                    Component_Id = Component_Id['Items'][0]['component_id']
                else:
                    return print({'error': 'Component ID not found'})

                # Check if item exists before inserting (in case you're replacing it)
                existing_item = schedule_table.get_item(
                    Key={'component_id': str(Component_Id)}
                )
                if 'Item' not in existing_item:
                    return print({'error': 'Item not found in table'})

                # Grabbing current time for update
                current_time = datetime.now().strftime('%m/%d/%Y')

                # Perform put_item (replaces the existing item with new values)
                maintenance = schedule_table.put_item(
                    Item={
                        'component_id': str(Component_Id),
                        'train_id': '1',
                        'component_failure' : 'true',
                        'Expected_Repair_DUF': str(current_time),
                        'Last_Repair_Date': '01/01/2001',
                        'Maintenance_Scheduled': 'true',
                        'Manually_Overriden': 'true',
                        'Mean_DUF': 3,
                        'Standard_Deviation_DUF': 12,
                        
                    }
                )
                print("Table updated successfully!")
                return print({'message': 'Anomaly detected, schedule updated'})
            except ClientError as e:
                return print({'error': 'Error putting item in table'})
        else:
            print("table wasn't changed in the database!")
    else:
        return print({'message': 'No anomaly detected'})