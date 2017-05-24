import yaml
import os

with open(os.path.dirname(os.path.realpath(__file__)) + '/config.yml') as yamlfile:
    cfg = yaml.load(yamlfile)
    cfg_mongo = cfg['mongo']
