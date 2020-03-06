# Grow-Space

ECE490/ECE491 Capstone design project -- Grow Space.

## Installation
1. Clone this directory:
```git clone git@github.com:m-rubik/Grow-Space.git```

2. Open the directory:
```cd Grow-Space```

3. If you don't already have pipenv, install it:
```pip install pipenv```

4. Install the virtual environment from the Pipfile:
```pipenv install --sequential```. It's probably going to throw a warning about Python version 3.*. Ignore that, it's fine.

### Raspberry Pi 4b Extra Installation Steps

5. You might need to add the correct python path to the env variable. 

To do so, open with a text editor: ```sudo nano .env``` and add the following text: ```PYTHONPATH=${PYTHONPATH}:src```  

## Usage on Windows/Mac

### Command Line Arguments [args]
-r, --refresh: Refresh interval of the GUI (ms)  
-p, --polling: Polling interval of the sensors  
-s, --simulate: Boolean for simulating the environment (Default: False)  
-c, --config: Name of the environment configuration file

### Windows
#### Powershell
Navigate to the directory containing main.py then do:

1. ```pipenv shell``` to activate the pipenv

2. ```python ./main.py [args]``` to run the main program

#### VSCode

1. Ensure that the correct Python interpreter (the pipenv) is selected for running. This can be done by pressing ctrl+shift+p and typing "python: select interpreter" in the menu that appears at the top of the window
2. If prompted, create the launch.json file and add all your arguments. For example:  
"args": ["-s"]
3. Run+debug with F5 or run without debugging shift+F5

### MAC

_To be updated_

## Usage on Raspberry Pi 4b

Open a terminal and navigate to the grow-space directory, then:

```sudo /home/pi/.local/share/virtualenvs/Grow-Space-_9Jpauul/bin/python ./main.py [args]```

## Troubleshooting
If when trying to run the code in VSCODE it fails to launch debugger:
1. open settings.json
2. change "python.terminal.activateEnvironment" to False

## Contributing
Talk to Mason to obtain source directory accessed.  
Please make sure to update tests as appropriate.