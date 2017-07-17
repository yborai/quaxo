from cement.utils import test

from ...__main__ import Quaxo


class QuaxoRunner(Quaxo):
    class Meta:
        argv = []

    @classmethod
    def assert_quaxo_success(cls, obj, args):
        with cls(argv=args) as app:
            with obj.assertRaises(SystemExit) as cm:
                app.run()
            obj.eq(
                cm.exception.code, 0, msg="Expected to return SystemExit: 0"
            )


class TestQuaxo(test.CementTestCase):
    app_class = QuaxoRunner

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
