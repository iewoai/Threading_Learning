 # 消费生产模型(一)
import threading
import time
'''
acquire([timeout])/release(): 调用关联的锁的相应方法。 
wait([timeout]): 调用这个方法将使线程进入Condition的等待池等待通知，并释放锁。使用前线程必须已获得锁定，否则将抛出异常。 
notify(): 调用这个方法将从等待池挑选一个线程并通知，收到通知的线程将自动调用acquire()尝试获得锁定（进入锁定池）；其他线程仍然在等待池中。调用这个方法不会释放锁定。使用前线程必须已获得锁定，否则将抛出异常。 
notifyAll(): 调用这个方法将通知等待池中所有的线程，这些线程都将进入锁定池尝试获得锁定。调用这个方法不会释放锁定。使用前线程必须已获得锁定，否则将抛出异常。
'''

'''
# 商品
product = None
# 条件变量
con = threading.Condition()

# 生产者方法
def produce():
    global product

    if con.acquire():
        while True:
            if product is None:
                print('produce...')
                product = 'anything'

                # 通知消费者，商品已经生产
                con.notify()

            # 等待通知
            con.wait()
            time.sleep(2)

# 消费者方法
def consume():
    global product

    if con.acquire():
        while True:
            if product is not None:
                print('consume...')
                product = None

                # 通知生产者，商品已经没了
                con.notify()

            # 等待通知
            con.wait()
            time.sleep(2)

t1 = threading.Thread(target=produce)
t2 = threading.Thread(target=consume)
t2.start()
t1.start()
'''

# 消费生产模型(二)
'''
import threading
import time

condition = threading.Condition()
products = 0

class Producer(threading.Thread):
    def run(self):
        global products
        while True:
            if condition.acquire():
                if products < 10:
                    products += 1
                    print("Producer(%s):deliver one, now products:%d" %(self.name, products))
                    condition.notify()#不释放锁定，因此需要下面一句
                    condition.release()
                else:
                    print("Producer(%s):already 10, stop deliver, now products:%d" %(self.name, products))
                    condition.wait()#自动释放锁定
                time.sleep(2)

class Consumer(threading.Thread):
    def run(self):
        global products
        while True:
            if condition.acquire():
                if products > 1:
                    products -= 1
                    print("Consumer(%s):consume one, now products:%d" %(self.name, products))
                    condition.notify()
                    condition.release()
                else:
                    print("Consumer(%s):only 1, stop consume, products:%d" %(self.name, products))
                    condition.wait()
                time.sleep(2)

if __name__ == "__main__":
    for p in range(0, 2):
        p = Producer()
        p.start()

    for c in range(0, 3):
        c = Consumer()
        c.start()
'''

# 消费生产模型(三)
import threading

alist = None
condition = threading.Condition()

def doSet():
    if condition.acquire():
        while alist is None:
            condition.wait()
        for i in range(len(alist))[::-1]:
            alist[i] = 1
        condition.release()

def doPrint():
    if condition.acquire():
        while alist is None:
            condition.wait()
        for i in alist:
            print(i)
        condition.release()

def doCreate():
    global alist
    if condition.acquire():
        if alist is None:
            alist = [0 for i in range(10)]
            condition.notifyAll()
        condition.release()

tset = threading.Thread(target=doSet,name='tset')
tprint = threading.Thread(target=doPrint,name='tprint')
tcreate = threading.Thread(target=doCreate,name='tcreate')
tset.start()
tprint.start()
tcreate.start()