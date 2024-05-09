from mdbook_pdf_summary.parse_section import Section
import os
def check_title(prefix_path: str, node: Section, overwrite: bool) -> bool:
    """
    Based on `SUMMARY.md`, check whether the title of each markdown file is the same as the content.
    If `overwrite==True`, generate the title at the first line, for those unmatched files.

    Parameters:
    -----------
    prefix_path: str
        The path prefix of the markdown files.
    node: Section
        The node of the section tree.
    overwrite: bool
        Whether to overwrite the title in the markdown file.

    Returns:
    --------
    bool
        Whether all titles are matched (after overwrite).
    """
    all_matched = True
    for child in node.children:
        child_result = check_title(prefix_path, child, overwrite)
        if not child_result:
            return False
    if node.is_root():
        return True
    
    source_file = os.path.join(prefix_path, node.source_file)
    if not os.path.exists(source_file):
        print(f"File {source_file} does not exist")
        return False
    with open(source_file, 'r') as f:
        lines = f.readlines()
    # Find the first title `# ${title}`
    for idx, line in enumerate(lines):
        if line.startswith('# '):
            title = line[2:]
            if not title.startswith(node.title):
                all_matched = False
                print("[ERROR] Title not matched: source_file:{}, line num:{}, title:{}, title in `SUMMARY.md`:{}".format(
                    source_file, idx, title, node.title))
                break
    if not all_matched and overwrite:
        lines.insert(0, f"# {node.title}\n")
        print(f"[Info] Overwrite title as {node.title } in {node.source_file}")
        with open(source_file, 'w') as f:
            f.writelines(lines)
        all_matched = True
    return all_matched

