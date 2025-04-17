import boto3
import serial
import asyncio
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
import uuid
import datetime
import json
from anomaly import anomaly_prediction, download_model_from_s3

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("cc-testing")

serialPort = serial.Serial(port="COM3", baudrate=9600, timeout=0)

# https://github.com/pyserial/pyserial/issues/216#issuecomment-369414522
class ReadLine:
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s
    
    def readline(self):
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b"\n")
            if i >= 0:
                r = self.buf + data[:i+1]
                self.buf[0:] = data[i+1:]
                return r
            else:
                self.buf.extend(data)

def read_serial_data():
    reader = ReadLine(serialPort)
    while True:
        data = reader.readline()
        if data:
            yield data.decode("utf-8").strip()

async def send_to_dynamodb(data):
    try:
        response = table.put_item(
            Item={
                "uuid": str(uuid.uuid4()),
                "message": str(data),
            }
        )
        print("Data sent to DynamoDB:", data)
    except ClientError as e:
        print("Error sending data to DynamoDB:", e.response["Error"]["Message"])
    except Exception as e:
        print("An unexpected error occurred:", str(e))

def append_timestamp(data): # this is in json format
    try:
        data_dict = json.loads(data)
        data_dict["timestamp"] = f"{datetime.datetime.now().year}-{datetime.datetime.now().month:02d}-{datetime.datetime.now().day:02d} {datetime.datetime.now().hour:02d}:{datetime.datetime.now().minute:02d}:{datetime.datetime.now().second:02d}"
        return json.dumps(data_dict)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", str(e))
        return None


async def main():
    clf = download_model_from_s3()
    loop = asyncio.get_event_loop()
    serial_data = read_serial_data()
    while True:
        data = next(serial_data)
        if not (data.startswith("{")):
            continue
        data_with_timestamp = append_timestamp(data)
        if data_with_timestamp:
            anomaly_prediction(data_with_timestamp, clf)
        await asyncio.sleep(10)

asyncio.run(main())