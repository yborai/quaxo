import boto3
import boto3.session

class PrivateSubnets(object):

    def __init__(self, region=None, account=None,):
        self.account = account
        self.region = region
        self.session = boto3.session.Session(region_name=self.region)
        self.elb = self.session.client(
            'elb', config=boto3.session.Config(signature_version='s3v4')
        )
        self.ec2 = self.session.client(
            'ec2', config=boto3.session.Config(signature_version='s3v4')
        )


    def private_subnets(self):
        subnets = []
        subnet_response = self.ec2.describe_subnets()
        for subnet in subnet_response['Subnets']:
            subnets.append(subnet['SubnetId'])

        igw = []
        internet_gateway_response = self.ec2.describe_internet_gateways()
        for gateway in internet_gateway_response['InternetGateways']:
            igw.append(gateway['InternetGatewayId'])    

        public_subs = []
        rt_response = self.ec2.describe_route_tables()
        for table in rt_response['RouteTables']:
            for route in table['Routes']:
                route_cidr_block = route.get('DestinationCidrBlock') == "0.0.0.0/0"
                gatewayid = route.get('GatewayId') in igw
                if route_cidr_block and gatewayid:
                    for assocation in table['Associations']:
                        if assocation.get('SubnetId') != None:
                            public_subs.append(assocation.get('SubnetId'))
        return self.double_check(public_subs, igw, subnets)

    def double_check(self, public_subs, igw, subnets):
        double_check_subnets = []
        for subnet in subnets:
            if subnet not in public_subs:
                double_check_subnets.append(subnet)

        subnet_response_2 = self.ec2.describe_subnets(
            Filters=[{'Name' : 'subnet-id', 'Values' : double_check_subnets}]
        )
        vpcs_need_to_check = []

        for subnet in subnet_response_2['Subnets']:
            vpcs_need_to_check.append(subnet['VpcId'])

        zipped = list(zip(double_check_subnets, vpcs_need_to_check))
        public_vpcs = []

        rt_response_2 = self.ec2.describe_route_tables(
            Filters=[{'Name' : 'vpc-id', 'Values' : vpcs_need_to_check}]
        )
        for table in rt_response_2['RouteTables']:
            for route in table['Routes']:
                route_cidr_block = route.get('DestinationCidrBlock') == "0.0.0.0/0"
                gatewayid = route.get('GatewayId') in igw
                if route_cidr_block and gatewayid:
                    for assocation in table['Associations']:
                        if assocation.get('SubnetId') == None:
                            public_vpcs.append(table.get('VpcId'))
        return self.combine(public_vpcs, public_subs, zipped)

    def combine(self, public_vpcs, public_subs, zipped):
        select_subnets = [item[0] for item in zipped if item[1] in public_vpcs]
        
        all_pubsubs = select_subnets + public_subs


        associated_priv_sub = []
        elb_names = []
        response = []
        lw_environment = None
        name = None
        elb_response = self.elb.describe_load_balancers()
        for elb_ in elb_response['LoadBalancerDescriptions']:
            for elb_subnet in elb_['Subnets']:
                if elb_subnet not in all_pubsubs:
                    elb_names.append(elb_['LoadBalancerName'])
                    associated_priv_sub.append(elb_subnet)
            
            tags = self.elb.describe_tags(LoadBalancerNames=[elb_.get('LoadBalancerName')])
            for tag in tags['TagDescriptions'][0]['Tags']:
                if tag.get('Key') == 'lw-environment':
                    lw_environment = tag.get('Value')
                if tag.get('Key') == 'Name':
                    name = tag.get('Value')

            elb_dict = dict(
                accout=self.account,
                region=self.region,
                load_blanacer_name=(elb_.get('LoadBalancerName')),
                load_balancer_name_tag=(name or 'no_name'),
                environment=(lw_environment or 'no_env'),
                invalid_subnets=associated_priv_sub,
                )
            response.append(elb_dict)
            associated_priv_sub = []

        return response
