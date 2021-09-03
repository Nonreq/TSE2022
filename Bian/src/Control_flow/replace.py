#-*- coding: utf-8 -*-
import os
import re
import sys
import auto_get_root
import ReadFile
import Control_flow_flattern
file_path=auto_get_root.file_path
function_name=auto_get_root.function_name
root_path=auto_get_root.root_path
file_path_next=ReadFile.delete_note_in_numberFile(file_path) #生成无注释文件

#将选择到function部分作为空格，等待输入,并且回传出修复好程序
def blank_sol_function(file_path_next,function_name):
    function_list=[]
    function_match=list()
    mystr_list=list()
    aim_str = list()
    i=1
    with open(file_path_next) as file_object:
        lines = file_object.readlines()
        for line in lines[:]:
            mystr=line
            mystr_list.append(line.strip())
            pattern = re.compile('(?<=function)[^}]*?(?=\()')  # 正则表达式匹配行号数字以及需要匹配的关键词
            if(re.search(pattern,mystr)):
                function_list.append(i)
                function_match.append(re.search(pattern,mystr).group().strip())
            if(re.search('}',mystr)):
                signal_num=i;
            i = i + 1
        function_list.append(signal_num)
        print(function_name)
        print(function_match)
        for n in range(0, len(function_name)):
            for m in range(0,len(function_match)):
                if(function_name[n]==function_match[m]):
                    print(m)
                    test_url=auto_get_root.get_root(root_path,function_match[m])
                    for u in range(function_list[m], function_list[m + 1] - 1):
                        mystr_list[u]=''
                    str_list=Control_flow_flattern.dot_file_pre(test_url)
                    aim_str=Control_flow_flattern.order(str_list)
                    for k in range(0,len(aim_str)):
                        mystr_list[function_list[m]]=mystr_list[function_list[m]]+aim_str[k]
    print(function_list)
    savedStdout = sys.stdout
    with open(file_path_next, 'wt') as file:
        sys.stdout = file  # 标准输出重定向至文件
        for i in mystr_list:
            print(i)
    sys.stdout = savedStdout
print('当前文件为：',file_path)
blank_sol_function(file_path_next,function_name)