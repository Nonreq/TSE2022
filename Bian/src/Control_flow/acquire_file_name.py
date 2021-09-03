import os
test_url='/home/zhangmeng/文档/PycahrmProject/project1/Ethraffle_v4b.dot'
file_name = os.path.basename(test_url)
print(file_name)
# 输出为 test.py
file_name = file_name.split('.')[0]
print(file_name)