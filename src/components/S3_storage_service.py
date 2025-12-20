import sys
import boto3
from botocore.exceptions import ClientError

from src.config import Config
from src.logger import logging
from src.exception import CustomException



class S3Storage:
    def __init__(self):
        try:
            logging.info("Initializing S3 Storage Service")
            self.s3 = boto3.client(
                's3',
                aws_access_key_id=Config.AWS_ACCESS_KEY,
                aws_secret_access_key=Config.AWS_SECRET_KEY
            )
            self.bucket = Config.AWS_BUCKET_NAME
            logging.info("S3 Storage Service initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing S3 Storage Service: {str(e)}")
            raise CustomException(e, sys)


    def upload_file(self, file_path, filename):
        try:
            logging.info(f"Uploading file {filename} to S3 bucket {self.bucket}")
            self.s3.upload_file(file_path, self.bucket, filename)
            logging.info(f"File {filename} uploaded successfully")
            return True
        except ClientError as e:
            logging.error(f"Error uploading file: {e}")
            raise CustomException(e, sys)


    def get_file(self, filename):
        try:
            logging.info(f"Retrieving file object {filename} from S3 bucket {self.bucket}")
            file_obj = self.s3.get_object(Bucket=self.bucket, Key=filename)
            logging.info(f"File {filename} retrieved successfully")
            return file_obj
        except ClientError as e:
            logging.error(f"Error retrieving file: {e}")
            raise CustomException(e, sys)