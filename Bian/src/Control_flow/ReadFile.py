#encoding:utf-8
import os
import re
import sys
import auto_get_root
import collections
from operator import length_hint
test_url='/home/zhangmeng/文档/PycahrmProject/project1/test_if_while_match.sol'
reset_url='/home/zhangmeng/文档/PycahrmProject/project1/'
test_start=5
test_end=11
#预先处理源文件，把源文件的else替换到下一行中去
def Pre_deal_source_file(file_path):
    mystr = read_file_as_str(file_path)
    savedStdout = sys.stdout  # 保存标准输出流
    with open(file_path,'wt') as file_object:
        pattern = re.compile('else {' )  # 正则表达式匹配 else {
        list_start = re.findall(pattern, mystr)
        length_list=len(list_start)
        mystr = re.sub('else {', '  \nelse {', mystr, length_list)  # 将else放置在下一行
        sys.stdout = file_object  # 标准输出重定向至文件
        sys.stdout = savedStdout

#删除带有行号的文件的注释，直接在带有行号的文件中直接操作，没有返回值。
def delete_note_in_numberFile(file_path):
    root_path, sol_name = auto_get_root.get_file_sol_name(file_path)  # 采用的合约名字
    mystr=read_file_as_str(file_path)
    mystr = re.sub('//(.)*(\n)?','', mystr)  # 替换
    mystr = re.sub('/\*((.)|((\r)?\n))*?\*/','', mystr)
    os.chdir(root_path)
    savedStdout = sys.stdout
    with open(sol_name+'_test.sol', 'wt') as file:
        sys.stdout = file  # 标准输出重定向至文件
        print(mystr)
    sys.stdout = savedStdout
    delete_blank(file_path+'_test.sol')
    file_path_next=file_path+'_test.sol'
    return file_path_next
#删除文件空行
def delete_blank(file_path_next):
    mystr_list=list()
    mystr_list_next=list()
    with open(file_path_next) as file_object:
        lines = file_object.readlines()
    for line in lines[:]:
        if(line.rstrip()):
            mystr_list.append(line.rstrip())
    savedStdout = sys.stdout
    with open(file_path_next, 'wt') as file:
        sys.stdout = file  # 标准输出重定向至文件
        for i in mystr_list:
            print(i)
    sys.stdout = savedStdout


#输出带有行号的文件内容，它只是一个数据预处理的中转站,输出行号+原先文件内容。
def Input_file_with_number(file_path):
    file = open(file_path, "r")
    for num, value in enumerate(file):
       print ("%s, %s" % (num, value))
    file.close()

#制作行号版本的文件，创建新文件，返回文件名
def make_sequence_num(file_path):

    file_name = os.path.basename(file_path)
    file_name = file_name.split('.')[0]
    savedStdout = sys.stdout  # 保存标准输出流
    with open(file_name+'with number.txt', 'wt') as file:
        sys.stdout = file  # 标准输出重定向至文件
        Input_file_with_number(file_path)

    sys.stdout = savedStdout  # 恢复标准输出流
    file_name=reset_url+file_name+'with number.txt'
    delete_note_in_numberFile(file_name)
    return (file_name)

#验证读取的文件是str类型，返回全部文件内容
def read_file_as_str(file_path):
    # 判断路径文件存在
    if not os.path.isfile(file_path):
        raise TypeError(file_path + " does not exist")
    all_the_text = open(file_path).read()
    #print(type(all_the_text))  注释掉返回的文件类型
    return (all_the_text)

#获得需要的文件行号,返回正则匹配的结果行号,格式为list类型
def get_sequence_num(file_path,aim_str):
    #print(file_path)
    mystr=read_file_as_str(file_path)
    with open(file_path) as file_object:
        #pattern=re.compile(r'(\d[0-9])+(\,).+(label)')
        #pattern = re.compile(r'(\d[0-9]|\d)+.+'+aim_str)#正则表达式匹配行号数字以及需要匹配的关键词
        pattern = re.compile(r'(\d{1,3})+.+'+aim_str)#正则表达式匹配行号数字以及需要匹配的关键词
        list_start=re.findall(pattern,mystr)
        #print(list_start)
    s=','.join(str(s) for s in list_start if s not in ['NONE', 'NULL']) #将list——start转化为相应的string类型，由于list_start中含有数字，不能直接转化
   # print(s)
    new_str = ""  # 创建一个空字符串
    for ch in s:
        if ch.isdigit():  # 字符串中的方法，可以直接判断ch是否是数字
            new_str += ch
        else:
            new_str += " "
    sub_list = new_str.split()  # 对新的字符串切片
    num_list = list(map(int, sub_list))  # map方法，使列表中的元素按照指定方式转变
    #print(num_list)
    return num_list

