import zipfile 
 
#解压zip文件 
def unzip(package_path, dest): 
    myzip=zipfile.ZipFile(package_path, 'r') 
    for name in myzip.namelist():
        myzip.extract(name, dest)
        f_handle=open(dest+name,"wb") 
        f_handle.write(myzip.read(name))
        f_handle.close() 
    myzip.close() 

#添加文件到已有的zip包中 
def addzip(package_path, src): 
    f = zipfile.ZipFile(package_path,'w',zipfile.ZIP_DEFLATED) 
    f.write(src) 
    f.close() 

#把整个文件夹内的文件打包 
def adddirfile(package_path, src): 
    f = zipfile.ZipFile(package_path,'w',zipfile.ZIP_DEFLATED) 
    for dirpath, dirnames, filenames in os.walk(src): 
        for filename in filenames: 
            f.write(os.path.join(dirpath,filename)) 
    f.close() 
