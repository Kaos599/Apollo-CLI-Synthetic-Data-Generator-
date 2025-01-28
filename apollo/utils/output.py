import csv
import json
import yaml

def save_csv(data, output_path):
    if not data:
        return
    fieldnames = data[0].keys()
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def save_jsonl(data, output_path):
    with open(output_path, 'w') as f:
        for entry in data:
            f.write(json.dumps(entry) + '\n')

def save_yaml(data, output_path):
    with open(output_path, 'w') as f:
        yaml.dump(data, f, indent=2)