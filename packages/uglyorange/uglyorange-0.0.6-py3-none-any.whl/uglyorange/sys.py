#!/usr/bin/env python3
import argparse
import os


class SafelyFileRemover(argparse.ArgumentParser):
    def __init__(self):
        super().__init__(description='remove file safely')
        self.add_argument('file', help='file to remove')

    def remove_file_or_dir(self, file: str):
        if os.path.exists(file):
            os.rename(file, f"/tmp/{file}")
            print(f"file {file} moved to /tmp")
        else:
            print(f"{file} does not exist")

    @staticmethod
    def entrypoint():
        SafelyFileRemover().remove_file_or_dir(SafelyFileRemover().parse_args().file)
