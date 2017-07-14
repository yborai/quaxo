import sys
import datetime

import boto3
import pytz
from cement.core.controller import CementBaseController, expose
from .scanners.list_no_mfa import list_no_mfa
from .scanners.iam_check import list_wo_policy
from .scanners.private_subnets import PrivateSubnets
from .scanners.snap_methods import get_snaps
from .scanners.list_mp_uploads import list_mp_uploads
from .scanners.get_parameters import get_parameters


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

class AgedSnapshots(CLI):
    class Meta:
        label = "stale-snaps"
        description = "Returns all snapshots older than a specified #days(default: 30)"
        stacked_on = "base"
        stacked_type = "nested"
        arguments = CLI.Meta.arguments + [(
            ["--days"], dict(
                type=int,
                action="store",
                help="The number of days after which a snapshot is considered expired"
            )
        )]

    @expose(hide=True)
    def default(self):
        self.run(**vars(self.app.pargs))

    def run(self, **kwargs):
        self.app.log.info("Retrieving snapshots from AWS store")
        days = self.app.pargs.days

        final_snapshots = get_snaps(days)

        self.app.render(final_snapshots)

class MFAStatus(CLI):
    class Meta:
        label = "list-no-mfa"
        description = "Returns all users with admin permissions who do not have MFA active"
        stacked_on = "base"
        stacked_type = "nested"

    @expose(hide=True)
    def default(self):
        self.run(**vars(self.app.pargs))

    def run(self, **kwargs):
        self.app.log.info("Retrieving credentials from AWS store")

        admin_users = list_no_mfa()

        self.app.render(admin_users)

class IamCheck(CLI):
    class Meta:
        label = "iam-check"
        description = "Returns all users without specified Iam policies"
        stacked_on = "base"
        stacked_type = "nested"
        arguments = CLI.Meta.arguments + [(
            ["--policies"], dict(
                nargs='*',
                action="store",
                help="List of all policy ARNs to scan for(default: LogicworksAllClients)"
            )
        )]

    @expose(hide=True)
    def default(self):
        self.run(**vars(self.app.pargs))

    def run(self, **kwargs):
        self.app.log.info("Retrieving snapshots from AWS store")
        policies = self.app.pargs.policies

        response = list_wo_policy(policies)

        self.app.render(response)

class S3Prune(CLI):
    class Meta:
        label = "s3-prune"
        description = ("Returns all s3 multipart uploads older than a " 
           "specified #days(default: 30)"
        )
        stacked_on = "base"
        stacked_type = "nested"
        arguments = CLI.Meta.arguments + [(
            ["--days"], dict(
                type=int,
                action="store",
                help="The number of days after which an upload is considered expired"
            )
        )]

    @expose(hide=True)
    def default(self):
        self.run(**vars(self.app.pargs))

    def run(self, **kwargs):
        self.app.log.info("Retrieving Uploads from AWS store")
        days = self.app.pargs.days

        stale_mp_uploads = list_mp_uploads(days)

        self.app.render(stale_mp_uploads)

class PullParameters(CLI):
    class Meta:
        label = "describe-parameter"
        stacked_on = "base"
        stacked_type = "nested"
        description = "Gives list of parameters with information based on filter"
        arguments = CLI.Meta.arguments + [(
            ["-fk", "--fkey"], dict(
                required=True,
                action='store',
                help='The name of the filter(Name, KeyId, Type)'
            )
        ),
        (
            ["-fv", "--fvalue"], dict(
                required=True,
                nargs='+',
                action='store',
                help='List of filter values'
            )
        )]

    @expose(hide=True)
    def default(self):
        self.run(**vars(self.app.pargs))

    def run(self, **kwargs):
        filters = [
            {
                'Key' : self.app.pargs.fkey,
                'Values' : self.app.pargs.fvalue
            }
        ]
        response = get_parameters(filters)

        self.app.render(response)


__ALL__ = [
    CLI,
    AgedSnapshots,
    IamCheck,
    MFAStatus,
    PrivateSubnetsController,
    S3Prune,
    PullParameters
]

