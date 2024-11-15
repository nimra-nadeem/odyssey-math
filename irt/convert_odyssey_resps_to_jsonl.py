import json
import os
import glob

def load_data(data_filepath):
    with open(data_filepath, "r") as f:
        samples = json.load(f)
    return samples

def convert_json_to_jsonl(input_file, output_file):
    data = load_data(input_file)

    with open(output_file, "w") as outfile:
        for entry in data:
            for problem_id, content in entry.items():
                jsonl_entry = {"problem_id": problem_id, **content}
                json.dump(jsonl_entry, outfile)
                outfile.write("\n")
    
    print(f"Converted {input_file} to {output_file}")

def main():
    output_dir = "jsonl/"
    input_dir = "json/"

    input_files = glob.glob(os.path.join(input_dir, "*_odyssey.json"))
    
    for input_file in input_files:
        filename = os.path.basename(input_file).replace(".json", ".jsonl")
        output_file = os.path.join(output_dir, filename)

        convert_json_to_jsonl(input_file, output_file)

if __name__ == "__main__":
    main()
