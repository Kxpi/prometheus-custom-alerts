# prometheus-alert-labels
Python script for adding new custom labeled Prometheus alerts based on alredy existing, default alerts from Alert Manager. Additional labels allow better routing when configuring alerts using webhooks. The default ones can't be mutated (can't have labels added) as they are provisioned by Alert Manager. Supposedly there is a way to do it with [Gatekeeper](https://open-policy-agent.github.io/gatekeeper/website/docs/mutation) but I didn't succeed doing so. 

## Usage
```
$ python3 main.py --help
usage: main.py [-h] --label --value [--file] [--json-file] [--output] [--apply]

Required arguments:
  --label, -l      Label name used for alert routing.
  --value, -v      Value for a given label.
  --file, -f       Path to file with alert names that you want to "customize".

Optional arguments:
  --json-file, -j  Path to json file with Prometheus rules dump.
  --output, -o     Path to where should custom rules be saved.
  --apply, -a          Specifies if to apply changes by executing "oc apply -f <filename>".
```
## Notes
Scirpt assumes certain things in JSON structure so for example dumped rules should be obtained by running:
```
oc get promrule [ -n <namespace> | -A ] -o json > rules.json
```
