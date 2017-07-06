from cement.utils import test

from ...cli.scanners.iam_check import list_wo_policy
from .base import QuaxoRunner


class TestQuaxo(test.CementTestCase):

    def test_iam_check_help(self):
        QuaxoRunner.assert_quaxo_success(self, [
            "iam-check", "--help"
        ])

    def test_iam_default(self):
        assert not(list_wo_policy(None) == None)
