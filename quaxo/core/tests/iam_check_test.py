from cement.utils import test

from ...cli.scanners.iam_check import list_wo_policy
from .base import QuaxoRunner


class TestQuaxo(test.CementTestCase):

    def test_iam_check_help(self):
        QuaxoRunner.assert_quaxo_success(self, [
            "iam-check", "--help"
        ])
