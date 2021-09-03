#-*- coding: utf-8 -*-
import os
import re
import sys

file_path='/home/zhangmeng/文档/database/other/3/open_address_lottery.sol'
def get_root(file_dir,function_name):
    for root, dirs, files in os.walk(file_dir):
        for i in range(0,len(files)):
            try:
                if(re.search(function_name,files[i]).group()):
                    return root + '/' + files[i]
            except:
                continue



''' print(root)  # 当前目录路径
        print(dirs)  # 当前路径下所有子目录
        print(files)  # 当前路径下所有非目录子文件
'''
#获得相应的function_name，输出是对应的lsit
def get_function_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        function_name=list()
        pattern=re.compile('(?<=-)[^}]*?(?=\()')
        for i in range(0,len(files)):
            try:
                if(re.search(pattern,files[i]).group()):
                    str_y=re.search(pattern,files[i]).group()
                    function_name.append(str_y)
            except:
                continue
        for m in range(0,len(function_name)):
            try:
                if(function_name[m]=='slitherConstructorConstantVariables'):
                    del function_name[m]
            except:
                print('none')
    return (function_name)
#输出合约名字和绝对路径
def get_file_sol_name(file_path):
    temp_name=file_path.split('/')
    root_path=temp_name[0]
    sol_name=temp_name.pop()
    for i in range(1,len(temp_name)):
        root_path=root_path+'/'+temp_name[i]
    return root_path,sol_name

root_path,sol_name=get_file_sol_name(file_path) #采用的合约名字
#print(root_path)  合约所在目录地址
function_name=get_function_name(root_path)

print(function_name) #合约function名字，依赖于dot文件

temp_str=list()
for i in range(0,len(function_name)):
    temp_str.append(get_root(root_path,function_name[i]))  #绝对地址list
