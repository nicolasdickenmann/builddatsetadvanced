from os import makedirs, path

class Analysis:

    datafilefolder = "data/analysis/"

    def __init__(self):
        if not path.exists(self.datafilefolder):
            makedirs(self.datafilefolder)

    def analyse(self, **kwargs):
        raise NotImplementedError

