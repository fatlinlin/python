"""
utilities for deploying environnements
"""
import os
import subprocess
import json
from xml.dom import minidom
import pysvn

modDir = os.path.dirname(__file__)

class Config:
    
    def __init__(self, path):
        self.path = path

    def get_connection_strings(self):
        config = minidom.parse(self.path)
        registry = config.getElementsByTagName("registry")[0]
        frontadmin = registry.getElementsByTagName("FrontAdmin")[0]
        connections_strings = frontadmin.getElementsByTagName("ConnectionStrings")[0]
        return connections_strings.firstChild.data.split("\n")

class Env:

    RSRC_PATH = "servers.json"
    with open(RSRC_PATH) as RSRC_FP:
        DATA = json.load(RSRC_FP)

    def __init__(self, env_name):
        self.params = self.DATA["env"][env_name]

    @property
    def config_path(self):
        return r"\\{server}\d$\{subfolder}\efront.config".format(**self.params)

    @property
    def config(self):
        return Config(self.config_path)

    def createUser(self):
        return {
            "name" : raw_input("choose a name:"),
            "login" : raw_input("choose a login:"),
            "password" : raw_input("choose a password:"),
            "connectionString" : choose(self.config.get_connection_strings())
            }

def choose(aList, msg=None):
    assert len(aList) > 0
    if msg is not None:
        print msg
    for i, elmt in enumerate(aList):
        print "{} - {}".format(i, elmt)
    while True:
        try:
            return aList[int(raw_input("choose a number between 0 and {}:".format(len(aList) - 1)))]
        except:
            pass
    
def deploy_env(env, path):
    # checkout
    svn = pysvn.Client()
    svn.checkout(env.params['repo'], path)

    # create efront.config
    confTemplateFp = open(os.path.join(modDir, "efront.config"))
    confTemplateStr = confTemplateFp.read()
    confTemplateFp.close()
    confPath = os.path.join(path, "website", "efront.config")
    confFp = open(confPath, "w")
    confFp.write(confTemplateStr.format(root=path, param=env.createUser()))
    confFp.close()

    # build env
    subprocess.check_call("Switch.cmd", cwd=path)
    subprocess.check_call("build_rt.bat", cwd=path)
    subprocess.check_call("msbuild_RSK.bat", cwd=path)
    
if __name__ == "__main__":
   env = Env("delta loyd")
   print choose(env.config.get_connection_strings())
