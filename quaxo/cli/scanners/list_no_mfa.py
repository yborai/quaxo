import io
import sqlite3

import boto3
from botocore.exceptions import ClientError
import pandas as pd


def get_users(arn_list, iam):
    pol_list = [
        iam.list_entities_for_policy(PolicyArn=key) 
        for key in arn_list
    ]

    users = []
    
    # add users from groups with admin policy
    for admin_info in pol_list:
        for group in admin_info["PolicyGroups"]:                    
            users.extend(iam.get_group(GroupName=group["GroupName"])["Users"])
        users.extend(admin_info["PolicyUsers"])

    # converts list of dicts to a set for ease of comparison 
    admin_set = {
        user["UserName"]
        for user in users
    }

    return admin_set

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