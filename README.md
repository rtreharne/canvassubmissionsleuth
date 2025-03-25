# Canvas Submission Sleuth

## Authors

This tool was created by Jack Foster and Robert Treharne from the School of Bioscience's Technology Enhanced Learning (TEL) team at the University of Liverpool.

## Overview

This tool lets you take a much deeper look at the Meta Data associated with a Canvas assignment's submissions.


## Run Using Goolge Colab (Easiest Method)
- [Google Colab](https://colab.research.google.com/drive/1rTJIuVO-sCQXt4ZWThDeX61m3zLvI_rz?usp=sharing)

## Virtual Environment Setup
To create a virtual environment and install dependencies:
1. Create a virtual environment named `.venv`:
   ```sh
   python -m venv .venv
   ```
2. Activate the virtual environment:
   - On macOS/Linux:
     ```sh
     source .venv/bin/activate
     ```
   - On Windows:
     ```sh
     .venv\Scripts\activate
     ```
3. Install required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

### 1. Run the Script
Execute the script using:
```sh
python script.py
```

### 2. Follow the Prompts
The script will:
1. Prompt for Canvas API credentials (if not provided in `config.py`).
2. Retrieve submissions for the specified assignments.
3. Throw all the submission data into .csv file.


## Configuration
For convenience, you can store API credentials in a `config.py` file:
```python
API_URL = "https://canvas.example.com"
API_TOKEN = "your_api_token_here"
```
This will prevent the script from prompting you each time.

## License
This project is released under the MIT License.

