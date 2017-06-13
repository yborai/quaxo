import sys

from cement.core.controller import CementBaseController, expose


class CLI(CementBaseController):
    class Meta:
        label = "base"
        description = "Quaxo CLI"
        arguments = CementBaseController.Meta.arguments

    @expose(hide=True)
    def default(self):
        self.app.args.print_help()
        sys.exit(0)


__ALL__ = [CLI]
