import sys

from cement.core.controller import CementBaseController, expose
from .scanners.list_no_mfa import list_no_mfa
from .scanners.private_subnets import PrivateSubnets


class CLI(CementBaseController):
    class Meta:
        label = "base"
        description = "Quaxo CLI"
        arguments = CementBaseController.Meta.arguments

    @expose(hide=True)
    def default(self):
        self.app.args.print_help()
        sys.exit(0)

class PrivateSubnetsController(CLI):
    class Meta:
        label = "private-subnets"
        stacked_on = "base"
        stacked_type = "nested"
        description = "Returns the private associated attached to ELBs"

        arguments = CLI.Meta.arguments + [(
            ["--region"], dict(
                type=str,
                help="The AWS region on which to run the scanner."

            )
        ), 
        (
            ["--account"], dict(
                type=str,
                help="The AWS account on which to run the scanner."

            )
        )]
    @expose(hide=True)
    def default(self):
        self.run(**vars(self.app.pargs))

    def run(self, **kwargs):
        region = self.app.pargs.region
        account = self.app.pargs.account
        self.app.log.info(
            "scanning your ELBs on {account} in {region}"
            .format(account=account, region=region)
        )
        client = PrivateSubnets(region=region, account=account)
        subs = client.private_subnets()
        self.app.render(subs)
        return subs


__ALL__ = [CLI, PrivateSubnetsController]
