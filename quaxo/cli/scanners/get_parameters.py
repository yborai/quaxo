import boto3
import boto3.session

def get_parameters(filters):
    session = boto3.session.Session(region_name='us-east-2')
    ssm = session.client('ssm', config=boto3.session.Config(signature_version='s3v4'))

    if not filters[0]['Key'] in ['Name', 'KeyId', 'Type']:
        return("Filter Key value not valid")

    return(ssm.describe_parameters(Filters=filters))
