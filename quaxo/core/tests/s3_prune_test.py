from cement.utils import test

from ...cli.scanners.list_mp_uploads import get_stale_uploads
from ...cli.scanners.utils import get_stale_date
from .base import QuaxoRunner


class TestQuaxo(test.CementTestCase):

    def test_iam_check_help(self):
        QuaxoRunner.assert_quaxo_success(self, [
            "s3-prune", "--help"
        ])

    def test_no_uploads(self):
        assert get_stale_uploads([], 30) == "No uploads to report on"

    def test_get_stale_uploads(self):
        uploads = [
            {
                'UploadId': 'One',
                'Key': 'MajorKey',
                'Initiated': get_stale_date(31),
                'StorageClass': 'STANDARD',
                'Owner': {
                    'DisplayName': 'yborai',
                    'ID': 'CoolIDNum'
                },
                'Initiator': {
                    'ID': 'BigLebo2048',
                    'DisplayName': 'TheDude'
                }
            },
            {
                'UploadId': 'Two',
                'Key': 'MajorKey',
                'Initiated': get_stale_date(30),
                'StorageClass': 'STANDARD',
                'Owner': {
                    'DisplayName': 'yborai',
                    'ID': 'CoolIDNum'
                },
                'Initiator': {
                    'ID': 'BigLebo2048',
                    'DisplayName': 'TheDude'
                }
            },
            {
                'UploadId': 'Three',
                'Key': 'MajorKey',
                'Initiated': get_stale_date(29),
                'StorageClass': 'STANDARD',
                'Owner': {
                    'DisplayName': 'yborai',
                    'ID': 'CoolIDNum'
                },
                'Initiator': {
                    'ID': 'BigLebo2048',
                    'DisplayName': 'TheDude'
                }
            },
        ]

        assert len(get_stale_uploads(uploads, 30)) == 2