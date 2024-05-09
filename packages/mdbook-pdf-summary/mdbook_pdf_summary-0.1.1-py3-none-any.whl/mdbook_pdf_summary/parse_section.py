import re    
class Section:
    def __init__(self, title: str, source_file: str, depth: int, index: int):
        self.title = title
        self.source_file = source_file
        self.depth = depth
        self.index = index
        self.parent = None
        self.children = []
        self.outline_item = None
    def set_parent(self, parent):
        self.parent = parent
    def add_children(self, child):
        self.children.append(child)
    def path_to_root(self):
        path = []
        node = self
        while not node.is_root():
            path.append(str(node.index + 1))
            node = node.parent
        path = path[::-1]
        return path
    def is_root(self):
        return self.parent is None

    def __str__(self):
        path = self.path_to_root()
        return "{}. {}".format(".".join(path), self.title)

def print_section_tree(root: Section):
    print(root)
    for child in root.children:
        print_section_tree(child)

def parse_section_tree(md_text: str):
    """
    Construct a tree from markdown unordered list.
    
    Markdown format:
    - Chaptor 1
        - Section 1.1
        - Section 1.2
            - Section 1.2.1
    - Chaptor 2
    - Chaptor 3
        - Section 3.1

    Consturct a tree need the line order and the indent number.
    """

    # root.depth = 0
    root = Section("root", "", 0, 0)
    # key: depth, value: node.
    bfs_map = {0: [root]}
    # can just match unordered_list, a.k.a. `-`
    pattern = re.compile(r'( *)- ([^:\n]+)(?:: ([^\n]*))?\n?')
    tmp = None
    min_indent_num = 4
    for indent, name, value in pattern.findall(md_text):
        # `-[${section_name}](${md_path})``
        title = name.split("](")[0].split("[")[1]
        source_file = name.split("](")[1].split(")")[0]
        indent_num = len(indent)
        # incase of the min_indent_num is 2
        if indent_num > 0 and indent_num < min_indent_num:
            min_indent_num = indent_num
        depth = indent_num // min_indent_num
        if depth + 1 not in bfs_map:
            bfs_map[depth + 1] = []
        tmp = Section(title, source_file, depth + 1, 0)
        bfs_map[depth + 1].append(tmp)
        parent = bfs_map[depth][-1]
        tmp.set_parent(parent)
        tmp.index = len(parent.children)
        parent.add_children(tmp)

    return root

