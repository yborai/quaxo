import boto3
import boto3.session

def get_private_subnets(subnets, vpcs, public_vpcs):
    subs_vpcs = list(zip(subnets,vpcs))
    public_subs = [item[0] for item in subs_vpcs if item[1] in public_vpcs]
    private_subs = []
    for subnet in subnets:
        if subnet not in public_subs:
            private_subs.append(subnet)
    return private_subs

def private_subnets():
    session = boto3.session.Session(region_name='us-east-1')
    elb = session.client('elb', config=boto3.session.Config(signature_version='s3v4'))
    ec2 = session.client('ec2', config=boto3.session.Config(signature_version='s3v4'))
    subnets = []
    vpcs = []

    elb_response = elb.describe_load_balancers()
    for load_balancer in elb_response['LoadBalancerDescriptions']:
        for subnet in load_balancer['Subnets']:
            subnets.append(subnet)
            vpcs.append(load_balancer['VPCId'])

    related_rts = []
    public_vpcs = []
    rt_response = ec2.describe_route_tables()
    for table in rt_response['RouteTables']:
        for vpc in vpcs:
            if table['VpcId'] == vpc:
                related_rts.append(table['RouteTableId'])
                for routes in table['Routes']:
                        if routes.get('DestinationCidrBlock') == "0.0.0.0/0":
                            public_vpcs.append(table['VpcId'])
    import pdb;pdb.set_trace()
    return get_private_subnets(subnets, vpcs, public_vpcs)
