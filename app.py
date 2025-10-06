# app.py
from flask import Flask, request, render_template_string, send_file
from extractor import FurnitureExtractor
from csv_util import create_csv
import io

HTML_PAGE = """ ... """  # Можно использовать твой HTML-шаблон из оригинального кода

app = Flask(__name__)
extractor = FurnitureExtractor()

@app.route("/", methods=["GET", "POST"])
def home():
    products = None
    url = None
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            products, _ = extractor.extract_products(url)
    return render_template_string(HTML_PAGE, products=products, url=url)

@app.route("/download_csv", methods=["POST"])
def download_csv():
    url = request.form.get("url")
    if not url:
        return "Error: No URL provided", 400
    _, tokenized_data = extractor.extract_products(url)
    if not tokenized_data:
        return "Error: No data to export", 400
    csv_file = create_csv(tokenized_data)
    return send_file(
        io.BytesIO(csv_file.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='tokenized_furniture_data.csv'
    )

if __name__ == "__main__":
    app.run(debug=True)
