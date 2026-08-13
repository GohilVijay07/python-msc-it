# def sum(*args):
#     total = 0
#     for i in args:
#         total += i
#     return total 

# def mul(*args):
#     prod = 1
#     for i in args:
#         prod *= i
#     return prod

# def div(*args):
#     div = args[0]
#     for i in args[1:]:
#         div /= i
#     return div

# print("sum: ",sum(1,2,3,4,5))
# print("mul: ",mul(1,2,3,4,5))
# print("div: ",div(100,10,5,2))

# def stude(**kargs):
#     print(type(kargs))
#     print(kargs)

# stude(a=1,b=2,c=3,d=4,e=5)

# def f(*args,**kwargs):
#     print("Positional Args:",args)
#     print("Keyword Args:",kwargs)

# f(1,2,3,a=1,b=2,c=3)
# f()

# def stud(**kwargs):
#     print("type:",type(kwargs))
#     for a,v in kwargs.items():
#         print(a,v)
#     print(kwargs)

# stud(name="vijay",age=21,city="gujarat",college="Gujarat vidyapith")

print("===== function ========")


print("1.lambda function")

add = lambda a, b: a + b
sub = lambda a, b: a - b
mul = lambda a, b: a * b

print("Addition:", add(11, 3))
print("Subtraction:", sub(11, 3))
print("Multiplication:", mul(11, 3))

print("2.map function")

add = lambda a, b: a + b

list1 = [1,2,3,4,5]
list2 = [6,7,8,9,10]

print(list(map(add,list1,list2)))

# print ("3.reduce function")

# from functools import reduce

# add = lambda a, b: a + b

# list1 = [1,2,3,4,5]

# print(reduce(add,list1))

# print("4.filter function")

# add = lambda a, b: a + b

# list1 = [1,2,3,4,5]

# print(list(filter(add,list1)))