from data_quality_validation_pydeequ import DataQualityValidation
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from tabulate import tabulate
from pathlib import Path
from pyspark.sql import SparkSession
from tabulate import tabulate

import boto3
import os
import fastparquet
import pydeequ
import pandas as pd
import botocore
import yaml


class sendEmailNotification:
    """ This class is used to send email notifications after validating the Data.
    """
    
    def __init__(
        self, 
        source_path: str, 
        target_path: dict, 
        email_config: dict, 
        **kwargs) -> None:
        """_summary_

        Args:
            source_path (str): Path to source data.
            target_path (str): Path to target data.
            email_config (dict): Email configuration settings.
        """
        os.environ["SPARK_VERSION"] = "3.0.1"
        path = Path(__file__).resolve().parent
        print(path)

        # Perform data quality validation and get result DataFrame
        self.result_df = self.execute_data_quality_validation(target_path)

        # Check if DataFrame is not empty
        if self.result_df is not None and not self.result_df.empty:  
            self.result_str = tabulate(self.result_df, headers='keys', tablefmt='grid')
            self.send_email(email_config, self.result_df)


    def execute_data_quality_validation(
        self, 
        target_path
        ):
        """ converts target data into a DataFrame

        Args:
            target_path (str): Path to target data.

        Returns:
            (pd.DataFrame): Result DataFrame
        """

        result_df = pd.read_parquet(target_path, engine='fastparquet')       
        return  result_df.loc[~result_df['check'].isna()] 


    def send_email(
        self, 
        email_config: dict, 
        result_df: pd.DataFrame
        ) -> None:
        """_summary_

        Args:
            email_config (dict): Email configuration settings.
            result_df (pd.DataFrame):  Result DataFrame
        """
        if result_df is None or result_df.empty:
            print("Error: Result DataFrame is None or empty. Cannot send email.")
            return

        # Save the result DataFrame to a temporary Parquet file
        temp_file_path = "temp_result.parquet"
        result_df.to_parquet(temp_file_path, index=False)

        # Create the email message
        msg = MIMEMultipart()
        msg['Subject'] = "Data Quality Validation Result"
        msg['From'] = email_config["sender_email"]
        msg['To'] = email_config["receiver_email"]

        # Add the test message to the email body
        body = "Hello,\n\nPlease find the attached data quality validation result in Parquet format.\n\nBest regards,\nYour Team"
        msg.attach(MIMEText(body, 'plain'))

        # Attach the Parquet file to the email
        with open(temp_file_path, "rb") as attachment:
            part = MIMEApplication(attachment.read(), Name=os.path.basename(temp_file_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(temp_file_path)}"'
            msg.attach(part)

        # Send the email using SES
        session = boto3.Session(
            aws_access_key_id=email_config["aws_access_key_id"],
            aws_secret_access_key=email_config["aws_secret_access_key"],
            aws_session_token=email_config["aws_session_token"]
        )

        ses = session.client('ses', region_name=email_config["aws_region"])
        response = ses.send_raw_email(RawMessage={'Data': msg.as_string()})

        # Delete the temporary Parquet file after sending the email
        os.remove(temp_file_path)

        print("Email sent successfully!")
        print("Message ID:", response['MessageId'])



class DqvPydeequ:
    """Class for performing data quality validation using PyDeequ"""

    def __init__(
        self,
        config_path: str,
        source_path: str,
        target_path: str,
        **kwargs
    ) -> None:
        """Initialize the DqvPydeequ class.

        Args:
            config_path (str): Path to configuration file.
            source_path (str): Path to source data.
            target_path (str): Path to target data.
        """
        spark = (
            SparkSession.builder.appName("data_quality_validation_pydeequ")
            .enableHiveSupport()
            .config("spark.dynamicAllocation.enabled", "true")
            .config("spark.jars.packages", pydeequ.deequ_maven_coord)
            .config("spark.jars.excludes", pydeequ.f2j_maven_coord)
            .config("spark.default.parallelism", "10")
            .config("spark.sql.shuffle.partitions", "10")
            .config("spark.sql.files.ignoreCorruptFiles", "true")
            .getOrCreate()
        )
        with open(config_path, "r") as stream:
            data = yaml.safe_load(stream)
        config = data["DQ_ASSERTIONS"]["DIR1"]["PRODUCT_FILE"]
        print(config)
        try:
            bolosse = DataQualityValidation(
                spark,
                source_path,
                target_path,
                config,
            )
            bolosse.execute()
            spark.stop()
        except Exception as ex:
            print(ex)
            spark.stop()
