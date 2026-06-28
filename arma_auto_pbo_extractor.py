from pathlib import Path
from typing import Optional, List
import os
import os.path
import shutil
import time

from PySide6.QtWidgets import (
    QApplication, 
    QFileDialog, 
    QListView, 
    QAbstractItemView, 
    QTreeView, 
    QFileSystemModel
)
app = QApplication()
def choose_directories() -> List[Path]:
    file_dialog = QFileDialog()
    file_dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
    file_dialog.setFileMode(QFileDialog.Directory)
    for widget_type in (QListView, QTreeView):
        for view in file_dialog.findChildren(widget_type):
            if isinstance(view.model(), QFileSystemModel):
                view.setSelectionMode(QAbstractItemView.ExtendedSelection)

    if file_dialog.exec():
        paths = list(map(Path, file_dialog.selectedFiles()))
        return paths
    print("\nNothing selected or selection cancelled, exiting.")
    exit(0)

def get_pbo_list(folder_path: str) -> List[Path]:
    addons_path = Path(folder_path) / "addons"
    if addons_path.exists():
        return list(addons_path.rglob("*.pbo"))
    return []

def get_sizes(file_list: List[Path]) -> str:
    size: int = 0
    for file in file_list:
        size += os.path.getsize(file)
    return str(f"{float(size / (1024 ** 3)):.2f}GB")

def copy_files(destination_path: Path, file_list: list[Path]):
    for file in file_list:
        print(f">  Copying {file} to {destination_path}")
        try:
            shutil.copy(file, destination_path)
        except shutil.SameFileError:
            print(f"Failed due to duplicate file {file.name}.")
        except Exception as e:
            print(f"Failed: {e}")

def main():
    print("Asking for destination directory...")
    destination: Path = Path(choose_directories()[0])
    print(f"Destination directory: {destination}")

    print("\nAsking for mod directories...")
    mod_directories: List[str] = choose_directories()

    print(f"\nYou selected {len(mod_directories)} directories.")
    for mod_directory in mod_directories:
        print(mod_directory)

    pbo_list = [
        pbo
        for mod_directory in mod_directories
        for pbo in get_pbo_list(mod_directory)
    ]

    print(f"\nFound {len(pbo_list)} PBO files.")
    print(f"Total Size: {get_sizes(pbo_list)}")
    total, used, free = shutil.disk_usage(destination.anchor)
    print(f"Free Space on disk {destination.anchor[0]}: {free // (2**30)} GiB")

    should_continue: bool = False if input("\nContinue? [Y/n]\n").lower().startswith("n") else True

    if not should_continue:
        print("Exiting.")
        exit(0)

    print(f"\nCopying files to {destination}...")

    start_time = time.time()

    copy_files(destination, pbo_list)

    print(f"\n\n\033[93mDone in {((time.time() - start_time)):.3f} seconds!")

if __name__ == "__main__":
    main()