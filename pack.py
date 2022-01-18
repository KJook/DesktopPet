import os
import shutil
import zipfile

source_path_resourses = './resourses'
target_path_resourses = "./dist/resourses"
if os.path.exists(target_path_resourses):
    shutil.rmtree(target_path_resourses)


source_path_pets = './pets'
target_path_pets = "./dist/pets"
if os.path.exists(target_path_pets):
    shutil.rmtree(target_path_pets)


shutil.copytree(source_path_resourses, target_path_resourses)
shutil.copytree(source_path_pets, target_path_pets)


os.system("pyinstaller -F -w -i ./resourses/bitbug_favicon.ico main.py")

print("打包zip文件")
file_names = [target_path_resourses, target_path_pets, './dist/main.exe']
with zipfile.ZipFile('./dist/dist_win.zip', mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
    for fn in file_names:
            parent_path, name = os.path.split(fn)
            
            # zipfile 内置提供的将文件压缩存储在.zip文件中， arcname即zip文件中存入文件的名称
            # 给予的归档名为 arcname (默认情况下将与 filename 一致，但是不带驱动器盘符并会移除开头的路径分隔符)
            zf.write(fn, arcname=name)
            
            # 等价于以下两行代码
            # 切换目录， 直接将文件写入。不切换目录，则会在压缩文件中创建文件的整个路径
            # os.chdir(parent_path)
            # zf.write(name)
print("打包结束")