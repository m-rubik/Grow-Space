# Grow-Space

ECE490/ECE491 Capstone design project -- Grow Space.

## Installation

1. Clone this directory:
```git clone https://github.com/m-rubik/Grow-Space.git```

2. Open the directory:
```cd Grow-Space```

3. If you don't already have pipenv, install it:
```pip install pipenv```

4. Install the virtual environment from the Pipfile:
```pipenv install --sequential```. It's probably going to throw a warning about Python version 3.*. Ignore that, it's fine.

## Usage on Personal Laptop
Navigate to the directory containing main.py then do:

```pipenv shell```

```python ./main.py```

## Usage on RPi

1. Ensure that the simulation option is disabled
```python
simulate_environment=False
``` 
in ```main.py``` as seen below:
```python
CLIENT = ThreadedClient(ROOT, simulate_environment=True)
```

2. ```sudo /home/pi/.local/share/virtualenvs/Grow-Space-_9Jpauul/bin/python ./main.py```

## Troubleshooting
ON THE RPI ONLY:
You might need to add the correct python path to the env variable. To do so, open with a text editor: ```sudo nano .env``` and add the following text:

```PYTHONPATH=${PYTHONPATH}:src```

Errors launching in VSCODE? If when trying to run the code in VSCODE it fails to launch debugger:
1. open settings.json
2. change "python.terminal.activateEnvironment" to False

## Contributing
Talk to Mason to get access as needed.

Please make sure to update tests as appropriate.
