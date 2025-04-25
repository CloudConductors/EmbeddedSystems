
# 🚀 Build Instructions  
The code for the Raspberry Pi can be run using **Git Bash** and **Python**.  
To upload and run the code for the Arduino, you'll need the [**Arduino IDE**](https://www.arduino.cc/en/software/).  

---

## 🐍 Running Code for Raspberry Pi

1. 📥 **Clone the repository**  
   ```bash
   git clone https://github.com/ITSC-4155-002/EmbeddedSystems.git
   ```

2. 📂 **Open the repository in Git Bash**

3. 🔍 **Check if Python is installed**  
   ```bash
   python --version
   ```
   - ❗ If not installed, follow this [Python installation guide](https://pythongeeks.org/python-3-installation-and-setup-guide/)

4. 📁 **Navigate to the RaspberryPi directory**  
   ```bash
   cd RaspberryPi/
   ```

5. 🛠️ **Create a virtual environment**  
   ```bash
   python -m venv venv
   ```

6. ⚡ **Activate the virtual environment**  
   ```bash
   source venv/Scripts/activate
   ```

7. 📦 **Install the required packages**  
   ```bash
   pip install -r requirements.txt
   ```

8. ▶️ **Run the application**  
   ```bash
   python app.py
   ```

   > ⚠️ **Note**: This application will not run unless an Arduino is connected to the **COM3** serial port.

---

## 🔌 Uploading and Running Code on the Arduino

1. 🧰 **Open the Arduino IDE**

2. 📄 **Open the Arduino sketch**  
   Navigate to:  EmbeddedSystems/Arduino/DataGenerator
   Using: `File > Open`

3. 🎯 **Select the connected Arduino board on COM3**  
   ![Arduino IDE board selection](https://github.com/user-attachments/assets/a6b9fa47-0170-415e-9f80-f31c2c290f18)

4. ⬆️ **Click "Upload"**

5. 🔁 **Once uploaded, the Arduino will start running** when the Python application is launched.
