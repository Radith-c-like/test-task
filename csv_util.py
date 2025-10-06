# csv_util.py
import io
import csv
import json

def create_csv(tokenized_data):
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["Tokens", "Labels"])
    for item in tokenized_data:
        writer.writerow([json.dumps(item["tokens"]), json.dumps(item["labels"])])
    output.seek(0)
    return output
