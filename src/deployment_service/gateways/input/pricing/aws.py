import os
import pdb
import boto3
import awspricing
# from dotenv import load_dotenv

# load_dotenv()

# ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
# SECRET_KEY = os.getenv('AWS_SECRET_KEY')
if __name__ == '__main__':


    # client = boto3.client(
    #     'eks',
    #     region_name='us-west-2',
    #     aws_access_key_id='AKIAUHL7KHCHVDWI2TCN',
    #     aws_secret_access_key='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',
    # )

    # offer = awspricing.offer('AmazonEKS')
    # import pdb
    # pdb.set_trace()

    # import boto3

    pricing_client = boto3.client(
        'pricing', 
        region_name='us-east-1',
        aws_access_key_id='AKIAUHL7KHCHVDWI2TCN',
        aws_secret_access_key='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',

    )

    response = pricing_client.get_products(
        ServiceCode='string',
        Filters=[
            {
                'Type': 'TERM_MATCH',
                'Field': 'ServiceCode',
                'Value': 'AmazonEKS'
            },
        ],
    #     FormatVersion='string',
    #     NextToken='string',




    #     MaxResults=123
    )
    import pdb
    pdb.set_trace()

    # response = pricing_client.describe_services(ServiceCode='AmazonEKS')

    # attribute_names = response['Services'][0]['AttributeNames']

    # for attribute_name in attribute_names:

    #     attribute_values = []

    #     response_iterator = pricing_client.get_paginator('get_attribute_values').paginate(
    #         ServiceCode='AmazonEKS',
    #         AttributeName=attribute_name
    #     )

    #     for response in response_iterator:
    #         for attribute_value in response['AttributeValues']:
    #             attribute_values.append(attribute_value['Value'])

    #     print('Attribute Name:', attribute_name)
    #     print(attribute_values)
