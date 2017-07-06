import io
import sqlite3

import boto3
from botocore.exceptions import ClientError
import pandas as pd

from .utils import get_users


def generate_report(iam):
    # ensures credential report exists
    while(True):
        try:
            state = iam.generate_credential_report()["State"]
        except ClientError as e:
            continue

        if state == "COMPLETE":
            return True


def list_no_mfa():    
    iam = boto3.client('iam')
    conn = sqlite3.connect(":memory:")

    """add new policies to check for using list_entities_for_policy
       and ARN as new list item"""
    arn_list = [
        'arn:aws:iam::aws:policy/AdministratorAccess', 
    ]
    admin_set = get_users(arn_list, iam)

    generate_report(iam)

    # Creates file-like csv 
    iamcr = io.BytesIO(iam.get_credential_report()["Content"])  

    # pandas used to make list from binary csv
    cf = pd.read_csv(iamcr)
    cf.to_sql("MFATable", conn, if_exists="replace")
    query = """SELECT user, mfa_active FROM MFATable WHERE mfa_active = 0;"""
    query_info = pd.read_sql(query, conn)
    
    # All necessary user info put into a list of dicts
    response = [
        {
            "UserName" : user,
            "Policies_Attached" : iam.list_attached_user_policies(UserName=user)["AttachedPolicies"],
            "MFA_active" : False
        }
        for user in admin_set.intersection(set(query_info["user"]))
    ]

    return(response)