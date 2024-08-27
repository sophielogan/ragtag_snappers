import os
import pandas as pd
import numpy as np

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

    for applicant_num in range(applications.shape[NUM_APPLICANTS]):
        # send as series
        single_application = applications.iloc[applicant_num]
        SnapApplication(single_application)


if __name__ == "__main__":
    ingestion_attrs = {
        "state_name": "District of Columbia",
        "qc_year": 2022,
        "data_dir": "C:/Users/SLogan/Downloads/snapqc_generate_text (2)/data",
        "file_name": "qcfy2022_csv.zip",
        "output_dir": "C:/Users/SLogan/Downloads/snapqc_generate_text (2)/output",
        # "data_dir": "/Users/ELJ479/pprojects/policy2code/data",
        # "file_name": "qcfy2022_csv.zip",
        # "output_dir": "/Users/ELJ479/pprojects/policy2code/output"
    }
    generate_application_details(ingestion_attrs)
