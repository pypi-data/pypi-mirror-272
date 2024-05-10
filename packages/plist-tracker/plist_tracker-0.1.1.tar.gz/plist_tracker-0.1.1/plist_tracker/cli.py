import subprocess
from typing import AnyStr, List, Optional
from rich.prompt import Prompt
from pathlib import Path
import tempfile
import shutil
import filecmp
from textual.app import App, ComposeResult
from textual.widgets import Button, Footer, Header, Static, Tree, TextArea
from textual.widgets._tree import TreeNode
import difflib


class DiffItem:
    def __init__(self, src_path: Path, tmp_path: Path, name: str):
        self.diff: Optional[List[str]] = None
        self.name = name
        self.src_path = src_path
        self.tmp_path = tmp_path

    def compute_diff(self):
        src_content = DiffItem._decode_plist(self.src_path)
        tmp_content = DiffItem._decode_plist(self.tmp_path)

        if len(src_content) == 0 or len(tmp_content) == 0:
            return

        self.diff = list(
            difflib.unified_diff(src_content, tmp_content, "before", "after", n=9999999)
        )

    @staticmethod
    def _decode_plist(path: Path) -> List[str]:
        result = ""
        try:
            result = subprocess.run(
                ["plutil", "-convert", "xml1", "-o", "/dev/stdout", str(path)],
                stdout=subprocess.PIPE,
            ).stdout.decode("utf-8")
        except:
            print(f"Failed to decode file {path}")

        return result.splitlines(True)


class TrackerApp(App):
    CSS = """
    #sidebar {
        dock: left;
        width: 50;
        height: 100%;
    }
    """

    BINDINGS = [("f", "copy_file_path", "Copy file name"), ("f10", "exit", "Exit")]

    def __init__(self, sys_changes: List[DiffItem], usr_changes: List[DiffItem]):
        super().__init__()
        self.sys_changes = sys_changes
        self.usr_changes = usr_changes
        self.text_area: Optional[TextArea] = None
        self.cur_diff: Optional[DiffItem] = None

    def compose(self) -> ComposeResult:
        tree: Tree[dict] = Tree("Changed files", id="sidebar")
        tree.root.expand()
        tree.show_root = False

        if len(self.sys_changes) > 0:
            TrackerApp._add_branch(tree.root, "System", self.sys_changes)

        if len(self.usr_changes) > 0:
            TrackerApp._add_branch(tree.root, "User", self.usr_changes)

        self.text_area = TextArea(read_only=True, show_line_numbers=True, soft_wrap=False)

        yield tree
        yield self.text_area
        yield Footer()

    def on_tree_node_highlighted(self, node):
        self.text_area.clear()
        self.cur_diff = None
        if node.node.data is not None:
            self.text_area.load_text("".join(node.node.data.diff))
            self.cur_diff = node.node.data

    def action_copy_file_path(self):
        if self.cur_diff is not None:
            subprocess.run("pbcopy", text=True, input=str(self.cur_diff.src_path))

    def action_exit(self):
        self.exit()

    @staticmethod
    def _add_branch(root: TreeNode, name: str, files: List[DiffItem]):
        branch = root.add(name)
        branch.expand()
        for file in files:
            branch.add_leaf(file.name, file)


def main():
    temp_dir = Path(tempfile.mkdtemp())
    temp_system = temp_dir.joinpath("sys")
    temp_user = temp_dir.joinpath("usr")
    src_system = Path("/Library/Preferences")
    src_user = Path.home().joinpath("Library/Preferences")

    print(temp_system)
    print(temp_user)

    try:
        shutil.copytree(src_system, temp_system)
    except:
        pass

    try:
        shutil.copytree(src_user, temp_user)
    except:
        pass

    Prompt.ask("Change a setting and press any key")

    sys_changes = _compare_files(src_system, temp_system)
    usr_changes = _compare_files(src_user, temp_user)

    app = TrackerApp(sys_changes, usr_changes)
    app.run()

    try:
        shutil.rmtree(temp_dir)
    except:
        print(f"Error while removing temp dir. You can remove it manually: {temp_dir}")


def _compare_files(src_path: Path, tmp_path: Path) -> List[DiffItem]:
    usr_cmp = filecmp.dircmp(src_path, tmp_path)
    result = [
        DiffItem(src_path.joinpath(file), tmp_path.joinpath(file), file)
        for file in usr_cmp.diff_files
    ]
    for item in result:
        item.compute_diff()

    return result


if __name__ == "__main__":
    main()
