import queue
import threading
import time

exitFlag = 0
'''
Queue.qsize() 返回队列的大小
Queue.empty() 如果队列为空，返回True,反之False
Queue.full() 如果队列满了，返回True,反之False
Queue.full 与 maxsize 大小对应
Queue.get([block[, timeout]])获取队列，timeout等待时间
Queue.get_nowait() 相当Queue.get(False)
Queue.put(item) 写入队列，timeout等待时间
Queue.put_nowait(item) 相当Queue.put(item, False)
Queue.task_done() 在完成一项工作之后，Queue.task_done()函数向任务已经完成的队列发送一个信号
Queue.join() 实际上意味着等到队列为空，再执行别的操作
'''
'''
class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        print ("开启线程：" + self.name)
        process_data(self.name, self.q)
        print ("退出线程：" + self.name)

def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print ("%s processing %s" % (threadName, data))
        else:
            queueLock.release()
        time.sleep(1)

threadList = ["Thread-1", "Thread-2", "Thread-3"]
nameList = ["One", "Two", "Three", "Four", "Five"]
queueLock = threading.Lock()
workQueue = queue.Queue(10)
threads = []
threadID = 1

# 创建新线程
for tName in threadList:
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

# 填充队列
queueLock.acquire()
for word in nameList:
    workQueue.put(word)
queueLock.release()

# 等待队列清空
while not workQueue.empty():
    pass

# 通知线程是时候退出
exitFlag = 1

# 等待所有线程完成
for t in threads:
    t.join()
print ("退出主线程")

运行结果：
开启线程：Thread-1
开启线程：Thread-2
开启线程：Thread-3
Thread-3 processing One
Thread-1 processing Two
Thread-2 processing Three
Thread-3 processing Four
Thread-1 processing Five
退出线程：Thread-3
退出线程：Thread-2
退出线程：Thread-1
退出主线程
'''
'''
class myThread (threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
    def run(self):
        print ("开启线程：" + self.name)
        process_data(self.name)
        print ("退出线程：" + self.name)

def process_data(threadName):
    while not q.empty():
        item = q.get()
        i = item%10
        print("%s processing 运行时间：%d" % (threadName, i))

def main():
    threads = []
    for task in range(1, 100):
        q.put(task)
    for tName in threadList:
        thread = myThread(tName)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    start = time.time()
    q = queue.Queue()
    threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4", "Thread-5", "Thread-6"]
    main()
    print('总耗时：%.5f秒' % float(time.time()-start))
'''

#开启多个线程，同时执行任务，有几个线程就执行几个任务
 
import threading
import time
import queue

a = []
class MyThread(threading.Thread):
    def __init__(self, func, i):
        threading.Thread.__init__(self)
        self.i = i
        self.func = func
    def run(self):
        print ("开启线程：%d" % self.i)
        self.func()
 
def worker():
    global a
    while not q.empty():
        item = q.get()
        if item % 3 == 0:
            a.append(item)
        print('Processing : ',item)
        time.sleep(1)
 
def main():
    threads = []
    for task in range(100):
        q.put(task)
    for i in range(threadNum):   #开启三个线程
        thread = MyThread(worker, i)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
 
if __name__ == '__main__':
    q = queue.Queue()
    threadNum = 3
    main()
    print(a)