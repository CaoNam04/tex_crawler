import os
import json
import matplotlib.pyplot as plt
import matplotlib

# Enable LaTeX rendering for text
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.preamble'] = r'''
    \usepackage{amsmath,amssymb}
    \usepackage{array} % For table support
    \newcommand{\Av}{\mathbf{A}} % Example definition
    \newcommand{\diag}{\operatorname{diag}}
    \newcommand{\br}[1]{\left(#1\right)}
    \newcommand{\tran}{\mathsf{T}}
    \newcommand{\opt}{\operatorname{opt}}
'''

# Directories for input and output
input_files = {
    "formula": "output_data/formulas.json",
    "table": "output_data/tables.json",
    "figure": "output_data/figures.json"
}
output_root_dir = "rendered_tex_2010.11645"

# Create the output root directory and subdirectories
os.makedirs(output_root_dir, exist_ok=True)
output_dirs = {key: os.path.join(output_root_dir, key) for key in input_files.keys()}
for output_dir in output_dirs.values():
    os.makedirs(output_dir, exist_ok=True)

# Function to render LaTeX content into a .png file
def render_content(content, output_path, figsize=(10, 5)):
    try:
        plt.figure(figsize=figsize)
        plt.text(0.5, 0.5, content, fontsize=16, ha='center', va='center', wrap=True)
        plt.axis('off')  # Remove axes
        plt.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=0.1)  # Save as .png
        plt.close()  # Close the figure to free memory
    except Exception as e:
        raise RuntimeError(f"Error rendering content: {e}")

# Iterate through each type (formula, table, figure)
for content_type, json_file in input_files.items():
    if not os.path.exists(json_file):
        print(f"File {json_file} not found. Skipping {content_type}.")
        continue
    
    # Load content from JSON file
    with open(json_file, 'r', encoding='utf-8') as file:
        contents = json.load(file)
    
    # Render each piece of content
    for idx, content in enumerate(contents, start=1):
        file_name = f"{content_type}_{idx}.png"
        output_path = os.path.join(output_dirs[content_type], file_name)
        try:
            # Use larger figure sizes for tables and figures
            figsize = (12, 6) if content_type in ['table', 'figure'] else (10, 5)
            render_content(content, output_path, figsize=figsize)
            print(f"Rendered {content_type} {idx}: {output_path}")
        except Exception as e:
            print(f"Failed to render {content_type} {idx}: {e}")

print("Rendering completed. Check the output folders for results.")
