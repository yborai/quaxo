import datetime

import pytz
import boto3

from .utils import get_stale_date

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
