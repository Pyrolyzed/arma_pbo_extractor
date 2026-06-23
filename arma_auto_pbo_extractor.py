from pathlib import Path
from typing import Optional, List
import os
import os.path
import shutil

from PySide6.QtWidgets import (
    QApplication, 
    QFileDialog, 
    QListView, 
    QAbstractItemView, 
    QTreeView, 
    QFileSystemModel
)
app = QApplication()
def choose_directories(base:Path = Path('.')) -> Optional[List[str]]:
    """
    Open a dialogue to select multiple directories
    Args:
        base (Path): Starting directory to show when opening dialogue
    Returns:
        List[str]: List of paths that were selected, ``None`` if "cancel" selected"
    References:
        Mildly adapted from https://stackoverflow.com/a/28548773
        to use outside an exising Qt Application
    """
    file_dialog = QFileDialog()
    file_dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
    file_dialog.setFileMode(QFileDialog.Directory)
    for widget_type in (QListView, QTreeView):
        for view in file_dialog.findChildren(widget_type):
            if isinstance(view.model(), QFileSystemModel):
                view.setSelectionMode(
                    QAbstractItemView.ExtendedSelection)

    if file_dialog.exec():
        paths = file_dialog.selectedFiles()
        return paths

def get_pbo_list(folder_path: str) -> List[str]:
    addons_path = Path(f"{folder_path}\\addons")
    pbo_list: List[str] = []
    if addons_path.exists():
        for root, dirs, files in os.walk(addons_path):
            for file in files:
                if file.endswith(".pbo"):
                    pbo_list.append(os.path.join(root, file))
        return pbo_list
    return []

def copy_files(destination_path: Path, file_list: list[str]):
    for file in file_list:
        shutil.copy(file, destination_path)

def main():
    print("Asking for destination directory...")
    destination: Path = Path(choose_directories()[0])
    print(f"Destination directory: {str(destination)}")
    print("\nAsking for mod directories...")
    mod_directories: List[str] = choose_directories()
    print(f"\nYou selected {len(mod_directories)} directories.")
    [print(mod_directory) for mod_directory in mod_directories]
    should_continue: bool = False if input("\nContinue? [Y/n]\n").lower().startswith("n") else True
    if not should_continue:
        print("Exiting.")
        exit(0)

    counter = 0
    for mod_directory in mod_directories:
        pbo_list = get_pbo_list(mod_directory)
        counter += len(pbo_list)
        copy_files(destination, pbo_list)
    print(f"Done! Copied {counter} files.") 


if __name__ == "__main__":
    main()