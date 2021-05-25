import argparse
import os

args = argparse.ArgumentParser()
args.add_argument("-i", help="input folder")
args.add_argument("-map", help="mapping from command to command id")
args.add_argument("-lumimap", help="mapping from command to command id for ok lumi")
args.add_argument("-o", help="folder to output annotation")
args.add_argument("-q", action="store_true", help="annotate quang's data")
args = args.parse_args()

def parse_command_mapping(infile):
    if infile is None:
        return None
    with open(infile) as f:
        lines = f.readlines()
    mapping = {}
    for line in lines:
        line = line.strip()
        if len(line) == 0: continue
        command, id = line.split("</s>")
        id = id.strip()
        id = id.split("_")[-1]
        id = id.replace(")", "")
        command = command.strip() + " </s>"
        mapping[id] = command
    return mapping

def get_command_id(filename):
    name, ext = filename.split(".")
    id = name.split("_")[-1]
    return id

def has_enough_files(person_dir):
    required_commands = sorted([f"l{i}" for i in range(1, 56)])
    commands = []
    for file in os.listdir(person_dir):
        ext = file.split(".")[-1]
        if ext != "wav": continue
        commands.append(get_command_id(file))
    commands = sorted(commands)
    if commands != required_commands:
        req_cmd_set = set(required_commands)
        cmd_set = set(commands)
        print(f"{person_dir} doesn't have enough files")
        print(req_cmd_set.difference(cmd_set) | cmd_set.difference(req_cmd_set))
    return commands == required_commands

transcript = []
file_ids = []

os.makedirs(args.o, exist_ok=True)
cmd_mapping = parse_command_mapping(args.map)
cmd_mapping_lumi = parse_command_mapping(args.lumimap)
print(cmd_mapping)
print(cmd_mapping_lumi)
for region in os.listdir(args.i):
    region_dir = os.path.join(args.i, region)
    if not os.path.isdir(region_dir): continue
    for distance in os.listdir(region_dir):
        distance_dir = os.path.join(region_dir, distance)
        if not os.path.isdir(distance_dir): continue
        for person in os.listdir(distance_dir):
            person_dir = os.path.join(distance_dir, person)
            if not os.path.isdir(person_dir): continue
            has_enough_files(person_dir)
            for file in os.listdir(person_dir):
                ext = file.split(".")[1]
                if ext != "wav": continue
                file_id, ext = file.split(".")
                if args.q:
                    cmd = " ".join(person.split("_"))
                    cmd = f"<s> {cmd} </s>"
                else:
                    cmd_id = get_command_id(file)
                    if "ok_lumi" in region:
                        cmd = cmd_mapping_lumi.get(cmd_id)
                    else:
                        cmd = cmd_mapping.get(cmd_id)
                if cmd is None: continue
                file_id = os.path.join(person_dir, file_id)
                transcript.append(f"{cmd} ({file_id})\n")
                file_ids.append(f"{file_id}\n")

with open(os.path.join(args.o, "anno.transcription"), "w") as f:
    f.writelines(transcript)
with open(os.path.join(args.o, "anno.fileids"), "w") as f:
    f.writelines(file_ids)