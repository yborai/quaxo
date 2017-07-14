from cement.utils import test

from ...cli.scanners.private_subnets import PrivateSubnets
from .base import QuaxoRunner


class TestQuaxo(test.CementTestCase):

    def test_private_subnets_help(self):
        QuaxoRunner.assert_quaxo_success(self, [
            "private-subnets", "--help"
        ])
