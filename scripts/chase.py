import sys
import os
import pandas as pd
from data import categories, desc, recategorize_by_desc


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
            "Notes",
            "Main Category",
            "Category",
            "Account",
        ]
    ]


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python chase.py <input_path> <output_path>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    print("Running")
    cwd = os.getcwd()
    df = pd.read_csv(input_path)
    df = df[df["Category"].notna()]
    process(df).to_csv(output_path, index=False)
    print("Saved as " + output_path)
