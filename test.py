import _thread
from time import sleep
items = [2, 4, 5, 2, 1, 7]
l = []

def sleep_sort(i):
    sleep(i*0.001)
    print(i)
    l.append(i)

for i in items:
    _thread.start_new_thread(sleep_sort, (i,)) 
