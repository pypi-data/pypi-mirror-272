
__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

import click


@click.group("couchdb", help="Contains commands datastore test results to CouchDB.")
def group_pycis_datastore_couchdb():
    return

def add_groups_and_commands(parent: click.Group):
    
    from pycis.cli.cmdtree.datastore.couchdb.initialize import add_groups_and_commands as initialize_add_groups_and_commands
    from pycis.cli.cmdtree.datastore.couchdb.publish import add_groups_and_commands as publish_add_groups_and_commands

    # Call to child groups to add themselfs to this group
    initialize_add_groups_and_commands(group_pycis_datastore_couchdb)
    publish_add_groups_and_commands(group_pycis_datastore_couchdb)

    # Add this group to its parent
    parent.add_command(group_pycis_datastore_couchdb)

    
    return