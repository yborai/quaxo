from cement.utils import test

from ...cli.scanners.get_parameters import get_parameters
from .base import QuaxoRunner


class TestQuaxo(test.CementTestCase):

    def test_describe_parameters_help(self):
        QuaxoRunner.assert_quaxo_success(self, [
            "describe-parameter", "--help"
        ])

    def test_wrong_key_input(self):
        filters = [
            {
                'Key' : 'InvalidFilterKey',
                'Values' : 'DasTestValue'
            }
        ]

        assert get_parameters(filters) == "Filter Key value not valid"
