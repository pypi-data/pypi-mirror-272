import os
import sys

thingy_path = os.path.dirname(os.path.realpath(__file__))
print(f'<<<{thingy_path}')
sys.path.append(thingy_path)
