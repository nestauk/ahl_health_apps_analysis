"""
Merge Companies House data download with Charities data download, drop duplicates and save
"""

import pandas as pd

from ahl_health_apps_analysis.pipeline.create_companies_data_utils import *


def combine_charities_companies(companies_house, charities_data):

    # if duplicate charity name, then use row that has a url
    charities_data.sort_values(by="charity_contact_web_cleaned", inplace=True)
    charities_data_nodupes = charities_data.drop_duplicates(
        subset=["charity_name_cleaned"]
    )

    # if duplicate company name, then use a company that is of a category of interest to Nesta
    nesta_interest = set(
        [
            "Charitable Incorporated Organisation",
            "Community Interest Company",
            "Registered Society",
        ]
    )
    companies_house["nesta_interest"] = companies_house["CompanyCategory"].apply(
        lambda x: x in nesta_interest
    )
    companies_house.sort_values(by="nesta_interest", inplace=True, ascending=False)
    companies_house_nodupes = companies_house.drop_duplicates(
        subset=["CompanyName_cleaned"]
    )

    # Join CH and charities

    # Charities that arent in the Companies House (CH) data
    charities_data_not_in_ch = charities_data_nodupes[
        ~charities_data_nodupes["charity_name_cleaned"].isin(
            companies_house_nodupes["CompanyName_cleaned"].tolist()
        )
    ]

    # Concat CH with charities which aren't in CH
    charities_data_formatted = charities_data_not_in_ch[
        [
            "charity_name",
            "charity_name_cleaned",
            "charity_contact_web",
            "charity_contact_web_cleaned",
        ]
    ].rename(
        {
            "charity_name": "CompanyName",
            "charity_name_cleaned": "CompanyName_cleaned",
            "charity_contact_web": "CompanyURL",
            "charity_contact_web_cleaned": "CompanyURL_cleaned",
        },
        axis=1,
    )
    charities_data_formatted["CompanyCategory"] = ["Charity"] * len(
        charities_data_formatted
    )

    combined_data = pd.concat([companies_house_nodupes, charities_data_formatted])

    # Change CompanyCategory to "Charity" if name is in both
    combined_data.loc[
        combined_data["CompanyName_cleaned"].isin(
            charities_data_nodupes["charity_name_cleaned"].tolist()
        ),
        "CompanyCategory",
    ] = "Charity"

    return combined_data


if __name__ == "__main__":

    companies_house = pd.read_csv(
        "inputs/data/BasicCompanyDataAsOneFile-2023-02-01.csv",
        usecols=["CompanyName", "CompanyCategory"],
    )
    charities_data = pd.read_csv("inputs/data/publicextract.charity.csv")

    charities_data["charity_contact_web_cleaned"] = charities_data[
        "charity_contact_web"
    ].apply(lambda x: charity_url_clean(x) if pd.notnull(x) else None)

    companies_house["CompanyName_cleaned"] = companies_house["CompanyName"].apply(
        lambda x: clean_function(x)
    )
    charities_data["charity_name_cleaned"] = charities_data["charity_name"].apply(
        lambda x: clean_function(x)
    )

    combined_data = combine_charities_companies(companies_house, charities_data)

    # Save
    combined_data[
        [
            "CompanyName",
            "CompanyName_cleaned",
            "CompanyCategory",
            "CompanyURL",
            "CompanyURL_cleaned",
        ]
    ].to_csv("outputs/data/combined_company_data.csv")
