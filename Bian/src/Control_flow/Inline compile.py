#encoding:utf-8
import os
import re
import sys
import collections
from operator import length_hint
test_url='/home/zhangmeng/文档/PycahrmProject/project1/test_if_while_match.sol'
reset_url='/home/zhangmeng/文档/PycahrmProject/project1/'
test_start=5
test_end=11
import ReadFile
#第二步是对分号进行截取，前提是使用 { 来进行选取其中内容
def complicate_re_deal_second_setence(str_text):
    temp_str=re.search('(?<=\{)[^}]*?(?=\})',str_text).group()
    temp_str_divide=temp_str.split(';')
    for i in range(0,len(temp_str_divide)-1):
        if(re.search(r'.transfer',temp_str_divide[i])):
            temp_str_0=temp_str_divide[i].split('.transfer')
            temp_str_1=re.search('(?<=\()[^}]*?(?=\))',temp_str_divide[i]).group()#msg.value
            temp_str_2=' let x := mload(0x40) mstore (x,sig)  let ret := call(g,'+temp_str_0[0].strip()+','+temp_str_1+',x,0x40,x,0x0)'
            print(temp_str_2)
            temp_str_B=re.sub(temp_str_divide[i], temp_str_2, str_text,1)
            print(temp_str_B)

#大于小于等于等这些操作集合
def set_of_operate(temp_str):
    if (re.search('>=', temp_str)):
        temp_str_A = temp_str.split('>=')
        temp_str = 'gt' + '(' + temp_str_A[0] + ',' + temp_str_A[1] + ')'
        temp_str_1 = 'eq' + '(' + temp_str_A[0] + ',' + temp_str_A[1] + ')'
        temp_str_2 = 'or' + '(' + temp_str + ',' + temp_str_1 + ')'
        x = temp_str_2
        return x

    elif (re.search('=<', temp_str)):
        temp_str_A = temp_str.split('>=')
        temp_str = 'lt' + '(' + temp_str_A[0] + ',' + temp_str_A[1] + ')'
        temp_str_1 = 'eq' + '(' + temp_str_A[0] + ',' + temp_str_A[1] + ')'
        temp_str_2 = 'or' + '(' + temp_str + ',' + temp_str_1 + ')'
        x = temp_str_2
        return x

    elif (re.search('==', temp_str)):
        temp_str_A = temp_str.split('==')
        temp_str = 'eq' + '(' + temp_str_A[0] + ',' + temp_str_A[1] + ')'
        x = temp_str
        return x

    elif (re.search('>', temp_str)):
        temp_str_A = temp_str.split('>')
        temp_str = 'gt' + '(' + temp_str_A[0] + ',' + temp_str_A[1] + ')'
        x = temp_str
        return x

    elif (re.search('<', temp_str)):
        temp_str_A = temp_str.split('<')
        temp_str = 'lt' + '(' + temp_str_A[0] + ',' + temp_str_A[1] + ')'
        x=temp_str
        return x

    else:
        temp_str_1 = 'iszero' + '(' + temp_str + ')'
        temp_str_2 = 'not' + '(' + temp_str_1 + ')'
        x = temp_str_2
        return x

#第一步转化if和while的条件问题
def cpmplicate_re_deal_first_setence_for_if(str_text):

    #if
        if (re.search('^\ *if', str_text)):
            temp_str = re.search('(?<=if \()[^}]*?(?=\))', str_text).group()  # if(pause)____pause
            if (re.search('&&',temp_str)):
                temp_str_A = temp_str.split('&&')
                temp_str_1='and'+'('
                for i in range(0,len(temp_str_A)):
                    if (i == len(temp_str_A) - 1):
                        x = set_of_operate(temp_str_A[i])
                    else:
                        x = set_of_operate(temp_str_A[i]) + ','
                    temp_str_1 = temp_str_1 + x

                temp_str_1=temp_str_1+')'
                temp_str_B = re.sub('(?<=if \()[^}]*?(?=\))', temp_str_1, str_text)
                print(temp_str_B)
            elif (re.search('\|\|',temp_str)):
                temp_str_A = temp_str.split('||')
                temp_str_1='or'+'('
                for i in range(0,len(temp_str_A)):
                    if (i == len(temp_str_A) - 1):
                        x = set_of_operate(temp_str_A[i])
                    else:
                        x = set_of_operate(temp_str_A[i]) + ','
                    temp_str_1 = temp_str_1 + x
                temp_str_1=temp_str_1+')'
                temp_str_B = re.sub('(?<=if \()[^}]*?(?=\))', temp_str_1, str_text)
                print(temp_str_B)
            else:
                x=set_of_operate(temp_str)
                temp_str_B = re.sub('(?<=if \()[^}]*?(?=\))', x, str_text)
                print(temp_str_B)


                #while
        elif(re.search('^\ *while', str_text)):
            temp_str = re.search('(?<=while \()[^}]*?(?=\))', str_text).group()  # if(pause)____pause
            if (re.search('&&', temp_str)):
                temp_str_A = temp_str.split('&&')
                temp_str_1 = 'and' + '('
                for i in range(0, len(temp_str_A)):
                    if(i==len(temp_str_A)-1):
                        x = set_of_operate(temp_str_A[i])
                    else:
                        x = set_of_operate(temp_str_A[i])+','
                    temp_str_1 = temp_str_1 + x
                temp_str_1 = temp_str_1 + ')'
                temp_str_B = re.sub('(?<=while \()[^}]*?(?=\))', temp_str_1, str_text)
                print(temp_str_B)
            elif (re.search('\|\|', temp_str)):
                temp_str_A = temp_str.split('||')
                temp_str_1 = 'or' + '('
                for i in range(0, len(temp_str_A)):
                    if (i == len(temp_str_A) - 1):
                        x = set_of_operate(temp_str_A[i])
                    else:
                        x = set_of_operate(temp_str_A[i]) + ','
                    temp_str_1 = temp_str_1 + x
                temp_str_1 = temp_str_1 + ')'
                temp_str_B = re.sub('(?<=while \()[^}]*?(?=\))', temp_str_1, str_text)
                print(temp_str_B)
            else:
                x = set_of_operate(temp_str)
                temp_str_B = re.sub('(?<=while \()[^}]*?(?=\))', x, str_text)
                print(temp_str_B)

#内容转换
def transform(file_path,start_num_list,end_num_list):
    for i in range(0,len(start_num_list)):
        str_text,str_text_1=ReadFile.read_need_partical_File(file_path,start_num_list[i]-1,end_num_list[i])
        #cpmplicate_re_deal_first_setence_for_if(str_text)
        complicate_re_deal_second_setence(str_text_1)
        #print(str_text)