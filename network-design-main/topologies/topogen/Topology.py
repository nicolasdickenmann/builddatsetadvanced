# Author: Alessandro Maissen

class Topology:

    p = None
    r = None
    nr = None
    R = None
    N = None
    edge = None
    __topo = None
    name = None

    def __init___(self, **kwargs): 
        raise NotImplementedError
    
    def get_topo(self):
        raise NotImplementedError
    
    def get_jellyfish_eq(self):
        raise NotImplementedError

    def get_info(self):
        return "name=%s p=%d net-radix=%d radix=%d R=%d N=%d" %(self.name, self.p, self.nr, self.r, self.R, self.N)