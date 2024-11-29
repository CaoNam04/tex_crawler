import os
import re
import json

def extract_tex_code(content, pattern):
    """Extracts sections of LaTeX code from content based on a given regex pattern."""
    matches = re.findall(pattern, content, re.DOTALL)
    return matches

def normalize_tex_code(tex_code):
    """Normalizes LaTeX code by removing extra spaces and line breaks."""
    tex_code = re.sub(r'\s+', ' ', tex_code).strip()  # Remove extra spaces and line breaks
    return tex_code

def save_to_json(output_path, data):
    """Saves the extracted data to a JSON file."""
    with open(output_path, 'w', encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

def process_tex_files_in_folder(folder_path, output_folder):
    """Processes all .tex files in a folder, extracting formulas, tables, and figures."""
    # Patterns for extraction
    formula_pattern = (
        r"\\\(.*?\\\)"                            # Inline math using \( ... \)
        r"|\\\[.*?\\\]"                           # Display math using \[ ... \]
        r"|\$.*?\$"                               # Inline math using $ ... $
        r"|\\begin\{equation\}.*?\\end\{equation\}"  # Equation environment
        r"|\\begin\{align\*?\}.*?\\end\{align\*?\}"  # Align environment (numbered & unnumbered)
        r"|\\begin\{gather\*?\}.*?\\end\{gather\*?\}"  # Gather environment (numbered & unnumbered)
        r"|\\begin\{multline\*?\}.*?\\end\{multline\*?\}"  # Multiline environment
        r"|\\begin\{cases\}.*?\\end\{cases\}"            # Cases environment
        r"|\\begin\{array\}.*?\\end\{array\}"            # Array environment
        r"|\\begin\{bmatrix\}.*?\\end\{bmatrix\}"        # Bmatrix (bracketed matrices)
        r"|\\begin\{pmatrix\}.*?\\end\{pmatrix\}"        # Pmatrix (parenthesized matrices)
    )

    table_pattern = (
        r"\\begin\{table\*?\}.*?\\end\{table\*?\}"       # Table environment (numbered & unnumbered)
        r"|\\begin\{tabular\}.*?\\end\{tabular\}"        # Tabular inside tables
    )

    figure_pattern = (
        r"\\begin\{figure\*?\}.*?\\end\{figure\*?\}"     # Figure environment (numbered & unnumbered)
        r"|\\includegraphics\[.*?\]\{.*?\}"              # Includegraphics for images
    )

    # Sets to hold unique extracted content
    formulas = set()
    tables = set()
    figures = set()

    # Walk through the folder to find .tex files
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.tex'):  # Process only .tex files
                tex_file_path = os.path.join(root, file)
                print(f"Processing {tex_file_path}...")
                try:
                    # Read the content of the .tex file
                    with open(tex_file_path, 'r', encoding="utf-8") as f:
                        content = f.read()

                    # Extract content based on patterns
                    formulas.update(normalize_tex_code(f) for f in extract_tex_code(content, formula_pattern))
                    tables.update(normalize_tex_code(t) for t in extract_tex_code(content, table_pattern))
                    figures.update(normalize_tex_code(f) for f in extract_tex_code(content, figure_pattern))

                except Exception as e:
                    print(f"Error processing {tex_file_path}: {e}")

    # Save the extracted content to JSON files
    os.makedirs(output_folder, exist_ok=True)
    save_to_json(os.path.join(output_folder, "formulas.json"), list(formulas))
    save_to_json(os.path.join(output_folder, "tables.json"), list(tables))
    save_to_json(os.path.join(output_folder, "figures.json"), list(figures))
    print("Extraction completed. Data saved to JSON files.")

# Example usage
folder_path = "2010.11645"  # Path to the extracted folder
output_folder = "output_data"  # Folder to save the JSON files
process_tex_files_in_folder(folder_path, output_folder)
