# Author: Marcel Schneider

from os import fork, pipe, _exit, wait, fdopen, getenv, close
from pickle import dump, load
from multiprocessing import cpu_count

# compared to multiprocessing.Pool.map, this simple implementation is
# - less memory hungry (no copying of input data)
# - less cpu-wasting (no pickling of input data)
# but:
# - more constant overhead: forks per call
# - no real scheduling, simply divides work in the beginning.

def pmap(func, args):
    n = len(args)
    ncpu = int(getenv("NPROCS", cpu_count()))
    block = int(n / ncpu)
    pipes = []
    for i in range(0, ncpu):
        start = i*block
        end = (i+1)*block
        if i == (ncpu-1):
            end = n

        (r, w) = pipe()
        pid = fork()
        if pid == 0: # child
            out = list(map(func, args[start:end]))
            with fdopen(w, 'wb') as f:
                dump(out, f)
            _exit(0)
        # parent 
        pipes.append(r)
        close(w)
    out = []
    fail = False
    for i, p in enumerate(pipes):
        #print("Waiting for %d..." % i)
        try:
            with fdopen(p, 'rb') as f:
                res = load(f)
                out = out + res
        except:
            print("load failed, output incomplete")
            fail = True
        (pid, status) = wait()
        if status != 0:
          print("Child failed! (%d, %d, %d)" % (pid, status / 256, status % 256))
          fail = True
    if fail:
      raise Exception("pmap failed!")
    return out

if __name__ == '__main__':
    ns = list(range(0, 9))
    res = pmap(lambda x: x-1, ns)
    print(res)

        



