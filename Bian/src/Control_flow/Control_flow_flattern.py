#encoding:utf-8
#对提取每个基本块，对基本块进行排列，使用不透明谓词构造next来确定数目；关于创建分支则是根据用户自定义比例进行分支添加数量的限定，创建怎么样的分支还是个问题
import ReadFile
import Control_flow
import os
import re
import sys
import auto_get_root
import collections
from operator import length_hint
#endRaffle  chooseWinner
function_name=auto_get_root.function_name[0]
test_url=auto_get_root.temp_str
#获取dot文件的每段,start_list,end_list.返回分好组的函数段str_text_list
def dot_file_pre(file_path):
    start_list = []
    str_text_list=list()
    temp_text_list = list()
    i = 0
    end_list = []
    with open(file_path) as file_object:
        lines = file_object.readlines()
    for line in lines[:]:
        mystr = line
        i = i + 1
        pattern = re.compile('^\d{1,}\[')  # 正则表达式匹配行号数字以及需要匹配的关键词
        if (re.search(pattern, mystr)):
            start_list.append(i)
    for i in range(1,len(start_list)):
        end_list.append(start_list[i]-1)
    temp_end_list=len(lines)-1
    end_list.append(temp_end_list)
    for i in range(0,len(start_list)):
        x_str=ReadFile.read_need_partical_File(file_path,start_list[i]-1,end_list[i])
        str_text_list.append(x_str)
    return (str_text_list)
#字符串中数字提取
def get_num_from_string(str_list):
    s = ','.join(str(s) for s in str_list if
                 s not in ['NONE', 'NULL'])  # 将list——start转化为相应的string类型，由于list_start中含有数字，不能直接转化
    # print(s)
    new_str = ""  # 创建一个空字符串
    for ch in s:
        if ch.isdigit():  # 字符串中的方法，可以直接判断ch是否是数字
            new_str += ch
        else:
            new_str += " "
    sub_list = new_str.split()  # 对新的字符串切片
    num_list = list(map(int, sub_list))  # map方法，使列表中的元素按照指定方式转变
    return num_list

def order(str_text_list):
    temp_text_list = list()
    temp_num_list=[]
    for i in range(0,len(str_text_list)):
        if(re.search('ENTRY_POINT',str_text_list[i])):#代表了开端
            temp_text_list.append(' uint next=1; while(next!=0){ ')
        elif(re.search(' IF ',str_text_list[i])):#代表了if语句
            temp_text_1=re.search('(?<=EXPRESSION:)[^}]*?(?=IR)',str_text_list[i]).group()  #获得了条件
            temp_text_2=(re.findall('(?<=\d->)[^}]*?(?=\[)',str_text_list[i]))       #获得后继
            temp_text_3=get_num_from_string(temp_text_2)
            temp_text = 'else if( next==' + str(i) + ') {' + 'if (' + temp_text_1 + ') '
            temp_text=temp_text+' next= '+str(temp_text_3[0])+'; else next= '+str(temp_text_3[1])+'; }'
            temp_text_list.append(temp_text)
        elif(re.search('Type: EXPRESSION',str_text_list[i])):#代表了普通表达式
            temp_text_1 = re.search('(?<=EXPRESSION:)[^}]*?(?=IR)', str_text_list[i]).group()  # 获得了条件   没有后继了
            temp_text='else if(next== ' + str(i) + ') { ' +temp_text_1+';'
            if (re.search('(?<=\d->)[^}]*?(?=;)', str_text_list[i])):
                temp_text_2 = (re.findall('(?<=\d->)[^}]*?(?=;)', str_text_list[i]))  # 获得后继
                temp_text_3 = get_num_from_string(temp_text_2)
            else:
                temp_text_3 = [0]
            temp_text = temp_text + ' next= ' + str(temp_text_3[0]) + '; }'
            temp_text_list.append(temp_text)
        elif(re.search(('Type: RETURN'),str_text_list[i])):
            temp_text = 'else if(next== ' + str(i) + ') return;'
            temp_text_list.append(temp_text)
        elif(re.search('END_IF',str_text_list[i])):
            temp_text = 'else if(next== ' + str(i) + '){  '
            if(re.search('(?<=\d->)[^}]*?(?=;)', str_text_list[i])):
                temp_text_2 = (re.findall('(?<=\d->)[^}]*?(?=;)', str_text_list[i]))  # 获得后继
                temp_text_3 = get_num_from_string(temp_text_2)
            else:
                temp_text_3=[0]
            temp_text = temp_text + ' next= ' + str(temp_text_3[0]) + '; }'
            temp_text_list.append(temp_text)
        elif (re.search('Type: NEW VARIABLE', str_text_list[i])):  # 代表了普通表达式
            temp_text_1 = re.search('(?<=EXPRESSION:)[^}]*?(?=IR)', str_text_list[i]).group()  # 获得了条件
            temp_text = 'else if(next== ' + str(i) + ') { ' + temp_text_1+';'
            if (re.search('(?<=\d->)[^}]*?(?=;)', str_text_list[i])):
                temp_text_2 = (re.findall('(?<=\d->)[^}]*?(?=;)', str_text_list[i]))  # 获得后继
                temp_text_3 = get_num_from_string(temp_text_2)
            else:
                temp_text_3 = [0]
            temp_text = temp_text + ' next= ' + str(temp_text_3[0]) + '; }'
            temp_text_list.append(temp_text)
        elif (re.search('BEGIN_LOOP', str_text_list[i])):
            temp_text = 'else if(next== ' + str(i) + ') { '
            temp_text_2 = (re.findall('(?<=\d->)[^}]*?(?=;)', str_text_list[i]))  # 获得后继
            temp_text_3 = get_num_from_string(temp_text_2)
            temp_text = temp_text + ' next= ' + str(temp_text_3[0]) + '; }'
            temp_text_list.append(temp_text)
        elif (re.search(' IF_LOOP ', str_text_list[i])):  # 代表了循环语句
            temp_text_1 = re.search('(?<=EXPRESSION:)[^}]*?(?=IR)', str_text_list[i]).group()  # 获得了条件
            temp_text_2 = (re.findall('(?<=\d->)[^}]*?(?=;)', str_text_list[i]))  # 获得后继
            temp_text_3 = get_num_from_string(temp_text_2)
            temp_text = 'else if( next== ' + str(i) + ')' + '{ if (' + temp_text_1 + ') '
            temp_text = temp_text + ' next= ' + str(temp_text_3[0]) + '; else next= ' + str(temp_text_3[1])+'; }'
            temp_text_list.append(temp_text)
        elif (re.search('END_LOOP', str_text_list[i])):
            temp_text = 'else if(next== ' + str(i) + ') {  '
            if (re.search('(?<=\d->)[^}]*?(?=;)', str_text_list[i])):
                temp_text_2 = (re.findall('(?<=\d->)[^}]*?(?=;)', str_text_list[i]))  # 获得后继
                temp_text_3 = get_num_from_string(temp_text_2)
            else:
                temp_text_3 = [0]
            temp_text = temp_text + ' next= ' + str(temp_text_3[0]) + '; }'
            temp_text_list.append(temp_text)

    temp_text_list.append('} }')
    temp_text_4=re.sub('else if','if',temp_text_list[1])
    temp_text_list[1]=temp_text_4
    return temp_text_list





