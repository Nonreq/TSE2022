#encoding:utf-8
#添加分支选项:把全局层次作为一个整体,顺序动态不透明谓词方法.把每个分支作为一个基本块,每次插入50%分支数目
import ReadFile
import Control_flow
import os
import re
import sys
import collections
from operator import length_hint
test_url='/home/zhangmeng/文档/PycahrmProject/project1/test_if_while_match.sol'
reset_url='/home/zhangmeng/文档/PycahrmProject/project1/'
#获取一系列的函数块的具体值,输出是str类型的list
def partical_block(file_path,start_num_list_modify,end_num_list_modify):
    basic_text_only_if=list()
    for i in range(0,len(start_num_list_modify)):
        basic_text_only_if.append(ReadFile.read_need_partical_File(file_path,start_num_list_modify[i]-1,end_num_list_modify[i]))
    return basic_text_only_if
#调整start_num_list的格式,将内嵌函数给覆盖掉
def adjust_start(start_num_list,end_num_list):
    excess_num=[]
    start_num_list_modify=[]
    end_num_list_modify = []
    for i in range(0,len(start_num_list)):
        for j in range(i,len(end_num_list)):
            if(end_num_list[i]>end_num_list[j]):
                excess_num.append(j)
    for x in range(0,len(excess_num)):
        start_num_list[excess_num[x]]=0
        end_num_list[excess_num[x]] = 0
    for i in range(0,len(start_num_list)):
        if(start_num_list[i]!=0):
            start_num_list_modify.append(start_num_list[i])
            end_num_list_modify.append(end_num_list[i])
    #print(start_num_list_modify,end_num_list_modify)
    return start_num_list_modify,end_num_list_modify
#修改start_list和end_list的顺序
def modify_start_list(start_num_list,end_num_list):
    for i in range(0,len(start_num_list)-1):
        for j in range(i,len(start_num_list)-1):
            if(start_num_list[j]>start_num_list[j+1]):
                temp_num_list=start_num_list[j]
                start_num_list[j]=start_num_list[j+1]
                start_num_list[j+1]=temp_num_list
                temp_num_list_1=end_num_list[j]
                end_num_list[j]=end_num_list[j+1]
                end_num_list[j+1]=temp_num_list_1
#构造基本块,返回list类型的基本块
def total_basic_block(file_path,start_num_list,end_num_list,basic_text_only_if):
    complicate_list_num=[]
    str_text=''
    str_text_final=list()
    join_text=''
    join_text_1=''
    with open(file_path) as file_object:
        lines = file_object.readlines()
    for i in range(0,len(start_num_list)):
        j=start_num_list[i]
        while(j<=end_num_list[i]):
            complicate_list_num.append(j)
            j = j + 1

    for i in range(1,len(lines)):
        if i in complicate_list_num:
            complicate_list_num.pop(0)
            str_text=str_text+join_text
        else:
            join_text_1=lines[i]
            str_text=str_text+join_text_1
    str_text_x=re.sub('\{',';',str_text)
    str_text_delete_n = re.sub('(\\n)( )*', '', str_text_x)
    str_text_final_pre=str_text_delete_n.split(';')
    for i in range(0,len(str_text_final_pre)):
        if(str_text_final_pre[i]!=''):
            str_text_final.append(str_text_final_pre[i])
    for i in range(0,len(str_text_final)):
        str_text_final[i]=str_text_final[i]+';'
    j=0
    for i in range(0,len(str_text_final)):
        if(re.search('if \(.*\)',str_text_final[i])):
            str_text_final[i]=basic_text_only_if[j]
            j=j+1
        elif(re.search('while \(.*\)',str_text_final[i])):
            str_text_final[i] = basic_text_only_if[j]
            j = j + 1
    return str_text_final
#添加分支完成-----------------add 100%||自我迭代达成效果_自我迭代需要一个跳出条件-----num>2?
def add_if_choice_again(basic_text):
    DOP='x^2>0'
    list=[1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
    num=int(len(basic_text)/2)+1   #谓词个数,每段长度为2完事
    str_text=Control_flow.str_text[0]+' { \n'
    temp_num=0
    temp_num_1=0
    for y in range(0,num):
        if (temp_num + 2 >= len(basic_text)):
            temp_str = 'if (' + DOP + ')  { \n'
            str_text = str_text + temp_str
            for i in range(temp_num, len(basic_text)):
                str_text = str_text + basic_text[i] + '\n'
            str_text = str_text + ' } \n' + 'else { \n'
            for i in range(temp_num_1, len(basic_text)):
                str_text = str_text + basic_text[i] + '\n'
            str_text = str_text + ' }\n '
            str_text = str_text + '############\n'
            break
        temp_str = 'if (' + DOP + ')  { \n'
        str_text = str_text + temp_str
        for i in range(temp_num, temp_num+2):
            str_text = str_text + basic_text[i] + '\n'
        str_text = str_text + ' } \n' + 'else { \n'
        for i in range(temp_num_1, temp_num_1+list[y] ):
            str_text = str_text + basic_text[i] + '\n'
        str_text = str_text + ' }\n '
        str_text = str_text + '############\n'
        temp_num=temp_num+2
        temp_num_1=temp_num_1+list[y]
    str_text_split = str_text.split('############\n')
    for i in range(0, len(str_text_split)):
        str_text_split[i] = re.sub('\\n', '', str_text_split[i])
    str_text_final=str_text.split('#')
    print(str_text)




#深度优先进行插入分支-------------------add 50%
def add_if_choice(basic_text):
    DOP='x^2>0'
    list=[1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
    num=int(len(basic_text)/2)+1   #谓词个数,每段长度为2完事
    str_text=Control_flow.str_text[0]+' { \n'
    temp_num=0
    temp_num_1=0
    for y in range(0,num):
        if (temp_num + 2 >= len(basic_text)):
            temp_str = 'if (' + DOP + ')  { \n'
            str_text = str_text + temp_str
            for i in range(temp_num, len(basic_text)):
                str_text = str_text + basic_text[i] + '\n'
            str_text = str_text + ' } \n' + 'else { \n'
            for i in range(temp_num_1, len(basic_text)):
                str_text = str_text + basic_text[i] + '\n'
            break
        temp_str = 'if (' + DOP + ')  { \n'
        str_text = str_text + temp_str
        for i in range(temp_num, temp_num+2):
            str_text = str_text + basic_text[i] + '\n'
        str_text = str_text + ' } \n' + 'else { \n'
        for i in range(temp_num_1, temp_num_1+list[y] ):
            str_text = str_text + basic_text[i] + '\n'
        temp_num=temp_num+2
        temp_num_1=temp_num_1+list[y]
    print(str_text)



start_num_list=ReadFile.start_num_list
end_num_list=ReadFile.end_num_list
modify_start_list(start_num_list,end_num_list)
#print(start_num_list,end_num_list)

start_num_list_modify,end_num_list_modify=adjust_start(start_num_list,end_num_list)
basic_text_only_if = partical_block(test_url, start_num_list_modify, end_num_list_modify)
partical_block(test_url,start_num_list_modify,end_num_list_modify)
basic_text=total_basic_block(test_url,start_num_list,end_num_list,basic_text_only_if)
add_if_choice(basic_text)