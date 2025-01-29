from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load the Excel file
excel_file_path = "C:/Users/UDAY/Desktop/ALokAIpresentnew/Pantechuniversity2025/likitha/LIKI/EXCEL DATA BRAIN CANCER.xlsx"  # Replace with your Excel file path
df = pd.read_excel(excel_file_path)

@app.route('/')
def home():
    # Example data that you might want to render dynamically for each tab
    tab1_content = "This is dynamic content for Tab 1"
    tab2_content = "This is dynamic content for Tab 2"
    tab3_content = "This is dynamic content for Tab 3"
    
    return render_template('index.html', tab1_content=tab1_content, tab2_content=tab2_content, tab3_content=tab3_content)

@app.route('/', methods=['GET', 'POST'])
def index():
    gene_name = ''  # Default empty gene name
    tables = []  # Default empty table list
    if request.method == 'POST':
        gene_name = request.form['gene_name'].strip()  # Strip spaces to prevent search issues

        if gene_name:  # Only search if the input is not empty
            # Filter the DataFrame to find matching gene names (case-insensitive search)
            filtered_df = df[df['Gene Names'].str.contains(gene_name, case=False, na=False)]
            
            if not filtered_df.empty:
                # Convert "Sequence" column to clickable links
                if 'Sequence' in filtered_df.columns:
                    filtered_df['Sequence'] = filtered_df['Sequence'].apply(
                        lambda x: f'<a href="{x}" target="_blank">{x}</a>' if pd.notna(x) else x
                    )
                tables = [filtered_df.to_html(classes='data', header=True, escape=False)]  # escape=False allows HTML

    return render_template('index.html', tables=tables, gene_name=gene_name)

@app.route('/suggestions', methods=['GET'])
def suggestions():
    query = request.args.get('query', '').strip()
    suggestions = []

    if query:
        # Perform case-insensitive search for matching gene names
        filtered_df = df[df['Gene Names'].str.contains(query, case=False, na=False)]
        suggestions = filtered_df['Gene Names'].tolist()  # Get the list of matching gene names
    
    return jsonify(suggestions)


if __name__ == '__main__':
    app.run(debug=True)
