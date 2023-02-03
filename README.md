# prometheus-alert-labels
Python script for adding labels to Prometheus alerts definitions. Additional labels allow better routing when configuring alerts using webhooks.

## Usage
```
$ python3 main.py --help
usage: main.py [-h] --label --value --file [--json-file] [--output] [--apply]

Required arguments:
  --label, -l      Label name used for alert routing.
  --value, -v      Value for a given label.
  --file, -f       Path to file with alert names.

Optional arguments:
  --json-file, -j  Path to json file with Prometheus rules dump.
  --output, -o     Path to where should updated rules be saved.
  --apply, -a          Specifies if to apply changes by executing "oc apply -f <filename>".
```
