import boto3
import serial
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
import uuid

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("cc-testing")

serialPort = serial.Serial(port="COM5", baudrate=9600, timeout=0)
size = 12
index = 100

while True:
    data = serialPort.readline(13)
    data = data.decode("utf-8")

    if data:
        print(data) # Currently has an issue that it will not print the data until program is closed (newline issue on the arduino side)