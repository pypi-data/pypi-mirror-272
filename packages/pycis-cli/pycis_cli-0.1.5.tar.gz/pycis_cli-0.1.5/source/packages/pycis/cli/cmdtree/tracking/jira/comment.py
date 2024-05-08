__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

from typing import List, Union, TYPE_CHECKING

import os
import sys

from http import HTTPStatus

import click
import requests

from mojo.credentials.apitokencredential import ApiTokenCredential
from mojo.credentials.personalapitokencredential import PersonalApiTokenCredential
from mojo.credentials.basiccredential import BasicCredential

from mojo.xmods.xclick import NORMALIZED_STRING

from jira import JIRA, Issue

if TYPE_CHECKING:
    from pycis.cli.cmdtree.tracking.jira import JiraConnectionContext

HELP_JQL = "A Jira Query String that is used to limit the effect Jira tickets."
HELP_LIMIT = "Limit the number of issues that can be modified by the command."
HELP_COMMENT = "A comment to append to the select Jira tickets. (must be specified if '--comment-source' is not passed)"
HELP_COMMENT_SOURCE = "A source path specifying where to get comment contents.  (must be specified if '--comment' is not passed)"

@click.command("comment")
@click.option("--jql", "jql", required=True, multiple=True, type=NORMALIZED_STRING, help=HELP_JQL)
@click.option("--comment", required=False, type=NORMALIZED_STRING, help=HELP_COMMENT)
@click.option("--comment-source", required=False, type=NORMALIZED_STRING, help=HELP_COMMENT_SOURCE)
@click.option("--limit", required=False, default=1, help=HELP_LIMIT)
@click.pass_context
def command_pycis_tracking_jira_comment(ctx: click.Context, jql: List[str], comment: Union[str, None], comment_source: Union[str, None], limit: bool):
    
    if ctx.obj is None:
        errmsg = "Something bad happend, we should always have a JiraConectionContext."
        raise RuntimeError(errmsg)

    if comment is None and comment_source is None:
        errmsg = "You must ONLY specify either the 'comment' or 'comment-source' option."
        raise click.BadOptionUsage(errmsg)
    
    if comment is not None and comment_source is not None:
        errmsg = "You must ONLY specify either the 'comment' or 'comment-source' option.  You cannot use both."
        raise click.BadOptionUsage(errmsg)

    if comment_source is not None:
        if comment_source.startswith("http:") or comment_source.startswith("https:"):
            resp = requests.get(comment_source)
            if resp.status_code == HTTPStatus.OK:
                comment = resp.content
            else:
                errmsg_lines = [
                    f"Invalid comment source specified. url={comment_source}",
                    f"STATUS CODE: {resp.status_code}",
                    f"CONTENT:"
                ]
                errmsg_lines.append(resp.content)

                errmsg = os.linesep.join(errmsg_lines)
                
                raise click.BadParameter(errmsg)
        else:
            with open(comment_source, 'r') as cs:
                comment = cs.read()

    jiractx: "JiraConnectionContext" = ctx.obj

    jclient: JIRA = jiractx.jclient

    issues_found = jclient.search_issues(jql_str=jql)
    if len(issues_found) > 0:
        if len(issues_found) > limit:
            print(f"The number of issues found exceeded the modify limit. limit={limit} found={len(issues_found)}", file=sys.stderr)
            exit(1)

        issue: Issue
        for issue in issues_found:
            jclient.add_comment(issue, comment)

    else:
        print("No issues found.", file=sys.stderr)
        exit(1)

    return
