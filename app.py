from flask import Flask, request, render_template
from extractor.extractor import extract_products

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    products = None
    if request.method == "POST":
        url = request.form.get("url") or (request.json and request.json.get("url"))
        if not url:
            products = ["Error: URL is required"]
        else:
            try:
                products = extract_products(url, verbose=True)
            except Exception as e:
                products = [f"Error: {str(e)}"]
    return render_template("index.html", products=products)

if __name__ == "__main__":
    app.run(debug=True)
