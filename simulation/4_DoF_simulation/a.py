def say_hello(*args):
    print('hello {0}'.format(args))

# 通过位置传值
say_hello('jack', 'tom')
def func_b(**kwargs):
    print(kwargs)

# 通过关键字传值
func_b(a=1, b=2)
def say_hello(name):
    print('hello {0}'.format(name))

# 通过位置传值
say_hello('jack')
# 通过关键字传值
say_hello(name='tom')
def func_b(*args, a, b):
    print(args, a, b)

# 只能通过关键字传值
func_b('test', a=1, b=2)