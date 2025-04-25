import boto3
import serial
import asyncio
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
import uuid
import datetime
import json
from anomaly import anomaly_prediction, download_model_from_s3
from network import ping_aws

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("cc-metropt3-prelearned")

def addToBatch(JSONdata):
    """
    Adds the JSON data to a batch file for later processing.

    Parameters:
        JSONdata (str): The JSON data to be added to the batch file.
    """
    with open('batch.txt', 'a') as batch_file:
        batch_file.write(JSONdata + "\n")
    print("Data added to batch:", JSONdata)

def sendBatch():
    """
    Sends the batch file to AWS DynamoDB and clears the batch file.
    If AWS is not reachable, it will return False.
    
    Returns:
        bool: True if the batch was sent successfully, False if AWS is not reachable.
    """

    batch_file = open('batch.txt', 'r')

    # Ping AWS
    if not ping_aws():
        print("AWS is not reachable. Exiting...")
        return False

    # AWS batcher
    with table.batch_writer() as batch:
        for line in batch_file:
            data = line.strip()
            batch.put_item(
                Item={
                    "uuid": str(uuid.uuid4()),
                    "components": str(data),
                }
            )

    batch_file.close()
    with open('batch.txt', 'w') as batch_file:
        batch_file.write("")  # Clear the batch file after sending

    print("Batch sent to DynamoDB and file cleared.")
    return True