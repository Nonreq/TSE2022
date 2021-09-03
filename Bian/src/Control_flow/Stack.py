class Stack():   #定义类
	def __init__(self):  #产生一个空的容器
		self.__list = []
	def push(self, item):  #入栈
		self.__list.append(item)
	def pop(self):  #出栈
		return self.__list.pop()
	def top(self):  #返回栈顶元素
		return self.__list[-1]
	def is_empty(self):  #判断是否已为空
		return not self.__list
	def size(self):  #返回栈中元素个数
		return len(self.__list)

if __name__ == '__main__':
	s = Stack()
	c = 1
	s.push('a')
	s.push('b')
	s.push(c)
	print('size:' + str(s.size()))
	print('top:' + str(s.top()))
	print(s.pop())
	print(s.pop())
	print(s.pop())
	print('size:' + str(s.size()))
