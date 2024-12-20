# bread

Local HTML interface that processes transaction exports from various banks. Uploads are categorized using a Python script. Category and description mappings are listed in `data.py`

## Instructions

Run `python3 app.py`

Open `index.html`

Upload a `.csv` file or a `.xlsx` file depending on the bank. The folllowing banks are supported:

1. Amex (xlsx)
2. Bilt (csv)
3. Capital One (csv)
4. Chase (csv)
5. Citi (csv)

Click the "Run" button to process the file and download the result as a `.csv`

Feel free to add more mappings to `data.py` as desired
