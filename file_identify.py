import argparse
import json

BYTE_READ = 30

# Try opening extensions.json, which should be in the databases directory
# Database found on: https://gist.github.com/seunlanlege/401898b5ca8486bd6685390cd87b1db4#file-extensions-json"
# Later edited to reflect more modern data
print("Getting extensions database...")
try:
    j = open('databases/extensions.json')
    jsn = json.load(j)
    j.close()
    print('Found the extensions.json database!')
except FileNotFoundError:
    print("\nERROR: extensions.json cannot be found! Please check if the file exists in the databases directory.\n")
    exit()

# Open a parser, which take the file name as input
parser = argparse.ArgumentParser(
    prog="file_identify.py",
    description="Python script used to read any file input (path to file may be used) and identify the intended filetype." \
    "The use case for this script is for files that have an extension that does not work for what the data holds.")
parser.add_argument('file_name')
args = parser.parse_args()

# Try opening the file the user inputted in as an argument
print(f"Finding user inputted file ({args.file_name})...")
try:
    f = open(args.file_name, 'rb')
    print('Found the file!')
except FileNotFoundError:
    print("\nERROR: File cannot be found! Please check if the file exists or the path to the file is correct.\n")
    exit()
except Exception as e:
    print(f"\nERROR: An unknown exception has occured: {e}")
    exit()

bytes = f.read(BYTE_READ)
bytes_formatted = ""
for byte in bytes:
    # print(f"{int(byte):02x}", end= " ")
    bytes_formatted += f"{int(byte):02x}".upper()
print(f"Bytes found: {bytes_formatted}")

for file_type in jsn:
    for sign in jsn[file_type]["signs"]:
        curr_offset, curr_sign = sign.split(",")
        if curr_sign == bytes_formatted[int(curr_offset): int(curr_offset) + len(curr_sign)]:
            print(f"{file_type}")
            print(f"\tMime: {jsn[file_type]["mime"]}")
            print(f"\tSignature: {curr_sign}")
            print(f"\tOffset: {curr_offset}")

f.close()
print("Program has finished.")