#对获取的list类型的行号进行匹配,！！！输出分支数组和全部元素在一起的数组！！！！！！这四个输入一定要考虑异常抛出的问题!!!!,输出对应后的顺序序列
def match_sequence_total_number(if_list_num,signal_list_num):
    #signal_list_num.pop()
    t = len(if_list_num+signal_list_num)
    temp_list_num = list(range(t))
    stack_list_num=[]#模拟栈列表
    start_num_list=[]
    end_num_list=[]
    for i in range(0,t):
        if(i<len(if_list_num)):
            temp_list_num[i]=if_list_num[i]
        else:
            temp_list_num[i]=signal_list_num[t-i-1]
    temp_list_num.sort()
    for i in range(0,len(temp_list_num)):
        if temp_list_num[i] not in if_list_num:
            end_num=temp_list_num[i]
            start_num=stack_list_num.pop()#pop(0)从头算作栈顶，pop()从尾算作栈顶
            start_num_list.append(start_num)
            end_num_list.append(end_num)
        else:
            stack_list_num.append(temp_list_num[i])
    return start_num_list,end_num_list

#就标记了相应的label，输出的是含有label的list序列
def label_need_sequence(file_path):
    mystr=read_file_as_str(file_path)
    pattern=re.compile('label')
    str_start=re.findall(pattern,mystr)
    #print(str_start)
    return (str_start)

#读取我需要行数中的文件
def read_need_partical_File(file_path,start_num,end_num):
    str_text=''
    str_text_1=''
    with open(file_path) as file_object:
      lines = file_object.readlines()
    '''
    for line in lines[start_num:end_num]:
        join_text=line.rstrip()+'\n'
        str_text=str_text+join_text
        '''
    for line in lines[start_num:end_num]:
        join_text_1=line.rstrip()+'\n'
        str_text_1=str_text_1+join_text_1
    return str_text_1

#重新设置了行号和其它玩意，使用的是源文件的内容
def re_get_num(file_path):
    start_list=[]
    i=0
    end_list=[]
    with open(file_path) as file_object:
        lines = file_object.readlines()
    for line in lines[:]:
        mystr=line
        i=i+1
        try:
            pattern = re.compile('   if')  # 正则表达式匹配行号数字以及需要匹配的关键词
            if(re.search(pattern, mystr)):
                start_list.append(i)
        except:
            print('No if')
        try:
            pattern = re.compile('   while')  # 正则表达式匹配行号数字以及需要匹配的关键词
            if(re.search(pattern, mystr)):
                start_list.append(i)
        except:
            print('No while')
        try:
            pattern = re.compile('   else')  # 正则表达式匹配行号数字以及需要匹配的关键词
            if(re.search(pattern, mystr)):
                start_list.append(i)
        except:
            print('No else')
        try:
            pattern = re.compile('   }')  # 正则表达式匹配行号数字以及需要匹配的关键词
            if (re.search(pattern, mystr)):
                end_list.append(i)
        except:
            print('')
    return(start_list,end_list)

def for_flattern_get_num(file_path):
    start_list = []
    i = 0
    end_list = []
    with open(file_path) as file_object:
        lines = file_object.readlines()
        print(len(lines))
    for line in lines[:]:
        mystr = line
        i = i + 1
        try:
            pattern = re.compile('   if')  # 正则表达式匹配行号数字以及需要匹配的关键词
            if(re.search(pattern, mystr)):
                start_list.append(i)

        except:
            print('No if')
        try:
            pattern = re.compile('else if')  # 正则表达式匹配行号数字以及需要匹配的关键词
            if(re.search(pattern, mystr)):
                start_list.append(i)
        except:
            print('No else if')
        try:
            pattern = re.compile('   }')  # 正则表达式匹配行号数字以及需要匹配的关键词
            if (re.search(pattern, mystr)):
                end_list.append(i)
        except:
            print('')

        return (start_list, end_list)


#read_need_partical_File(test_url,test_start,test_end)
#read_file_as_str(test_url)
#label_need_sequence(test_url)
#get_sequence_num(make_sequence_num(test_url),'label')
#s=make_sequence_num(test_url)
#print(s)
#read_need_partical_File(test_url,1,5)
#read_need_partical_File(make_sequence_num(test_url),1,5)  对于截取而言，我不需要行号的。所以该操作是错误的
#delete_notes(test_url)
#delete_note_in_numberFile(make_sequence_num(test_url))
#get_sequence_num_for_special_signal(make_sequence_num(test_url))
#Pre_deal_source_file(test_url)    不要忘了最后清理空白行，或者将他变成无空格的代码段
#test_url_next=make_sequence_num(test_url)
#print(test_url_next)
#start_num_list,end_num_list=match_sequence_total_number(get_sequence_num(test_url_next,'if'),get_sequence_num(test_url_next,'while'),get_sequence_num_for_special_signal(test_url_next),get_sequence_num(test_url_next,'else'))
#print(start_num_list,end_num_list)#获得了匹配好的开始与结束括号
#transform(test_url,start_num_list,end_num_list)
#if_num_list,signal_num_list=re_get_num(test_url)
#start_num_list,end_num_list=match_sequence_total_number(if_num_list,signal_num_list)

