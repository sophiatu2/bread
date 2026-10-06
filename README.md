# bread

Local HTML interface that processes transaction exports from various banks. Uploads are categorized using a Python script. Category and description mappings are listed in `scripts/data.py`

## Setup

Requires Python 3.9 or newer.

Create a virtual environment and install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

macOS ships `python3`/`pip3` but no plain `python`/`pip`, which is why `pip install` fails with "command not found" outside a virtual environment. Activating the venv provides both.

Re-run `source .venv/bin/activate` in each new terminal session. To skip activation, call the venv directly: `.venv/bin/python app.py`

## Instructions

Run `python3 app.py`

Open `index.html`

Upload a `.csv` file. The following banks are supported:

1. Amex
2. Bilt
3. Capital One
4. Capital One Checking
5. Chase
6. Citi

Click the "Run" button to process the file and download the result as a `.csv`

Feel free to add more mappings to `scripts/data.py` as desired
