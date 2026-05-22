import sys
import os
import pandas as pd
from data import categories, desc, recategorize_by_desc


def process(df):

    df["Account"] = "Citi Double Cash"
    df["Desc"] = ""
    df["Category"] = ""

    # Places
    for key, value in desc.items():
        df.loc[df["Description"].str.contains(key, case=False), "Description"] = value

    # Subategories
    for key, value in recategorize_by_desc.items():
        df.loc[df["Description"].str.contains(key, case=False), "Category"] = value

    df["Main Category"] = df["Category"].map(categories)

    # Account Names
    # df["Account Name"] = df["Account Name"].replace(
    #     {
    #         "CREDITCARD Account": "Capital One SavorOne",
    #         "CHECKING Account": "360 Checking",
    #     },
    # )

    # df.loc[df["Account Name"].str.contains("Blue Cash"), "Account Name"] = "Amex Blue"
    # df.loc[df["Account Name"].str.contains("Delta"), "Account Name"] = "Amex Delta"

    df["Amount"] = df["Debit"].fillna(df["Credit"])

    return df[
        [
            "Date",
            "Description",
            "Amount",
            "Desc",
            "Main Category",
            "Category",
            "Account",
        ]
    ]


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python amex.py <input_path> <output_path>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    print("Running")
    cwd = os.getcwd()
    df = pd.read_csv(input_path)
    process(df).to_csv(output_path, index=False)
    print("Saved as " + output_path)
