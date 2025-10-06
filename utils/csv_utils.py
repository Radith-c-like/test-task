import io
import csv
import json

class CSVGenerator:
    @staticmethod
    def create_csv(tokenized_data: list[dict]) -> io.StringIO:
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Tokens", "Labels"])
        for item in tokenized_data:
            tokens_str = json.dumps(item["tokens"])
            labels_str = json.dumps(item["labels"])
            writer.writerow([tokens_str, labels_str])
        output.seek(0)
        return output