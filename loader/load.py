from argparse import ArgumentParser
from pathlib import Path
import sys
import json
from pprint import pprint
import os

import neo4j
import jsonschema


CONFIG_SCHEMA_FILENAME = os.environ.get('CONFIG_SCHEMA', 'config.schema.json')

def load_config(filename):
    if not Path(filename).exists():
        print(f'ERROR: Specified JSON configuration file ({filename}) does not exist')
        sys.exit(1)

    if not Path(CONFIG_SCHEMA_FILENAME).exists():
        print(f'ERROR: Required json schema file does not exists ({CONFIG_SCHEMA_FILENAME})')
        sys.exit(1)

    with open(args.config) as f:
        config = json.load(f)

    with open(CONFIG_SCHEMA_FILENAME) as f:
        schema = json.load(f)

    try:
        jsonschema.validate(instance=config, schema=schema)
    except jsonschema.exceptions.SchemaError as e:
        print('Loaded schema (invalid):')
        pprint(schema)
        raise e
    except jsonschema.exceptions.ValidationError as e:
        print('Loaded config (invalid):')
        pprint(config)
        raise e

    return config

def add_vm_trans(tx, id, name, tags):
    tx.run("CREATE(vm:VM{id: $id, name: $name, tags: $tags})", id=id, name=name, tags=tags)

def add_rule_trans(tx, id, src_tag, dst_tag):
    id = id.replace('-', '_')
    tx.run(f"MATCH(s:VM), (d:VM) WHERE $src_tag in s.tags AND $dst_tag in d.tags AND s.id <> d.id CREATE (s)-[r:{id}]->(d)", src_tag=src_tag, dst_tag=dst_tag)

def clean_trans(tx):
    tx.run('MATCH(n) DETACH DELETE n')

if __name__ == '__main__':
    parser = ArgumentParser('VMs configuration loader')
    parser.add_argument('config', help='JSON file with VMs config')
    parser.add_argument('--neo-uri', default='neo4j:localhost', help='NEO4J database uri')
    parser.add_argument('--clean', action='store_true', default=False, help='Clean database before load')
    args = parser.parse_args()

    config = load_config(args.config)

    driver = neo4j.GraphDatabase.driver(args.neo_uri)
    with driver.session() as s:
        if args.clean:
            s.write_transaction(clean_trans)

        for vm in config['vms']:
            s.write_transaction(add_vm_trans, vm['vm_id'], vm['name'], vm['tags'])

        for rule in config['fw_rules']:
            s.write_transaction(add_rule_trans, rule['fw_id'], rule['source_tag'], rule['dest_tag']) 
