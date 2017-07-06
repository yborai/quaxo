import datetime
import pytz

def get_stale_date(days):
    today = datetime.datetime.now(pytz.UTC)

    #checks to see if days should be set to default
    if days is None:
        num_days = 30
    else:
        num_days = days

    return(today - datetime.timedelta(days=num_days))

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