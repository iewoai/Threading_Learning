import threading
import time

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print ("开启线程： " + self.name)
        # 获取锁，用于线程同步
        threadLock.acquire()
        print_time(self.name, self.counter, 3)
        # 释放锁，开启下一个线程
        threadLock.release()

def print_time(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1
'''
# Lock()指令锁-全局锁
# RLock()可重入锁-线程锁
import threading
lock = threading.Lock() #Lock对象
lock.acquire()
lock.acquire()  #产生了死锁。
lock.release()
lock.release()
print lock.acquire()

import threading
rLock = threading.RLock()  #RLock对象
rLock.acquire()
rLock.acquire() #在同一线程内，程序不会堵塞。
rLock.release()
rLock.release()
'''
# threadLock = threading.Lock()
# threads = []

# # 创建新线程
# thread1 = myThread(1, "Thread-1", 1)
# thread2 = myThread(2, "Thread-2", 2)

# # 开启新线程
# thread1.start()
# thread2.start()

# # 添加线程到线程列表
# threads.append(thread1)
# threads.append(thread2)

# # 等待所有线程完成
# for t in threads:
#     t.join()
# print ("退出主线程")
'''
运行结果：
开启线程： Thread-1
开启线程： Thread-2
Thread-1: Wed May 15 10:46:46 2019
Thread-1: Wed May 15 10:46:47 2019
Thread-1: Wed May 15 10:46:48 2019
Thread-2: Wed May 15 10:46:50 2019
Thread-2: Wed May 15 10:46:52 2019
Thread-2: Wed May 15 10:46:54 2019
退出主线程
'''
import threading
import time

gl_num = 0
lock = threading.RLock()

# 调用acquire([timeout])时，线程将一直阻塞，
# 直到获得锁定或者直到timeout秒后（timeout参数可选）。
# 返回是否获得锁。
def Func():
    lock.acquire()
    global gl_num
    gl_num += 1
    time.sleep(1)
    print(gl_num)
    lock.release()

for i in range(10):
    t = threading.Thread(target=Func)
    t.start()