import datetime

from cement.utils import test
import pytz

from ...cli.scanners.utils import get_stale_date
from .base import QuaxoRunner


class TestQuaxo(test.CementTestCase):

    def test_stale_snapshots_help(self):
        QuaxoRunner.assert_quaxo_success(self, [
            "stale-snaps", "--help"
        ])

    def test_get_stale_date(self):
        test_date = datetime.datetime.now(pytz.UTC) - datetime.timedelta(days=365)

        assert test_date.day == get_stale_date(365).day

    def test_stale_snaps_default(self):
        test_date = datetime.datetime.now(pytz.UTC) - datetime.timedelta(days=30)

        assert test_date.day == get_stale_date(None).day
