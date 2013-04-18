import os
import iohelpers as io
import repo

class Builder:

    build_dir = repo.DEV_DIR

    def __init__(self, user):
        self.user = user

    def setupVSEnvironment(self):
        io.cmd(["FrontBuild\vsimportconfig.bat", "vs2008"])

    def switch(self):
        pass
