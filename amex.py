import sys
import os
import pandas as pd
from ..data import categories, desc, recategorize_by_desc


def process(df):

    # Rename Cateogry if the Cateogry contains the left side
    recategorize_category = {
        "Taxis & Coach": "Ride share",
        "Internet Purchase": "Shopping",
        "Fuel": "Gas & Fuel",
        "Clothing": "Clothing",
        "Rail Services": "Public transportation",
        "Merchandise & Supplies": "Merchandise",
        "Business Services": "Other services",
        "Restaurant": "Restaurant",
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
    df["Account"] = "Amex Blue Cash Everyday"
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

    return df[
        [
            "Date",
            "Description",
            "Amount",
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
        file_name = args[:-5]
        df = pd.read_excel(args, sheet_name=0)

        ### Clean dataframe ###
        # Reset columns
        df.columns = df.iloc[5]
        df = df[6:]

        # Remove rows with no category
        df = df[df["Category"].notna()]

        process(df).to_csv(file_name + "_processed.csv", index=False)
        print("Saved as " + file_name + "_processed.csv")
    else:
        print("No arguments provided. Please provide file for processing.")
