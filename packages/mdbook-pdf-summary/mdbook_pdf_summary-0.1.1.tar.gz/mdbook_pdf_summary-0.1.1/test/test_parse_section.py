from mdbook_pdf_summary import parse_section_tree, print_section_tree
if __name__ == "__main__":
    summary_path = "./example/a_book/src/SUMMARY.md"
    summary_path = "./Interface/src/SUMMARY.md"
    with open(summary_path) as f:
        md_text = f.read()
    result = parse_section_tree(md_text)
    print_section_tree(result)