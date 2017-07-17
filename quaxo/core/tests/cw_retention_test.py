from cement.utils import test

from ...cli.scanners.cw_retentions import get_overrides
from .base import QuaxoRunner


class TestQuaxo(test.CementTestCase):

    def test_cw_retention_help(self):
        QuaxoRunner.assert_quaxo_success(self, [
            "list-overrides", "--help"
        ])
