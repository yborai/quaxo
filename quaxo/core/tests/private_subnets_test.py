from cement.utils import test

from ...cli.scanners.private_subnets import PrivateSubnets
from .base import QuaxoRunner


class TestQuaxo(test.CementTestCase):

    def test_private_subnets_help(self):
        QuaxoRunner.assert_quaxo_success(self, [
            "private-subnets", "--help"
        ])

    def test_get_private_subnets(self):
        vpc_2 = ['vpc-88ac4bec', 'vpc-f810dc9c', 'vpc-6f1fa208']
        public_subs = [
            'subnet-96f929cc',
            'subnet-348b0a7c',
            'subnet-75804859',
            'subnet-3046e11a',
            'subnet-bd144d97',
            'subnet-1f712334',
            'subnet-ec04c3d1',
            'subnet-53144d79',
        ]
        zipped = [
            ('subnet-6c707447', 'vpc-35c77d51'),
            ('subnet-851dafdd', 'vpc-7f92af1b'),
            ('subnet-d72c36ed', 'vpc-88ac4bec'),
            ('subnet-4602b01e', 'vpc-7f92af1b'),
            ('subnet-d91daf81', 'vpc-3f93ae5b'),
            ('subnet-9f82d9c7', 'vpc-6d1fa20a'),
            ('subnet-62582949', 'vpc-88ac4bec'),
            ('subnet-78a0ae0e', 'vpc-fe1ca199'),
            ('subnet-fb1caea3', 'vpc-3f93ae5b'),
            ('subnet-fc1dafa4', 'vpc-7f92af1b'),
            ('subnet-54144d7e', 'vpc-6c1fa20b'),
            ('subnet-36a5ce0b', 'vpc-0ed4f96a'),
            ('subnet-85d4def2', 'vpc-f810dc9c'),
            ('subnet-6481da3c', 'vpc-fe1ca199'),
            ('subnet-2d014d74', 'vpc-88ac4bec'),
            ('subnet-2e1a3677', 'vpc-f810dc9c'),
            ('subnet-b98cbc85', 'vpc-a31ca1c4'),
            ('subnet-c65950eb', 'vpc-6f1fa208'),
            ('subnet-2e1cae76', 'vpc-3f93ae5b'),
            ('subnet-658ca612', 'vpc-88ac4bec'),
        ]

        ps = PrivateSubnets()

        print(ps.combine(vpc_2, public_subs, zipped))
        assert ps.combine(vpc_2, public_subs, zipped) == [
            {
                "accout": None,
                "region": None,
                "load_blanacer_name": "kelvin-training-DMZ",
                "load_balancer_name_tag": "kelvin-trainin-ELB",
                "environment": "no_env",
                "invalid_subnets": []
            },
            {
                "accout": None,
                "region": None,
                "load_blanacer_name": "chef-server",
                "load_balancer_name_tag": "kelvin-trainin-ELB",
                "environment": "no_env",
                "invalid_subnets": []
            },
            {
                "accout": None,
                "region": None,
                "load_blanacer_name": "chef-server2",
                "load_balancer_name_tag": "kelvin-trainin-ELB",
                "environment": "no_env",
                "invalid_subnets": []
            },
            {
                "accout": None,
                "region": None,
                "load_blanacer_name": "Dashboard-test",
                "load_balancer_name_tag": "DashBoard-Demo",
                "environment": "no_env",
                "invalid_subnets": []
            },
            {
                "accout": None,
                "region": None,
                "load_blanacer_name": "Dashboard-demo",
                "load_balancer_name_tag": "Dashboard-ELB",
                "environment": "no_env",
                "invalid_subnets": []
            },
            {
                "accout": None,
                "region": None,
                "load_blanacer_name": "LBDMZ",
                "load_balancer_name_tag": "TkimLB",
                "environment": "no_env",
                "invalid_subnets": []
            },
            {
                "accout": None,
                "region": None,
                "load_blanacer_name": "quaxo-elb",
                "load_balancer_name_tag": "TkimLB",
                "environment": "no_env",
                "invalid_subnets": ["subnet-b98cbc85"]
        }]
