import boto3
import serial
import asyncio
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
import uuid

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("cc-testing")

serialPort = serial.Serial(port="COM5", baudrate=9600, timeout=0)
serialPort.write("Hello from Raspberry Pi!\n".encode())
# wait for the arduino to send data
def read_serial_data():
    while True:
        data = serialPort.readline().decode("utf-8").strip()
        if data:
            print("Data received from Arduino: ", data)
            item = {"uuid": str(uuid.uuid4()), "message": data}
            print ("Item: ", item)
            table.put_item(Item=item)
            print("Data saved to DynamoDB")
            break

def read_table_data():
    response = table.scan()
    items = response["Items"]
    print("Data read from DynamoDB: ", items)

read_serial_data()
read_table_data()




