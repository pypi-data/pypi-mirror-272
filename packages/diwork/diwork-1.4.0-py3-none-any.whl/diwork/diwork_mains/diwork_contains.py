# -*- coding: utf-8 -*-

import os
import sys
import argparse

from diwork_ways import *

from tqdm import tqdm


def get_files_size(files: list) -> list:
    """
    return sorted by size list
    """
    res = []
    for file_i in files:
        file_i_size = os.path.getsize(file_i)
        res.append((file_i, file_i_size))
    res = sorted(res, key=lambda size_i: res[1])
    return res


def get_nearest_file_by_name(file: str, files: list) -> list:
    file_name = os.path.basename(file)
    res = []
    for file_i in files:  # TODO: optimize this piece of code
        file_i_name = os.path.basename(file_i)
        if file_name in file_i_name:
            res.append(file_i)
    return res


def get_file_hash_4_contains(file: str, d: dict):
    if file in d:
        return d[file]
    else:
        file_hash = get_hash_file(file)
        d[file] = file_hash
        return d[file]

def get_nearest_file_by_size(file: str, sizes: list) -> list:
    x = os.path.getsize(file)
    left = 0
    right = len(sizes) - 1
    result = []

    while left <= right:
        mid = (left + right) // 2
        if sizes[mid][1] == x:
            result.append(sizes[mid])
            i = mid - 1
            while i >= 0 and sizes[i][1] == x:
                result.append(sizes[i])
                i -= 1
            j = mid + 1
            while j < len(sizes) and sizes[j][1] == x:
                result.append(sizes[j])
                j += 1
            return result
        elif sizes[mid][1] < x:
            left = mid + 1
        else:
            right = mid - 1

    return [el_i[0] for el_i in result]


def get_nearest_file_by_size_one(file: str, sizes: list) -> str:
    x = os.path.getsize(file)
    left = 0
    right = len(sizes) - 1
    res = None

    while left <= right:
        mid = (left + right) // 2
        if sizes[mid][1] == x:
            res = sizes[mid]
            break
        elif sizes[mid][1] < x:
            left = mid + 1
        else:
            right = mid - 1

    if res is None:
        if right < 0:
            res = sizes[left]
        elif left >= len(sizes):
            res = sizes[right]
        else:
            res = sizes[left] if abs(x - sizes[left][1]) < abs(x - sizes[right][1]) else sizes[right]

    return res[1]


def main_contains(args: list):
    platform = sys.platform
    parser = argparse.ArgumentParser(prog="diwork contains",
        description="The module checks the contents of all files from {folder_src} in {folder_dest}. "
                    "It will find those that are not in directory 2.")
    parser.add_argument("folder_src", type=str, nargs=1,
                       help="Path to source directory")
    parser.add_argument("folder_dest", type=str, nargs=1,
                       help="Path to destination directory")

    parser = common_init_parser(parser)
    args = parser.parse_args(args)
    common_init_parse(args)

    folder1 = args.folder_src[0]
    folder2 = args.folder_dest[0]

    folder1_abs = os.path.abspath(folder1)
    folder2_abs = os.path.abspath(folder2)
    if not is_folder(folder1_abs):
        pout(f"\"{folder1_abs}\" is not folder. ")
        exit()
    if not is_folder(folder2_abs):
        pout(f"\"{folder2_abs}\" is not folder. ")
        exit()

    files1, files2 = get_files_list(folder1_abs), get_files_list(folder2_abs)
    files2_sizes = get_files_size(files2)
    d = {}
    reses, not_founded = [], []

    for file1_i in tqdm(files1):
        file1_i_hash = get_file_hash_4_contains(file1_i, d)

        nearests_by_name = get_nearest_file_by_name(file1_i, files2)
        if len(nearests_by_name) != 0:
            f = False
            for file2_i in nearests_by_name:
                file2_i_hash = get_file_hash_4_contains(file2_i, d)
                if file1_i_hash == file2_i_hash:
                    reses.append(f"* \"{file1_i}\" is \"{file2_i}\"")
                    f = True
                    break
            if f:
                continue

        nearests_by_size = get_nearest_file_by_size(file1_i, files2_sizes)
        if len(nearests_by_size) != 0:
            f = False
            for file2_i in nearests_by_size:
                file2_i_hash = get_file_hash_4_contains(file2_i, d)
                if file1_i_hash == file2_i_hash:
                    reses.append(f"* \"{file1_i}\" is \"{file2_i}\"")
                    f = True
                    break
            if f:
                continue

        f = False
        for file2_i in files2:
            file2_i_hash = get_file_hash_4_contains(file2_i, d)
            if file1_i_hash == file2_i_hash:
                reses.append(f"* \"{file1_i}\" is \"{file2_i}\"")
                f = True
                break
        if f:
            continue
        else:
            not_founded.append(f"{file1_i}")

    pout("Calculated info: ")
    if len(reses) != 0:
        for info_i in reses:
            pout(info_i)
    else:
        pout(f"Not a single coincidence. "
             f"None of the files from \"{folder1_abs}\" are contained in the directory \"{folder2_abs}\". ")

    if len(not_founded) != 0:
        pout("\n\t!!!!! THESE FILE ARE NOT FOUND: !!!!!")
        for losted_i in not_founded:
            pout(losted_i)
        pout("\t!!!!!!!!!!\n")
    else:
        pout(f"All files from \"{folder1_abs}\" contains in the directory \"{folder2_abs}\". ")

    pout("=============== Done! ===============")
