
__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

import click


@click.group("document", help="Contains commands for writing data to a pycis document.")
def group_pycis_document():
    return


def add_groups_and_commands(parent: click.Group):

    from pycis.cli.cmdtree.document.build import add_groups_and_commands as build_add_groups_and_commands
    from pycis.cli.cmdtree.document.configuration import add_groups_and_commands as configuration_add_groups_and_commands
    from pycis.cli.cmdtree.document.testrun import add_groups_and_commands as testrun_add_groups_and_commands

    build_add_groups_and_commands(group_pycis_document)
    configuration_add_groups_and_commands(group_pycis_document)
    testrun_add_groups_and_commands(group_pycis_document)

    parent.add_command(group_pycis_document)

    return