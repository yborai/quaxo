import datetime

import pytz
import boto3

def get_stale_date(days):
    today = datetime.datetime.now(pytz.UTC)

    #checks to see if days should be set to default
    if days is None:
        num_days = 30
    else:
        num_days = days

    return(today - datetime.timedelta(days=num_days))

def get_snaps(days):
    client = boto3.client('ec2')
    snapshots = client.describe_snapshots()

    #initializes datetime object with offset awareness
    stale_check = get_stale_date(days)

    """Checks through list of snapshots and compares with
       datetime object for n days ago"""
    final_snapshots = [
        {
            'SnapshotId' : snapshot['SnapshotId'],
            'StartTime' : snapshot['StartTime']
        }
        for snapshot in snapshots['Snapshots']
        if snapshot['StartTime'] < stale_check
    ]

    return final_snapshots