import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Preformatted, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

# === CONFIG ===
ROOT_DIR = "."  #katalog repo
OUTPUT_FILE = "full_repo_documentation_Selenium_vs_Playwright.pdf"

EXCLUDE_DIRS = {".git", "venv", "__pycache__", ".idea", ".vscode"}
INCLUDE_EXTENSIONS = {".py", ".txt", ".md", ".json", ".yaml", ".yml"}

# === INIT PDF ===
doc = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=A4,
    rightMargin=2 * cm,
    leftMargin=2 * cm,
    topMargin=2 * cm,
    bottomMargin=2 * cm
)

styles = getSampleStyleSheet()
content = []

# === HELPERS ===

def add_title(text):
    content.append(Paragraph(text, styles["Title"]))
    content.append(Spacer(1, 12))


def add_heading(text):
    content.append(Paragraph(text, styles["Heading2"]))
    content.append(Spacer(1, 10))


def add_code(code_text):
    content.append(Preformatted(code_text, styles["Code"]))
    content.append(Spacer(1, 12))


def should_skip_dir(dirname):
    return dirname in EXCLUDE_DIRS


def build_tree_structure(root_dir):
    tree_lines = []
    for root, dirs, files in os.walk(root_dir):
        # filtr katalogów
        dirs[:] = [d for d in dirs if not should_skip_dir(d)]

        level = root.replace(root_dir, "").count(os.sep)
        indent = "    " * level
        tree_lines.append(f"{indent}{os.path.basename(root)}/")

        sub_indent = "    " * (level + 1)
        for f in files:
            tree_lines.append(f"{sub_indent}{f}")

    return "\n".join(tree_lines)


# === GENERATE ===

add_title("Repository Documentation")

# 📂 STRUKTURA
add_heading("Project Structure")
tree = build_tree_structure(ROOT_DIR)
add_code(tree)

content.append(PageBreak())

# 📄 PLIKI
for root, dirs, files in os.walk(ROOT_DIR):
    dirs[:] = [d for d in dirs if not should_skip_dir(d)]

    for file in files:
        filepath = os.path.join(root, file)

        # filtr rozszerzeń
        if not any(file.endswith(ext) for ext in INCLUDE_EXTENSIONS):
            continue

        relative_path = os.path.relpath(filepath, ROOT_DIR)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                code = f.read()
        except Exception as e:
            code = f"ERROR READING FILE: {e}"

        add_heading(f"File: {relative_path}")
        add_code(code)

        # opcjonalnie podział na strony (dla dużych plików)
        content.append(PageBreak())

# === BUILD PDF ===
doc.build(content)

print(f"✅ PDF generated: {OUTPUT_FILE}")