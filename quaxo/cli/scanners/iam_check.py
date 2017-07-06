import boto3
from .list_no_mfa import get_users

from .utils import get_users

def list_wo_policy(policies):
    iam = boto3.client('iam')

    #sets default Arn if none were given
    if not(policies):
        policies = ['arn:aws:iam::915928547063:policy/logicworks/LogicworksAllClients']

    #creates list of dicts with PolicyArn and all users with policy as it's items 
    pol_users = [
        {
            'PolicyArn': policy,
            'Users': get_users([policy], iam)
        }
        for policy in policies
    ]
    #obtains list of all users in an account for comparison
    all_users = {
        user['UserName']
        for user in iam.list_users()['Users']
    }

    #adjusts pol_users to contain all users without the requested policies
    for c in range(len(pol_users)):
        pol_users[c]['Users'] = list(all_users.difference(pol_users[c]['Users']))

    return pol_users
