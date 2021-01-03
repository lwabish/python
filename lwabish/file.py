# -*- encoding: utf-8 -*-
import os


def get_all_filenames(path: str, ignore: tuple = (), all_files: list = None):
    """
    遍历并返回path目录下所有文件，包含子目录。返回值不包含路径，只包含文件名称\n
    ;ignore;要忽略的目录名称或文件名称\n
    ;all_files;默认不需要提供\n
    """
    if all_files is None:
        all_files = list()
    if os.path.isfile(path):
        file_name = path.split('/')[-1]
        if file_name not in ignore:
            all_files.append(file_name)
    elif os.path.isdir(path):
        for s in os.listdir(path):
            if s in ignore:
                continue
            subpath = os.path.join(path, s)
            get_all_filenames(subpath,  ignore, all_files)
    return all_files


def get_binary_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()
