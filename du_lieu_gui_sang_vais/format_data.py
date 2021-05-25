import argparse
import os
import shutil
import copy
import re

args = argparse.ArgumentParser()
args.add_argument("-i", help="input directory")
args.add_argument("-o", help="output directory")
args.add_argument('-lumi', action='store_true')
args = args.parse_args()
    


def format_person(person_dir, out_person_dir, lumi=False):
    os.makedirs(out_person_dir, exist_ok=True)
    if lumi:
        for file in os.listdir(person_dir):
            if not os.path.isdir(os.path.join(person_dir, file)): continue 
            if file in ["ok", "lumi", "ok lumi"]:
                format_person(os.path.join(person_dir, file), out_person_dir)
    else:
        for command in os.listdir(person_dir):
            ori_command = copy.copy(command)
            command = command.split(".")
            ext = command[-1]
            if ext != "wav": continue
            command = command[0].replace("-", "_")
            command = command.split("_")
            command[0] = command[0][:2]
            command[1] = command[1].strip().lower()
            command[1] = re.sub('[()l]', '', command[1])
            command = command[0] + "_l" + command[1] + "." + ext
            shutil.copy(os.path.join(person_dir, ori_command), os.path.join(out_person_dir, command))


input_dir = args.i
output_dir = args.o
os.makedirs(output_dir, exist_ok=True)
for distance in os.listdir(input_dir):
    distance_dir = os.path.join(input_dir, distance)
    if not os.path.isdir(distance_dir): continue
    distance_dir_out = os.path.join(output_dir, distance)
    os.makedirs(distance_dir_out, exist_ok=True)
    if not os.path.isdir(distance_dir): continue
    for person in os.listdir(distance_dir):
        person_dir = os.path.join(distance_dir, person)
        if not os.path.isdir(person_dir): continue
        ori_person = copy.copy(person)
        person = person.split()
        if len(person) > 1:
            person[1] = re.sub('[()]', '', person[1])
        person = "".join(person)
        person_dir_out = os.path.join(distance_dir_out, person)
        format_person(person_dir, person_dir_out, args.lumi)
        # print(person)
        # shutil.copy(person_dir, person_dir_out)


    

