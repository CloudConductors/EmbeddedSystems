import boto3
import serial
import asyncio
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
import uuid
import datetime
import json
from anomaly import anomaly_prediction, download_model_from_s3
from batcher import addToBatch, sendBatch

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

def append_timestamp(data): # this is in json format
    try:
        data_dict = json.loads(data)
        data_dict["timestamp"] = f"{datetime.datetime.now().year}-{datetime.datetime.now().month:02d}-{datetime.datetime.now().day:02d} {datetime.datetime.now().hour:02d}:{datetime.datetime.now().minute:02d}:{datetime.datetime.now().second:02d}"
        return json.dumps(data_dict)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", str(e))
        return None

async def data_handler(data, current_size, max_size):
    addToBatch(data)

    if current_size >= max_size:
        sendBatch()
        return True
    else:
        return False

async def main():
    current_size = 0
    max_size = 5

    # Download the model from S3
    clf = download_model_from_s3()

    # Main
    loop = asyncio.get_event_loop()
    serial_data = read_serial_data()
    while True:
        data = next(serial_data)
        if not (data.startswith("{")): # Arduino sends notifications, don't want to parse those lol
            continue

        data_with_timestamp = append_timestamp(data) # Arduino doesn't have RTC
        if data_with_timestamp:
            if anomaly_prediction(data_with_timestamp, clf):
                # Circumvent batcher, this is important because we need to send the data immediately
                sendBatch()
                print("Anomaly detected, batch sent immediately")
                current_size = 0
            else:
                print(f"Current batch size: {current_size}")
                if await data_handler(data_with_timestamp, current_size, max_size):
                    current_size = 0
                else:
                    current_size += 1

        await asyncio.sleep(10) # Eepy

asyncio.run(main())