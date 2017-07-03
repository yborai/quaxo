import sys

from cement.core.controller import CementBaseController, expose
from .scanners.list_no_mfa import list_no_mfa
from .scanners.private_subnets import private_subnets


class CLI(CementBaseController):
    class Meta:
        label = "base"
        description = "Quaxo CLI"
        arguments = CementBaseController.Meta.arguments

    @expose(hide=True)
    def default(self):
        self.app.args.print_help()
        sys.exit(0)

    @expose(help="List all private subnets associated with elbs")
    def private_subnets(self):
        priv_subs = private_subnets()
        self.app.render(priv_subs)

    @expose(help=(
        "Lists all users with admin level permissions that do not "
        "have multifactor authentication"
    ))
    def list_no_mfa(self):
        response = list_no_mfa()

        self.app.render(response)

__ALL__ = [CLI]
