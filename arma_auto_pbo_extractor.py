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
def choose_directories(base:Path = Path('.')) -> Optional[List[str]]:
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

def get_sizes(file_list: List[str]) -> str:
    size: int = 0
    for file in file_list:
        size += os.path.getsize(file)
    return str(f"{float(size / (1024 ** 3)):.2f}GB")

def copy_files(destination_path: Path, file_list: list[str]):
    for file in file_list:
        print(f">  Copying {file.split("\\")[-1]} to {str(destination_path)}")
        try:
            shutil.copy(file, destination_path)
        except shutil.SameFileError:
            print(f"Failed due to duplicate file {file.split("\\")[-1]}.")
        except:
            print("Failed due to a generic error.")

def main():
    print("Asking for destination directory...")
    destination: Path = Path(choose_directories()[0])
    print(f"Destination directory: {str(destination)}")

    print("\nAsking for mod directories...")
    mod_directories: List[str] = choose_directories()

    print(f"\nYou selected {len(mod_directories)} directories.")
    [print(mod_directory) for mod_directory in mod_directories]

    pbo_list = []
    for mod_directory in mod_directories:
        for file in get_pbo_list(mod_directory):
            pbo_list.append(file)

    print(f"Found {len(pbo_list)} PBO files.")
    print(f"Total Size: {get_sizes(pbo_list)}")
    total, used, free = shutil.disk_usage(str(destination).split("\\")[0] + "\\")
    print(f"Free Space: {free // (2**30)} GiB")

    should_continue: bool = False if input("\nContinue? [Y/n]\n").lower().startswith("n") else True

    if not should_continue:
        print("Exiting.")
        exit(0)

    print(f"\nCopying files to {str(destination).split("\\")[-1]}...")

    start_time = time.time()

    copy_files(destination, pbo_list)

    print(f"\n\n\033[93mDone in {(time.time() - start_time) / 60} minutes!")

if __name__ == "__main__":
    main()