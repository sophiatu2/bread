import sys
import os
import pandas as pd
from data import categories, desc, recategorize_by_desc


def process(df):

    # Places
    for key, value in desc.items():
        df.loc[df["Description"].str.contains(key, case=False), "Description"] = value

    # Subategories
    for key, value in recategorize_by_desc.items():
        df.loc[df["Description"].str.contains(key, case=False), "Category"] = value

    df["Main Category"] = df["Category"].map(categories)
    df["Account"] = "Capital One SavorOne"
    df["Desc"] = ""

    # Account Names
    # df["Account Name"] = df["Account Name"].replace(
    #     {
    #         "CREDITCARD Account": "Capital One SavorOne",
    #         "CHECKING Account": "360 Checking",
    #     },
    # )

    # df.loc[df["Account Name"].str.contains("Blue Cash"), "Account Name"] = "Amex Blue"
    # df.loc[df["Account Name"].str.contains("Delta"), "Account Name"] = "Amex Delta"

    df.loc[df["Credit"] > 0, "Debit"] = -df.Credit

    return df[
        [
            "Transaction Date",
            "Description",
            "Debit",
            "Category",
            "Desc",
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
        process(df).to_csv(file_name + "_processed.csv", index=False)
        print("Saved as " + file_name + "_processed.csv")
    else:
        print("No arguments provided. Please provide csv file for processing.")
