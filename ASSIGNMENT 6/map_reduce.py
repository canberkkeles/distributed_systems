from abc import ABCMeta,abstractmethod
import zmq
from multiprocessing import Process,Value
from math import ceil
import time

class MapReduce(metaclass = ABCMeta):

    def __init__(self,numWorker):
        self.numWorker = numWorker
        self.result = Value('i',0)


    @abstractmethod
    def Map(self,map_input):
        return
    
    @abstractmethod
    def Reduce(self,reduce_input):
        return
    
    def __Producer(self,producer_input):
        context = zmq.Context()
        socket = context.socket(zmq.PUSH)
        socket.bind("tcp://127.0.0.1:5557")



        fName = producer_input['file_name']
        kw = producer_input['keyword']

        lineCount = 0

        # CODE PRODUCER

        with open(fName) as f:
            for line in f:
                lineCount += 1
        
        linePerEntry = ceil(lineCount / self.numWorker)
        start = 0
        end = 0

        while end < lineCount and start < lineCount: # ASSIGNING LINES TO CONSUMERS
            end = start + linePerEntry - 1
            if end >= lineCount:
                end = lineCount - 1

            work_message = {'filename' : fName, 'startno' : start,'endno' : end,'keyword' : kw}
            socket.send_json(work_message)
            time.sleep(0.1) # TO AVOID MESSAGES BEING LOST
            start = start + linePerEntry


    
    def __Consumer(self):
        context = zmq.Context()

        results_receiver = context.socket(zmq.PULL)
        results_receiver.connect("tcp://127.0.0.1:5557")

        results_sender = context.socket(zmq.PUSH)
        results_sender.connect("tcp://127.0.0.1:5558")
        # EVERY CONSUMER RUNS ONCE
        message = results_receiver.recv_json()
        mapped = self.Map(message)
        results_sender.send_json(mapped)
   
   
    def __ResultCollector(self):
        finishCount = 0
        context = zmq.Context()
        collector = context.socket(zmq.PULL)
        collector.bind("tcp://127.0.0.1:5558")

 

        while finishCount < self.numWorker: # UNTIL ALL THE WORKERS ARE FINISHED
            message = collector.recv_json()
            self.result.value += self.Reduce(message)
            finishCount+=1
        


    def start(self,fileName,keyword = None):
        print("Program in progress... please wait...")
        rc = Process(target = self.__ResultCollector)
        rc.start()
        
        consumers = list()
        for i in range(self.numWorker):
            consumer = Process(target =self.__Consumer)
            consumer.start()
            consumers.append(consumer)

        p = Process(target = self.__Producer,args= ({'file_name' : fileName,'keyword' : keyword},)) #NOT SURE
        p.start()

        p.join()
        for c in consumers:
            c.join()
        rc.join()
        print("The result is ",self.result.value)
        


        







