import os 
import shutil
import argparse

args = argparse.ArgumentParser()
args.add_argument('-i', help="input directory")
args = args.parse_args()

for file in os.listdir(args.i):
    src = os.path.join(args.i, file)
    dst = os.path.join(args.i, f"copy_{file}")
    shutil.copy(src, dst)