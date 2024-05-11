import yaml
def LoadCFG(cfg_file):
    confg = yaml.load(cfg_file, Loader=yaml.FullLoader)
    return confg