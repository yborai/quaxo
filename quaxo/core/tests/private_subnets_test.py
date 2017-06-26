import os

from cement.utils import test

from ...__main__ import Stub as Quaxo
from ...cli.scanners.private_subnets import get_private_subnets

class Quaxo_(Quaxo):
    class Meta:
        argv = []

    @classmethod
    def assert_quaxo_success(cls, obj, args):
        with cls(argv=args) as app:
            with obj.assertRaises(SystemExit) as cm:
                app.run()
            obj.eq(cm.exception.code, 0, msg="Expected to return SystemExit: 0")

class TestQuaxo(test.CementTestCase):
    app_class = Quaxo_

    def setUp(self):
        with self.app_class() as app:
            log = app.log

    def tearDown(self):
        """
        Cement uses temp files in its default tests, and the references
        will not exist if setUp is overridden and will break when
        tearDown is called. A short-term fix is to override tearDown as
        well. The long-term fix will be to use CementTestCase more like
        the authors of Cement intended.
        """
        pass

    def test_private_subnets_help(self):
        Quaxo_.assert_quaxo_success(self, [
            "private-subnets", "--help"
        ])

    def test_get_private_subnets(self):
        subnets = ['subnet-d72c36ed', 'subnet-b98cbc85']
        vpcs =    ['vpc-88ac4bec', 'vpc-a31ca1c4']
        public_vpcs = ['vpc-88ac4bec']
        assert get_private_subnets(subnets, vpcs, public_vpcs) == ["subnet-b98cbc85"]