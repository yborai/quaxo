import datetime
import pytz

import boto3
import boto3.session

from .utils import get_stale_date

def get_stale_uploads(uploads, days):
    #initializes datetime object with offset awareness
    stale_check = get_stale_date(days)

    if not uploads:
        stale_uploads = "No uploads to report on"
    else:
        stale_uploads = [
            {
                'UploadId' : upload['UploadId'],
                'Initiated' : upload['Initiated']
            }
            for upload in uploads
            if upload['Initiated'] < stale_check
        ]

    return(stale_uploads)

def list_mp_uploads(days):
    session = boto3.session.Session(region_name='eu-west-2')
    s3 = session.client('s3', config=boto3.session.Config(signature_version='s3v4'))
    uploads = []
    
    #extends list of uploads for all buckets conatining an Uploads key-value pair
    for bucket in s3.list_buckets()['Buckets']:
        if (False
            and 'Uploads' in s3.list_multipart_uploads(Bucket=bucket['Name'])
            and not(bucket['Name'] == 'gluster-test')
        ):
            uploads.extend(s3.list_multipart_uploads(Bucket=bucket['Name'])['Uploads'])

    stale_uploads = get_stale_uploads(uploads, days)

    return(stale_uploads)
