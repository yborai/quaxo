from cement.utils import test

from ...cli.scanners.private_subnets import get_private_subnets
from .base import QuaxoRunner


class TestQuaxo(test.CementTestCase):

    def test_private_subnets_help(self):
        QuaxoRunner.assert_quaxo_success(self, [
            "private-subnets", "--help"
        ])

    def test_get_private_subnets(self):
        subnets = ['subnet-d72c36ed', 'subnet-b98cbc85']
        vpcs = ['vpc-88ac4bec', 'vpc-a31ca1c4']
        public_vpcs = ['vpc-88ac4bec']
        assert get_private_subnets(subnets, vpcs, public_vpcs) == ["subnet-b98cbc85"]
