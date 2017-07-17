import boto3
import boto3.session

def get_overrides(days):
    session = boto3.session.Session(region_name='us-east-2')
    logs = session.client('logs', config=boto3.session.Config(signature_version='s3v4'))
    log_groups = logs.describe_log_groups()['logGroups']
    default = None

    if days:
        default = days

    refined_logs = [
        log_group
        for log_group in log_groups
        if not (log_group.get('retentionInDays') == default)
    ]

    return(refined_logs)
