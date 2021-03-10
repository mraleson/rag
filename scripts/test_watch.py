#!/usr/bin/env python3
import sys
from subprocess import call

if __name__ == "__main__":
    args = ' '.join(sys.argv[1:])
    cmd = f'poetry run env PYTHONPATH="/rag/tests" ptw --runner "pytest{" " if args else ""}{args}"'
    print(cmd)
    try:
        call(cmd, shell=True)
    except KeyboardInterrupt:
        pass
