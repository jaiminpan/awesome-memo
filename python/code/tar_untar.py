
import os
import tarfile

def tar_file(target_name, src_dir):
    #创建压缩包名
    tar = tarfile.open(target_name,"w:gz")

    #创建压缩包
    for root,dir,files in os.walk(src_dir):
        for filename in files:
            fullpath = os.path.join(root, filename)
            tar.add(fullpath)
    tar.close()

def untar_file(target_name, dest):
    tar = tarfile.open(target_name)
    for filename in tar.getnames():
        tar.extract(filename, path=dest)
    tar.close()
