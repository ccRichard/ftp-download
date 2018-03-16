# -*- coding: utf-8 -*-
# Version   : python3
# Date       : 2018-1-23 10:29:56
# Author     : cc
# Description: update client from ftp download


import os
import sys
import shutil
import getopt
import zipfile
from ftplib import FTP

cfg = {
    "ip": "127.0.0.1",
    "user": "test",
    "pwd": "test",
    "port": 21,
    "ftp_package": "/packages",
    "ftp_scripts": "/scripts",
    "local_path": "./"
}


def ftp_connect():
    """ 建立ftp连接 """
    ftp = FTP()
    ftp.set_debuglevel(2)
    ftp.connect(cfg["ip"], cfg["port"])
    ftp.login(cfg["user"], cfg["pwd"])

    return ftp


def ftp_download_file(ftp_path, filename):
    """ 从ftp上下载文件 """
    buffsize = 1024

    ftp = ftp_connect()
    ftp.cwd(ftp_path)
    print(u"开始下载{}文件，请等待...".format(filename))
    fp = open(filename, "wb")
    ftp.retrbinary("RETR "+filename, fp.write, buffsize)
    ftp.set_debuglevel(0)
    fp.close()
    ftp.quit()

    print(u"{}文件下载成功。".format(filename))


def uncompress_file(zip_filename):
    """ 解压缩文件 """
    zip_file = zipfile.ZipFile(zip_filename)
    print(u"正在解压{}文件，请等待...".format(zip_filename))

    for name in zip_file.namelist():
        zip_file.extract(name, zip_filename.split(".")[0]+"/")

    print(u"{}文件解压成功。".format(zip_filename))
    return zip_filename.split(".")[0]


def move_files(f_from, f_to):
    """ 将f_from目录下的所有文件或文件夹移动到f_to目录下 """
    files = os.listdir(f_from)
    print(u"正在将{}目录下的文件拷贝到{}目录下，请等待...".format(f_from, f_to))

    for file in files:
        # 先判断目标目录下是否有已存在的文件或文件夹，如果有则删除
        if os.path.isdir(f_from+"/"+file) and os.path.exists(f_to+"/"+file):
            shutil.rmtree(f_to + "/" + file)
        elif os.path.isfile(f_from+"/"+file) and os.path.exists(f_to+"/"+file):
            os.remove(f_to + "/" + file)

        shutil.move(f_from+"/"+file, f_to)

    print(u"{}目录下的{}文件成功移动到{}目录下。".format(f_from, ",".join(files), f_to))


def clear_files(path):
    """ 删除文件及所有文件夹 """
    shutil.rmtree(path)


def update_packages(filename = "pc_package.zip"):
    """ 更新客户端所有文件 """
    ftp_download_file(cfg["ftp_package"], filename)
    temp_file = uncompress_file(filename)
    move_files(temp_file+"/Windows", cfg["local_path"])
    print(u"所有客户端文件更新完毕。")
    # 删除缓存解压文件目录
    clear_files(cfg["local_path"]+"/"+temp_file)


def update_scripts(filename = "script.zip"):
    """ 更新客户端脚本文件 """
    ftp_download_file(cfg["ftp_scripts"], filename)
    temp_file = uncompress_file(filename)
    move_files(temp_file+"/script", cfg["local_path"]+"/zys_Data/StreamingAssets")
    print(u"客户端脚本更新完毕。")
    # 删除缓存解压文件目录
    clear_files(cfg["local_path"]+"/"+temp_file)


def main():
    """ 命令行调用不同更新模式 """
    help_msg = "-h: help document\n" \
               "-a: update all files\n" \
               "-s: only update scripts\n"

    try:
        options, args = getopt.getopt(sys.argv[1:], "has", ["help", "all", "scripts"])

        if not options:
            print("invalid arguments, please input:")
            print(help_msg)

    except getopt.GetoptError as e:
        print(help_msg)
        sys.exit()

    for name, value in options:
        if name in ("-h", "--help"):
            print(help_msg)
        elif name == "-a":
            update_packages()
        elif name == "-s":
            update_scripts()


if __name__ == "__main__":
    # update_scripts()
    # update_packages()
    main()
