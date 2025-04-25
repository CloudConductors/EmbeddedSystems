# Build Instructions
The code for the Raspberry Pi can be run using Git Bash and Python. To upload and run the code for the Arduino, you will need the [Arduino IDE](https://www.arduino.cc/en/software/).

## Running Code for Raspberry Pi
1. Clone this repository.
```
git clone https://github.com/ITSC-4155-002/EmbeddedSystems.git
```
2. Open repository in Git Bash
3. Check if Python is installed:
```
python --version
```
- If Python is not installed, please use [this guide](https://pythongeeks.org/python-3-installation-and-setup-guide/) to install Python.
4. Navigate to the RaspberryPi directory
```
cd RaspberryPi/
```
5. Create a virtual environment
```
python -m venv venv
```
6. Activate virtual environment
```
source venv/Scripts/activate
```
7. Install required packages
```
pip install -r requirements.txt
```
8. Run the application
```
python app.py
```
**Please note, this application will not run if an Arduino is not connected on the COM3 serial port.**

## Uploading and Running Code on the Arduino
1. Open the Arduino IDE
2. Open EmbeddedSystems/Arduino/DataGenerator
```
File > Open
```
3. Once the sketch is loaded, select the Arduino board connected on COM3.

![Arduino IDE board selection](https://github.com/user-attachments/assets/a6b9fa47-0170-415e-9f80-f31c2c290f18)
   
4. Select "Upload"
5. Once the code has finished uploading, the Arduino will begin running when the Python application is launched.

