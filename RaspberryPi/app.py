import boto3
import serial
import asyncio
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
import datetime
import json
from anomaly import anomaly_prediction, download_model_from_s3
from batcher import addToBatch, sendBatch
from network import ping_aws
import pickle

serialPort = serial.Serial(port="COM3", baudrate=9600, timeout=0)

class ReadLine:
    """
    A class to read lines from a serial port.

    Attributes:
        s (serial.Serial): The serial port to read from.
    """

    def __init__(self, s):
        """
        Initializes the ReadLine class.

        Parameters:
            s (serial.Serial): The serial port to read from.
        """
        self.buf = bytearray()
        self.s = s
    
    def readline(self):
        """
        Read a line from the serial port. This method will wait until a newline character is found.

        Returns:
            bytes: The line read from the serial port, including the newline character.
        """
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
    """
    Reads serial data sent by Arduino, yields any collected data.
    """
    reader = ReadLine(serialPort)
    while True:
        data = reader.readline()
        if data:
            yield data.decode("utf-8").strip()


def append_timestamp(data):
    """
    Appends a timestamp to the data. 

    Parameters:
        data (str): The data to which the timestamp will be appended.

    Returns:
        str: The data with the timestamp appended in the format YYYY-MM-DD HH:MM:SS.
    """
    try:
        # Assuming data is a JSON string, parse it to a dictionary and add the timestamp
        data_dict = json.loads(data)
        data_dict["timestamp"] = f"{datetime.datetime.now().year}-{datetime.datetime.now().month:02d}-{datetime.datetime.now().day:02d} {datetime.datetime.now().hour:02d}:{datetime.datetime.now().minute:02d}:{datetime.datetime.now().second:02d}"
        return json.dumps(data_dict)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", str(e))
        return None

async def data_handler(data, current_size, max_size):
    """
    Handles the data by adding it to the batch and checking if the batch size exceeds the maximum size.
    If the batch size exceeds the maximum size, it sends the batch to AWS.

    Parameters:
        data (str): The data to be handled.
        current_size (int): The current size of the batch.
        max_size (int): The maximum size of the batch.

    Returns:
        bool: True if the batch was sent successfully, False otherwise.
    """

    # Add data to batch
    addToBatch(data)

    # Send batch if size exceeds max size
    if current_size >= max_size:
        if sendBatch():
            print("Batch sent successfully.")
            return True
        else:
            print("Network error, batch not sent.")
            return False
    else:
        return False

async def anomaly_prediction_catchup(clf, max_size):
    """
    When network is restored, this function reads the entire batch file and checks for anomalies.
    If an anomaly is detected, it sends the data to AWS.

    Parameters:
        clf (object): The anomaly detection model.
        max_size (int): The maximum size of the batch.
    """

    # Read the last 5 lines from the batch file
    with open('batch.txt', 'r') as batch_file:
        lines = batch_file.readlines()[0:]

    print("Starting anomaly detection catchup...", flush=True)

    # Process each line and check for anomalies
    for line in lines:
        data = line.strip()
        if data.startswith("{"):
            data_with_timestamp = append_timestamp(data)
            if data_with_timestamp:
                if anomaly_prediction(data_with_timestamp, clf):
                    await data_handler(data_with_timestamp, max_size, max_size)
    
    print("Anomaly detection catchup completed.\n", flush=True)


async def main():
    """
    Main function to handle the data stream from Arduino, check for anomalies, and send data to AWS.
    """

    current_size = 0
    max_size = 144 # 12 hours of data at 5 min intervals
    outage = False

    print("Starting program...")

    # Download the model from S3
    clf = download_model_from_s3()
    if clf is False:
        file = open("anomaly_prediction.pkl", "rb")
        if file:
            clf = pickle.load(file)
            file.close()

            print("Prediction model loaded from local file.", flush=True)
        else:
            print("Prediction model not found locally. Exiting...", flush=True)
            return
    else:
        print("Prediction model downloaded from AWS S3.", flush=True)
        
    # Main
    loop = asyncio.get_event_loop()
    serial_data = read_serial_data()
    while True:
        # Check network connection
        if not ping_aws():
            print("Network outage detected, waiting for recovery...", flush=True)
            print("Caching data until network is restored...", flush=True)
            outage = True
            while outage:
                if ping_aws():
                    print("Network restored.", flush=True)
                    await anomaly_prediction_catchup(clf, max_size)
                    outage = False
                else: # Cache data until network is restored
                    data = next(serial_data)
                    if data.startswith("{"):
                        print("Data received.")
                        data_with_timestamp = append_timestamp(data)
                        print(data_with_timestamp)
                        if data_with_timestamp:
                            await data_handler(data_with_timestamp, current_size, max_size)
                            current_size += 1
                        print("\n")


        data = next(serial_data) # Read data from serial port
        if not (data.startswith("{")): # Arduino sends notifications, don't want to parse those lol
            continue

        data_with_timestamp = append_timestamp(data) # Arduino doesn't have RTC
        print("Data received.")
        print(data_with_timestamp)

        # If there is data and it is a JSON string, process it
        if data_with_timestamp:
            if anomaly_prediction(data_with_timestamp, clf):
                # Circumvent batcher, this is important because we need to send the data immediately
                current_size = max_size
                await data_handler(data_with_timestamp, current_size, max_size) # doing it this way allows for network check
                print("Anomaly detected, batch sent immediately.", flush=True)
                current_size = 0
            else:
                print(f"Current batch size: {current_size + 1}.", flush=True)
                if await data_handler(data_with_timestamp, current_size, max_size):
                    current_size = 0
                else:
                    current_size += 1

        print("\n", flush=True)
        await asyncio.sleep(300) # 5 min intervals

asyncio.run(main())