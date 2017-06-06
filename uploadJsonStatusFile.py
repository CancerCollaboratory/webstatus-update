import yaml
import json
import sys
import jsonschema
from jsonschema import SchemaError, ValidationError
from os import popen

def main(config="config.yaml"):
    """
    Create a json file from 3 yaml files, validate it against a JSON schema, and scp it to a server if it has changed.

    :param config: A yaml config file
    :return: None
    """
    c=readYaml(config)

    d=readYaml(c['notifications_file'])
    d2=readYaml(c['resources_file'])
    d3=readYaml(c['status_file'])

    d.update(d2)
    d.update(d3)

    schema = readJson(c['schema_file'])
    try:
        jsonschema.validate(d,schema)
    except SchemaError as e:
        print("Schema has errors: {}".format(e))
        return
    except ValidationError as e2:
        print("Validation error: {}".format(e2))
        return

    j = json.dumps(d)

    try:
        currentJson = readFile(c['json_file'])
    except FileNotFoundError:
        currentJson = "{}"
    if currentJson != j:
        writeFile(c['json_file'], j)
        status=popen(fmt("echo scp {} {}:{}/{}", c['json_file'], c['host'], c['path'], c['remote_json_file']))
        print(list(status))
    else:
        print("Json file '{}' is unchanged; no need to remotely update".format(c['json_file']))

def printf(str, *args, **kw):
    print(fmt(str,*args,**kw))

def fmt(str, *args, **kw):
    return str.format(*args, **kw)

def writeFile(name, data):
    with open(name,"w") as h:
        h.write(data)

def readYaml(name):
    with open(name) as h:
        return yaml.load(h)

def readJson(name):
    with open(name) as h:
        return json.load(h)


def readFile(name):
    with open(name) as h:
        return h.read()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        main()
    else:
        main(sys.argv[1])
