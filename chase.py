import sys
import os
import pandas as pd
from ..data import categories, desc, recategorize_by_desc


def process(df):
    # Rename Cateogry if the Cateogry contains the left side
    recategorize_category = {
        "Food & Drink": "Restaurant",
        "Gas": "Gas & Fuel",
        "Travel": "Public transportation",
        "Entertainment": "Entertainment",
    }

    # Places
    for key, value in desc.items():
        df.loc[df["Description"].str.contains(key, case=False), "Description"] = value

    # Subategories
    for key, value in recategorize_category.items():
        df.loc[df["Category"].str.contains(key, case=False), "Category"] = value
    for key, value in recategorize_by_desc.items():
        df.loc[df["Description"].str.contains(key, case=False), "Category"] = value

    df["Main Category"] = df["Category"].map(categories)
    df["Account"] = "Chase Sapphire Preferred"

    df["Amount"] *= -1
    df["Notes"] = df["Memo"]

    return df[
        [
            "Transaction Date",
            "Description",
            "Amount",
            "Category",
            "Notes",
            "Account",
            "Main Category",
        ]
    ]


if __name__ == "__main__":
    args = sys.argv[1]

    if args:
        print("Running")
        cwd = os.getcwd()
        file_name = args[:-4]
        df = pd.read_csv(args)
        df = df[df["Category"].notna()]
        process(df).to_csv(file_name + "_processed.csv", index=False)
        print("Saved as " + file_name + "_processed.csv")
    else:
        print("No arguments provided. Please provide csv file for processing.")
