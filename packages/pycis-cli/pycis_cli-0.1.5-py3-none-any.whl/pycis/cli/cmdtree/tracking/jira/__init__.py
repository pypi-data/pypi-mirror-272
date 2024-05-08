
__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

from typing import Optional, Union

from dataclasses import dataclass

import click

from mojo.xmods.xclick import NORMALIZED_STRING

from mojo.credentials.apitokencredential import ApiTokenCredential
from mojo.credentials.personalapitokencredential import PersonalApiTokenCredential
from mojo.credentials.basiccredential import BasicCredential

from jira import JIRA

@dataclass
class JiraConnectionContext:
    jclient: JIRA
    credential: Optional[Union[ApiTokenCredential, BasicCredential, PersonalApiTokenCredential]] = None


HELP_JIRA = "The Jira host to connect with."
HELP_CREDENTIAL_SOURCE = "The source location of a credential catalog."
HELP_CREDENTIAL = "The name of a Jira credential to use from the specified credential catalog."

@click.group("jira", help="Contains commands for interoperating with Jira tracking software and services.")
@click.option("--jira", "jirahost", required=True, type=NORMALIZED_STRING, help=HELP_JIRA)
@click.option("--credential", required=False, type=NORMALIZED_STRING, help=HELP_CREDENTIAL)
@click.option("--credential-source", required=False, default=None, type=NORMALIZED_STRING, help=HELP_CREDENTIAL_SOURCE)
@click.pass_context
def group_pycis_tracking_jira(ctx: click.Context, jirahost: str, credential: str, credential_source: Union[str, None]):

    jiracred = None

    if credential is not None:
        from mojo.config.optionoverrides import MOJO_CONFIG_OPTION_OVERRIDES
        from mojo.config.configurationmaps import resolve_configuration_maps

        if credential_source is not None:
            MOJO_CONFIG_OPTION_OVERRIDES.override_config_credentials_files([credential_source])

        resolve_configuration_maps(use_credentials=True, use_landscape=False, use_topology=False, use_runtime=False)

        from mojo.config.wellknown import CredentialManagerSingleton

        credmgr = CredentialManagerSingleton()

        jiracred: Union[ApiTokenCredential, BasicCredential] = credmgr.lookup_credential(credential)
    
    jclient = None
    
    if jiracred is None:
        jclient = JIRA(jirahost)
    elif isinstance(jiracred, BasicCredential):
        jclient = JIRA(jirahost, basic_auth=(jiracred.username, jiracred.password))
    elif isinstance(jiracred, PersonalApiTokenCredential):
        jclient = JIRA(jirahost, basic_auth=(jiracred.username, jiracred.token))
    elif isinstance(jiracred, ApiTokenCredential):
        jclient = JIRA(jirahost, token_auth=jiracred.token)
    else:
        errmsg = f"Un-Supported credential type={type(jiracred)}"
        raise ValueError(errmsg)

    ctx.obj = JiraConnectionContext(jclient, jiracred)

    return


def add_groups_and_commands(parent: click.Group):

    from pycis.cli.cmdtree.tracking.jira.comment import command_pycis_tracking_jira_comment

    group_pycis_tracking_jira.add_command(command_pycis_tracking_jira_comment)

    parent.add_command(group_pycis_tracking_jira)

    return