import os
from mdbook_pdf_summary import parse_section_tree, check_title
if __name__ == "__main__":
    summary_path = "./example/a_book/src/SUMMARY.md"
    with open(summary_path) as f:
        md_text = f.read()
    prefix_path = os.path.dirname(summary_path)
    section_tree = parse_section_tree(md_text)
    check_result = check_title(prefix_path, section_tree, overwrite=True)
    print(f"Check result: {check_result}")