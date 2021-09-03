import os
import sys


savedStdout = sys.stdout  #保存标准输出流
with open('./hello', 'wt') as file:
    sys.stdout = file  #标准输出重定向至文件
    print('This message is for file!')


sys.stdout = savedStdout  #恢复标准输出流
print ('This message is for screen!')
