#!/usr/bin/env python3
import sys
import json
import argparse
import subprocess


def parse_args() -> dict:
    """
    Parses arguments from CLI and returns them as dict
    """
    parser = argparse.ArgumentParser(description=argparse.SUPPRESS)
    parser._action_groups.pop()
    required = parser.add_argument_group('Required arguments')
    optional = parser.add_argument_group('Optional arguments')
    required.add_argument('--label', '-l', type = str, metavar = '\b', required = True, help = 'Label name used for alert routing.')
    required.add_argument('--value', '-v', type = str, metavar = '\b', required = True, help = 'Value for a given label.')
    required.add_argument('--file', '-f', type = str, metavar = '\b', required = True, help = 'Path to file with alert names.')
    optional.add_argument('--json-file', '-j', type = str, metavar = '\b', help = 'Path to json file with Prometheus rules dump.')
    optional.add_argument('--output', '-o', type = str, default="updated_prom_rules.json", metavar = '\b', help = 'Path to where should updated rules be saved.')
    optional.add_argument('--apply', '-a', action = 'store_true', help = 'Specifies if to apply changes by executing "oc apply -f <filename>".')

    args = vars(parser.parse_args())
    
    return args


def read_alerts(args: dict) -> list:
    """
    Reads json with alert names and returns it as dict
    """
    try:
        alerts = [line.strip() for line in open(args['file'], 'r')]
    except FileNotFoundError:
        sys.exit('File with alert names not found')

    return alerts


def read_rules(args: dict) -> dict:
    """
    Reads json with prometheus alert rules and returns it as dict
    """
    try:
        with open(args['json'], 'r') as json_rules:
            rules = json.load(json_rules)
    except ValueError:
        sys.exit('Exiting read - wrong JSON')
    except FileNotFoundError:
        sys.exit('File with rules not found')

    return rules


def get_rules() -> dict:
    """
    Executes command as subprocess to get json with Prometheus rules definitions in JSON
    """
    result = subprocess.run(['oc', 'get', 'promrule', '-A', '-o', 'json'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    result_json = json.loads(result)
    return result_json


def save_rules(updated_rules: dict, args: dict):
    """
    Saves updated rules to a new file called 'updated_rules.json'
    """
    with open(args['output'], 'w') as new_rules:
        json.dump(updated_rules, new_rules, indent = 4)


def apply_rules(args: dict):
    """
    Applies file with updated rules using oc apply
    """
    subprocess.run(['oc', 'apply', '-f', args['output']])


def add_new_labels(rules_json: dict, args: dict, alerts: list):
    """
    Applies new specified labels to exisitng alerts
    """
    item_index = 0 # keeps track of index of current item in top-level array

    for item in rules_json['items']:
        group_index = 0 # keeps track of index of current group
        for group in item['spec']['groups']:
            rule_index = 0 # keeps track of index of current rule
            for rule in group['rules']:
                try:
                    if rule['alert'] in alerts:
                        # items[x][spec][groups][y][rules][z][labels][LABEL]: VALUE
                        rules_json['items'][item_index]['spec']['groups'][group_index]['rules'][rule_index]['labels'][args['label']] = args['value']
                except KeyError:
                    pass
                rule_index += 1
            group_index += 1
        item_index += 1

    save_rules(rules_json)

    if args['apply']:
        apply_rules(args)


if __name__ == '__main__':
    """
    Main function
    """
    args = parse_args() # parse arguments from cli
    
    if args['file'] is None:
       rules_json = get_rules(args) # get alerts from oc output
    else:
        rules_json = read_rules(args) # read alert rules data from json file

    alerts = read_alerts(args) # read names of alert that are supposed to be labeled

    add_new_labels(rules_json, args) # add labels to rules declarations and save
