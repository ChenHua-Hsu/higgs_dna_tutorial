import json
import subprocess
import argparse

## Example usage
# python copy_files_from_json_w_xrd.py ../04_base_processor/configs/04_samples.json DataC_2022 3 /eos/cms/store/group/phys_higgs/cmshgg/tutorials/HiggsDNA_2024/04_base_processor/DataC_2022
## Only works with active grid proxy

# Function to execute the xrdcp command
def execute_xrdcp_command(xrd_string, destination):
    command = f"xrdcp {xrd_string} {destination}"
    print(f"Executing: {command}")
    subprocess.run(command, shell=True)

# Function to read JSON and execute xrdcp commands
def copy_files_from_json(json_file_path, key, num_files, destination):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    if key in data:
        xrd_strings = data[key][:num_files]  # Get the specified number of xrd strings
        for xrd_string in xrd_strings:
            execute_xrdcp_command(xrd_string, destination)
    else:
        print(f"Key '{key}' not found in the JSON file")

# Main function to parse arguments and execute the copy process
def main():
    parser = argparse.ArgumentParser(description='Copy files from a JSON list using xrdcp')
    parser.add_argument('json_file_path', type=str, help='Path to the JSON file')
    parser.add_argument('key', type=str, help='Key in the JSON file to retrieve the list of xrd strings')
    parser.add_argument('num_files', type=int, help='Number of files to copy')
    parser.add_argument('destination', type=str, help='Destination directory for the copied files')

    args = parser.parse_args()

    copy_files_from_json(args.json_file_path, args.key, args.num_files, args.destination)

if __name__ == '__main__':
    main()