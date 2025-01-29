from flask import Flask, request, render_template
import pandas as pd

# Load the Excel data
file_path = "EXCEL DATA BRAIN CANCER.xlsx"  # Replace with your file path
data = pd.read_excel("A:/likitha/LIKI/EXCEL DATA BRAIN CANCER.xlsx")


# Flask app setup
app = Flask(__name__)

@app.route("/", methods=["GET"])
def search():
    gene_name = request.args.get("gene_name", "").strip()
    results = []
    searched = False

    if gene_name:
        searched = True
        # Filter rows containing the gene name (case-insensitive)
        filtered_data = data[data["Gene Names"].str.contains(gene_name, case=False, na=False)]
        results = filtered_data.to_dict(orient="records")

    return render_template("index.html", results=results, searched=gene_name)

if __name__ == "__main__":
    app.run(debug=True)
