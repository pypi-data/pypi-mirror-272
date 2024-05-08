
__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

import click

def add_groups_and_commands(parent: click.Group):
    
    from pycis.cli.cmdtree.datastore import add_groups_and_commands as datastore_add_groups_and_commands
    from pycis.cli.cmdtree.document import add_groups_and_commands as document_add_groups_and_commands
    from pycis.cli.cmdtree.tracking import add_groups_and_commands as tracking_add_groups_and_commands

    datastore_add_groups_and_commands(parent)
    document_add_groups_and_commands(parent)
    tracking_add_groups_and_commands(parent)

    return
