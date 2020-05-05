def hello(i):
  print('This is hello: %s' % i)

def hello1(n):
  return n + 1

def hello2():
  return 1 / 0

hello(hello1(1))
hello2()
