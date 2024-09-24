import os
import pandas as pd
import numpy as np
from datetime import datetime

from application_object import SnapApplication

NUM_APPLICANTS = 0

def generate_application_details(ingestion_attrs):
    """
    Run the ingestion process for country profiles. Builds and saves tables for
    country profiles into parquet files

    Parameters:
    - ingestion_attrs (dict): A dictionary containing attributes necessary for ingestion.
        Required keys:
            - latest_year (int): The latest year of data.
            - data_coverage_from_latest_year (int): Data coverage from the latest year.
            - limit_data_coverage (bool): Whether to limit data coverage and filter data
            - product_classification (str)
            - schema (str): use "country_profiles"
            - data_dir (str): Directory path where input data is located
            - output_dir (str): Directory path where output data will be saved
            - other_data (str): Directory path for other data files
    """
    data_dir = ingestion_attrs["data_dir"]
    file_name = ingestion_attrs["file_name"]

    applications = pd.read_csv(os.path.join(data_dir, file_name))
    applications = applications[applications.STATENAME == ingestion_attrs["state_name"]]
    # add meta data obj num applicants in state... etc

    applications = clean_data(applications)

    # Open the CSV file and write the dictionaries
    with open(
        f"model_input_{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.txt", "w"
    ) as txtfile:

        for applicant_num in range(applications.shape[NUM_APPLICANTS]):
            print(applicant_num)
            txtfile.write(f"Information about Applicant: {applicant_num}")
            txtfile.write("\n")
            # one application becomes a pandas series
            single_application = applications.iloc[applicant_num]
            snapp = SnapApplication(single_application)
            txtfile.write(snapp.application_story)
            txtfile.write("\n \n")


def clean_data(df):
    """"""
    return df


import os
import pandas as pd
import numpy as np
from datetime import datetime

from application_object import SnapApplication

NUM_APPLICANTS = 0


def generate_application_details(ingestion_attrs):
    """
    Run the ingestion process for country profiles. Builds and saves tables for
    country profiles into parquet files

    Parameters:
    - ingestion_attrs (dict): A dictionary containing attributes necessary for ingestion.
        Required keys:
            - latest_year (int): The latest year of data.
            - data_coverage_from_latest_year (int): Data coverage from the latest year.
            - limit_data_coverage (bool): Whether to limit data coverage and filter data
            - product_classification (str)
            - schema (str): use "country_profiles"
            - data_dir (str): Directory path where input data is located
            - output_dir (str): Directory path where output data will be saved
            - other_data (str): Directory path for other data files
    """
    data_dir = ingestion_attrs["data_dir"]
    file_name = ingestion_attrs["file_name"]

    applications = pd.read_csv(os.path.join(data_dir, file_name))
    applications = applications[applications.STATENAME == ingestion_attrs["state_name"]]
    # add meta data obj num applicants in state... etc

    applications = clean_data(applications)

    snap_stories = {}

    for applicant_num in range(applications.shape[NUM_APPLICANTS]):
        single_application = applications.iloc[applicant_num]
        snapp = SnapApplication(single_application)
        snap_string = snapp.application_story .replace(',', '.').replace("'", '')
        snap_stories[applicant_num] = [snap_string]
        # print(snap_stories)
    snap_df = pd.DataFrame.from_dict(snap_stories).T
    snap_df.to_csv('~/snap/snap_qc_results.csv')

def clean_data(df):
    """"""
    return df

if __name__ == "__main__":
    ingestion_attrs = {
        "state_name": "District of Columbia",
        "qc_year": 2022,
        "data_dir": "/Users/esiu/Desktop/SNAP",
        "file_name": "qc_2022_dc.csv",
        "output_dir": "/Users/esiu/Desktop/SNAP"
    }
    generate_application_details(ingestion_attrs)

    
