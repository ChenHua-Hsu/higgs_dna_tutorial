import os
import json
import argparse

# Function to scan directories and create JSON structure
def create_json_from_directory_structure(base_path):
    data = {}
    for root, dirs, files in os.walk(base_path):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            root_files = [f for f in os.listdir(dir_path) if f.endswith('.root')]
            if root_files:
                data[dir_name] = [os.path.join(dir_path, f) for f in root_files]
    return data

# Main function to parse arguments and execute the JSON creation
def main():
    parser = argparse.ArgumentParser(description='Create JSON from directory structure')
    parser.add_argument('directory_path', type=str, help='Path to the base directory')
    parser.add_argument('output_json_path', type=str, help='Path to the output JSON file')

    args = parser.parse_args()

    data = create_json_from_directory_structure(args.directory_path)

    with open(args.output_json_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"JSON file saved to {args.output_json_path}")

if __name__ == '__main__':
    main()