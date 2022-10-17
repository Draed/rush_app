import threading
import time
  
# c = threading.Condition()
# c.acquire()

# def countdown ():
#     c.acquire()
#     print('start countdown')
#     duration_in_sec = 8
#     while duration_in_sec:
#         print(duration_in_sec, "\r")
#         time.sleep(1)
#         duration_in_sec -= 1
        
#     else:
#         c.notify()
#         c.release()
#     print('The timer has finish') 
    
# def question():
#     c.acquire()
#     time.sleep(2)
#     print("ending rush right now")
#     c.notify()
#     c.release
  
# t1 = threading.Thread(target = countdown)
# t2 = threading.Thread(target = question)
# t1.start()
# t2.start()
# # wait for the countdown to end or question
# c.wait()

# print("wait for the countdown to stop ... ")

# c.release()

def countdown(stop_event):
    print('start countdown')
    duration_in_sec = 8
    while duration_in_sec and (not stop_event.is_set()):
        print(duration_in_sec, "\r")
        time.sleep(1)
        duration_in_sec -= 1

def endQuestion(stop_event):
    print("This Thread will kill countdown is 2 second")
    time.sleep(2)
    print("ending rush right now")
    stop_event.set()

print("Stop event is set as False by default")
stop_event = threading.Event()
print(stop_event.is_set())

print("\n")

t1 = threading.Thread(target = countdown, args = (stop_event,))
t2 = threading.Thread(target = endQuestion, args = (stop_event,))

print("Starting countdown")
t1.start()
print("Starting EndQuestion")
t2.start()


print("waiting for EndQuestion to end")
t2.join()

print("Programm ended")


