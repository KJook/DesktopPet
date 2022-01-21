import os
import shutil
import zipfile

def zip_compress(to_zip,save_zip_name):#save_zip_name是带目录的，也可以不带就是当前目录
#1.先判断输出save_zip_name的上级是否存在(判断绝对目录)，否则创建目录
    save_zip_dir=os.path.split(os.path.abspath(save_zip_name))[0]#save_zip_name的上级目录
    print(save_zip_dir)
    if not os.path.exists(save_zip_dir):
        os.makedirs(save_zip_dir)
        print('创建新目录%s'%save_zip_dir)
    f = zipfile.ZipFile(os.path.abspath(save_zip_name),'w',zipfile.ZIP_DEFLATED)
# 2.判断要被压缩的to_zip是否目录还是文件，是目录就遍历操作，是文件直接压缩
    if not os.path.isdir(os.path.abspath(to_zip)):#如果不是目录,那就是文件
        if os.path.exists(os.path.abspath(to_zip)):#判断文件是否存在
            f.write(to_zip)
            f.close()
            print('%s压缩为%s' % (to_zip, save_zip_name))
        else:
            print ('%s文件不存在'%os.path.abspath(to_zip))
    else:
        if os.path.exists(os.path.abspath(to_zip)):#判断目录是否存在，遍历目录
            zipList = []
            for dir,subdirs,files in os.walk(to_zip):#遍历目录，加入列表
                for fileItem in files:
                    zipList.append(os.path.join(dir,fileItem))
                    # print('a',zipList[-1])
                for dirItem in subdirs:
                    zipList.append(os.path.join(dir,dirItem))
                    # print('b',zipList[-1])
            #读取列表压缩目录和文件
            for i in zipList:
                f.write(i,i.replace(to_zip,''))#replace是减少压缩文件的一层目录，即压缩文件不包括to_zip这个目录
                # print('%s压缩到%s'%(i,save_zip_name))
            f.close()
            print('%s压缩为%s' % (to_zip, save_zip_name))
        else:
            print('%s文件夹不存在' % os.path.abspath(to_zip))


source_path_resourses = './resourses'
target_path_resourses = "./dist/resourses"
if os.path.exists(target_path_resourses):
    shutil.rmtree(target_path_resourses)


source_path_pets = './pets'
target_path_pets = "./dist/pets"
if os.path.exists(target_path_pets):
    shutil.rmtree(target_path_pets)

source_path_script = './script'
target_path_script = "./dist/script"
if os.path.exists(target_path_script):
    shutil.rmtree(target_path_script)


shutil.copytree(source_path_resourses, target_path_resourses)
shutil.copytree(source_path_pets, target_path_pets)
shutil.copytree(source_path_script, target_path_script)
# shutil.copy('./conf.json', './dist/conf.json')
os.remove('./dist/script/script.py')
# 虚拟环境下pyinstaller
os.system("E:\Environment\Anaconda\envs\DesktopPet\Scripts\pyinstaller -F -i ./resourses/bitbug_favicon.ico main.py")

print("打包zip文件")

zip_compress('./dist', './DesktopPet_win_amd64.zip')

print("打包结束")