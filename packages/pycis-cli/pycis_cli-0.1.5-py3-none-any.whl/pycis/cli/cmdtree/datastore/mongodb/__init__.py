
__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

import click

from pycis.cli.cmdtree.datastore.mongodb.publish import command_pycis_datastore_mongodb_publish


@click.group("mongodb", help="Contains commands datastore test results to MongoDB.")
def group_pycis_datastore_mongodb():
    return

group_pycis_datastore_mongodb.add_command(command_pycis_datastore_mongodb_publish)

def add_groups_and_commands(parent: click.Group):
    
    from pycis.cli.cmdtree.datastore.mongodb.publish import add_groups_and_commands as publish_add_groups_and_commands

    # Call to child groups to add themselfs to this group
    publish_add_groups_and_commands(group_pycis_datastore_mongodb)

    # Add this group to its parent
    parent.add_command(group_pycis_datastore_mongodb)

    
    return