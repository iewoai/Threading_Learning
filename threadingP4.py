
import threading
import time

event = threading.Event()
'''
isSet(): 当内置标志为True时返回True。 
set(): 将标志设为True，并通知所有处于等待阻塞状态的线程恢复运行状态。 
clear(): 将标志设为False。 
wait([timeout]): 如果标志为True将立即返回，否则阻塞线程至等待阻塞状态，等待其他线程调用set()。
'''
def func():
    # 等待事件，进入等待阻塞状态
    print('%s wait for event...' % threading.currentThread().getName())
    event.wait()

    # 收到事件后进入运行状态
    print('%s recv event.' % threading.currentThread().getName())

t1 = threading.Thread(target=func)
t2 = threading.Thread(target=func)
t1.start()
t2.start()

time.sleep(2)

# 发送事件通知
print('MainThread set event.')
event.set()

'''
运行结果：
Thread-1 wait for event...
Thread-2 wait for event...
 
#2秒后。。。
MainThread set event.
Thread-1 recv event.
 Thread-2 recv event.
'''


import threading
'''
Timer(interval, function, args=[], kwargs={}) 
interval: 指定的时间 
function: 要执行的方法 
args/kwargs: 方法的参数
'''
def func():
    print('hello timer!')

timer = threading.Timer(5, func)
timer.start()


'''
local是一个小写字母开头的类，用于管理 thread-local（线程局部的）数据。对于同一个local，线程无法访问其他线程设置的属性；线程设置的属性不会被其他线程设置的同名属性替换。

可以把local看成是一个“线程-属性字典”的字典，local封装了从自身使用线程作为 key检索对应的属性字典、再使用属性名作为key检索属性值的细节。
'''
local = threading.local()
local.tname = 'main'

def func():
    local.tname = 'notmain'
    print(local.tname)

t1 = threading.Thread(target=func)
t1.start()
t1.join()

print(local.tname)

'''
运行结果：
notmain
main
'''

