from flask import Flask, request, render_template_string, send_file
from services.product_service import ProductService
from utils.csv_utils import CSVGenerator
import io
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Flask app setup
app = Flask(__name__)
product_service = ProductService()

# HTML template
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Furniture Extractor</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
</head>
<body class="p-5">
    <h1 class="mb-4">🛋 Furniture Extractor <small class="text-muted fs-5">(Powered by NER model)</small></h1>
    <form method="post" action="/" class="mb-5">
        <input class="form-control" type="url" name="url" placeholder="Enter full URL (e.g., https://example.com/products)" required>
        <button class="btn btn-primary mt-3">Extract Furniture Products</button>
    </form>
    {% if products %}
        {% if products[0].startswith("Error:") %}
            <div class="alert alert-danger" role="alert">
                <strong>Error:</strong> {{ products[0] | replace("Error: ", "") }}
            </div>
        {% else %}
            <h3 class="mb-3">Found products: <span class="badge bg-success">{{ products | length }}</span></h3>
            <ul class="list-group mb-3">
                {% for p in products %}
                    <li class="list-group-item">{{ p }}</li>
                {% endfor %}
            </ul>
            <form method="post" action="/download_csv">
                <input type="hidden" name="url" value="{{ url }}">
                <button class="btn btn-success">Download CSV with Token Labels</button>
            </form>
        {% endif %}
    {% elif products is not none %}
        <div class="alert alert-warning" role="alert">
            No furniture items were found on this page.
        </div>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    products = None
    url = None
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            products, _ = product_service.extract_products(url)
    return render_template_string(HTML_PAGE, products=products, url=url)

@app.route("/download_csv", methods=["POST"])
def download_csv():
    url = request.form.get("url")
    if not url:
        return "Error: No URL provided", 400
    
    _, tokenized_data = product_service.extract_products(url)
    if not tokenized_data:
        return "Error: No data to export", 400
    
    csv_file = CSVGenerator.create_csv(tokenized_data)
    return send_file(
        io.BytesIO(csv_file.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='tokenized_furniture_data.csv'
    )

if __name__ == "__main__":
    app.run(debug=True)