#encoding:utf-8
#对提取每个基本块，对基本块进行排列，使用不透明谓词构造next来确定数目；关于创建分支则是根据用户自定义比例进行分支添加数量的限定，创建怎么样的分支还是个问题
import ReadFile
import os
import re
import sys
import collections
from operator import length_hint
test_url='/home/zhangmeng/文档/PycahrmProject/project1/test_if_while_match.sol'
reset_url='/home/zhangmeng/文档/PycahrmProject/project1/'
#开始构建彼此间的顺序
def control_flow_order(str_text_total,str_text_partical):
    #print(str_text_total)
    str_text=str_text_total
    data_text=list()
    for i in range (0,len(str_text_total)):
        temp_str_delete_n=re.sub('(\\n)( )*','',str_text_total[i])
        str_text[i]=temp_str_delete_n
    data_text.append(str_text[0]+'{')
    for i in range(1,len(str_text)):
        temp_str='elif (next='+str(i)+')'+'{'
        if(re.search('if',str_text[i])):
            temp_str=temp_str+str_text[i]+'{'
            data_text.append(temp_str)
        elif(re.search('while',str_text[i])):
            re.sub('while','if',str_text[i],1)
            temp_str=temp_str+str_text[i]+'{'
            data_text.append(temp_str)
        else:
            temp_str=temp_str+str_text[i]+';'
            data_text.append(temp_str)


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




#获得函数整体的变化从function开始
def total_basic_block(file_path,start_num_list):
    complicate_list_num=[]
    str_text=''
    join_text=''
    join_text_1=''
    with open(file_path) as file_object:
        lines = file_object.readlines()
    for i in range(0,len(start_num_list)):
        if(i>0):
            if(start_num_list[i]<start_num_list[i-1]):
                start_num=start_num_list[i]-1#行数和line的计数方式不一样
                complicate_list_num.append(start_num)
    for i in range(0,len(lines)):
        if i in complicate_list_num:
            join_text_1=lines[i]
            join_text=re.sub('\{', ';', join_text_1, 1)
            complicate_list_num.pop(0)
            str_text=str_text+join_text
            #print(str_text)
        else:
            join_text_1=lines[i]
            str_text=str_text+join_text_1
    #print(str_text)
    temp_str_delete_signal = re.sub('\{', ';', str_text, 1)  # 删掉开始的{
    temp_str_blcok_pre = re.sub('\{(?<=\{)[^}]*?(?=\})\}', ';', temp_str_delete_signal)  # 获取{}中的函数块
    temp_str_1=re.sub('\}','};',temp_str_blcok_pre)
    final_str=temp_str_1.split(';')#把 } 后面也加了分号
    #print(final_str)
    return final_str

#这个是获得分支阶段的基本的函数块和函数语句的获得，输出函数语句+函数块，均为string类型
def basic_block(file_path,start_num_list,end_num_list):
    #ReadFile.re_get_num(test_url)
    temp_str=list()
    for i in range(0,len(start_num_list)):
        str_text=ReadFile.read_need_partical_File(file_path,start_num_list[i]-1,end_num_list[i])
        #print(str_text)
        temp_str_front = str_text.split('{') #获取了IF (xxx)
        #print(temp_str_front[0])     #这个是条件语句
        #获取内部的子集成分
        temp_str_delete_signal=re.sub('\{','',str_text,1)
        #print(temp_str_delete_signal)  #这个是删除了函数条件的  {
        temp_str_blcok_pre = re.sub('\{(?<=\{)[^}]*?(?=\})\}', ';',temp_str_delete_signal)#获取{}中的函数块
        #print(temp_str_blcok_pre)          #这个包含了函数的条件
        temp_str_blcok_pre_pre=re.search('(?<=\))[^}]*?(?=\})|(?<=else)[^}]*?(?=\})',temp_str_blcok_pre).group()
        temp_str.append(temp_str_blcok_pre_pre)
    return (temp_str)#这个是最终的得到结果，字符串形式的函数块集合












ReadFile.delete_note_in_numberFile(test_url)

if_num_list,signal_num_list=ReadFile.re_get_num(test_url)
start_num_list,end_num_list=ReadFile.match_sequence_total_number(if_num_list,signal_num_list)

str_text_partical=basic_block(test_url,start_num_list,end_num_list)
str_text=total_basic_block(test_url,start_num_list)
modify_start_list(start_num_list,end_num_list)
control_flow_order(str_text,str_text_partical)

