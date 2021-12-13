import os
import boto3
import awspricing
from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
SECRET_KEY = os.getenv('AWS_SECRET_KEY')


client = boto3.client(
    'eks',
    region_name='us-west-2',
    aws_access_key_id='AKIAUHL7KHCHVDWI2TCN',
    aws_secret_access_key='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',
)

offer = awspricing.offer('AmazonEKS')