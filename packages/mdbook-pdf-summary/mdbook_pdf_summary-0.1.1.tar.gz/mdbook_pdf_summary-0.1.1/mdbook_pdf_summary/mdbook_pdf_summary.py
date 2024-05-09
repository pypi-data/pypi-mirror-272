#!/usr/bin/env python3
from mdbook_pdf_summary.parse_section import Section, parse_section_tree
import pypdf
import lxml.html
import urllib
import argparse
import os


def get_dom_id(node: Section):
    """
    Get the DOM ID in `print.html`.

    ATTENTION:
    Before calling `get_href_path`, the user must use `check_title.check_title` to make sure the title is matched.

    The rule is:
    1. DOM="${MARKDOWN PATH}"
    2. lowercase all the characters.
    3. replace all the `/` with `-`.
    4. replace all the ` ` with `-`

    e.g.
    line in `SUMMARY.md`(double G not typoo):
    - [Getting Started](./user_guide/GGetting_started.md)

    line in `print.html`:
    href="#user_guide-ggetting_started-getting-started"
    """
    source_path = node.source_file
    # remove the prefix `./`
    if source_path.startswith("./"):
        source_path = source_path[2:]
    # strip the suffix
    source_path = source_path.split(".")[0]
    result = source_path
    # lowercase all the characters
    result = result.lower()
    # replace the `/` with `-`
    result = result.replace("/", "-")
    # replace the ` ` with `-`
    result = result.replace(" ", "-")
    return result


def add_outline(
    html_root, reader: pypdf.PdfReader, writer: pypdf.PdfWriter, node: Section
):
    """
    Add outline to the PDF file.

    Parameters:
    -----------
    html_root: lxml.html.HtmlElement
        The root element of the HTML file.
    reader: pypdf.PdfReader
        The reader of the PDF file.
    writer: pypdf.PdfWriter
        The writer of the PDF file.
    node: Section
        The node of the section tree.
    """
    if not node.is_root():
        id = get_dom_id(node)
        try:
            results = html_root.get_element_by_id(id)
        except KeyError:
            print("[ERROR] Element not found: [{}]".format(id))
            return

        if results is None:
            print("[ERROR] Element is None, id: [{}]".format(id))
            return
        dest = reader.named_destinations["/{}".format(urllib.parse.quote(id))]

        page = None
        fit = None
        if dest.get("/Type") != "/Fit":
            page = reader.get_destination_page_number(dest)
            fit = pypdf.generic.Fit(
                dest.get("/Type"),
                (dest.get("/Left"), dest.get("/Top"), dest.get("/Zoom")),
            )
        node.outline_item = writer.add_outline_item(
            str(node), page, node.parent.outline_item, fit=fit
        )
    # dfs
    for child in node.children:
        add_outline(html_root, reader, writer, child)


def main():
    parser = argparse.ArgumentParser(
        prog="mdbook_pdf_summary", description="Add outline to the PDF file."
    )
    parser.add_argument(
        "--html_path",
        type=str,
        help="path of the `print.html` generated `mdbook-pdf`",
        default="book/html/print.html",
    )
    parser.add_argument(
        "--pdf_path",
        type=str,
        help="path of the `output.pdf` generated `mdbook-pdf`",
        default="book/pdf/output.pdf",
    )
    parser.add_argument(
        "--summary_path",
        type=str,
        help="path of the `SUMMARY.md`",
        default="src/SUMMARY.md",
    )
    parser.add_argument(
        "--output_path",
        type=str,
        help="path of the output PDF file",
        default="output_with_outline.pdf",
    )
    args = parser.parse_args()
    print("============ args =============")
    print("args.html_path: ", args.html_path)
    print("args.pdf_path: ", args.pdf_path)
    print("args.summary_path: ", args.summary_path)
    print("args.output_path: ", args.output_path)
    if not os.path.exists(args.html_path):
        raise FileNotFoundError(f"{args.html_path} does not exist")
    if not os.path.exists(args.pdf_path):
        raise FileNotFoundError(f"{args.pdf_path} does not exist")
    if not os.path.exists(args.summary_path):
        raise FileNotFoundError(f"{args.summary_path} does not exist")

    reader = pypdf.PdfReader(args.pdf_path)
    writer = pypdf.PdfWriter()
    writer.append(reader)
    with open(args.summary_path) as f:
        md_text = f.read()
    section_root = parse_section_tree(md_text)
    html_root = None
    with open(args.html_path, "r", encoding="utf8") as f:
        data = f.read()
        html_root = lxml.html.fromstring(data)
    if html_root is None:
        raise ("[ERROR] html_root is None")
    add_outline(html_root, reader, writer, section_root)
    with open(args.output_path, "wb") as f:
        writer.write(f)
        print("[INFO] Write to {}".format(args.output_path))
