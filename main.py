import pybind_exit_test as m
import threading
import time
import sys
import argparse
import os

parser = argparse.ArgumentParser(description='Pybind11 exit test')
parser.add_argument('api', choices=['pybind', 'capi'])


def test_pybind(pipe):
    m.read_pipe_pybind(pipe)

def test_capi(pipe):
    m.read_pipe_capi(pipe)

def main():
    print(f'Using {args.api}', file=sys.stderr)

    target = {
        'pybind': test_pybind,
        'capi': test_capi,
    }[args.api]

    r, w = os.pipe()

    # This test uses a deamon thread, but you can also get the same behavior
    # with a thread created by C/C++ calling through Python or with a
    # non-daemon thread and exit via ctrl-c.
    t = threading.Thread(target=target, args=(r,), daemon=True)
    t.start()

    # Create some cyclic garbage that will slow down the shutdown
    # process.
    class ClosePipeOnGC:
        def __del__(self):
            print("Shutting down...", file=sys.stderr)
            # close the pipe to trigger daemon thread exit
            os.close(w)
            time.sleep(0.05)

    g = ClosePipeOnGC()
    g.g = g
    del g

if __name__ == '__main__':
    args = parser.parse_args()
    main()