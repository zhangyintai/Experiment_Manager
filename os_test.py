import sys
import os
f1= 'z:/Users/Yintai Zhang/Research/ExperimentManger_Test_2/hello.py'
with open(f1,'r') as f:
    exec(f.read())
print("hello world!")