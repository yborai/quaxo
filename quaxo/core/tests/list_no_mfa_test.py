from cement.utils import test
import boto3

from ...cli.scanners.list_no_mfa import generate_report, get_users
from .base import QuaxoRunner


class TestQuaxo(test.CementTestCase):

    def test_list_no_mfa_help(self):
        QuaxoRunner.assert_quaxo_success(self, [
            "list-no-mfa", "--help"
        ])
