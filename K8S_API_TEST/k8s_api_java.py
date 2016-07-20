from net.grinder.script import Test
from net.grinder.script.Grinder import grinder
from com.netease.qa.nce.test import SyncAPIClient
from com.netease.qa.nce.test import BasicAPIClient
from java.util import Random
import time

rand = Random()
prefix = rand.nextInt(1000000)

namelistFile=open("namelist", "w")
class TestRunner:
    
    def __init__(self):
        #sleepTime = grinder.threadNumber * 200  # per thread
        #grinder.sleep(sleepTime, 0)   
        self.namelist=[]
        self.basicCli = BasicAPIClient()
        self.syncCli = SyncAPIClient()
        #self.namespace = "perf" + str(grinder.threadNumber + 1)
        
        
    def createRC(self, rcName, namespace):
        success = self.syncCli.createRCWaitRunning(rcName, namespace)
        if(not success):
            grinder.getStatistics().getForCurrentTest().setSuccess(False)
            
    def expandRC(self, rcName, namespace, replicas):
        success = self.syncCli.updateRC(rcName, namespace, replicas)
        if(not success):
            grinder.getStatistics().getForCurrentTest().setSuccess(False)

    def reduceRC(self, rcName, namespace, replicas):
        success = self.syncCli.updateRC(rcName, namespace, replicas)
        if(not success):
            grinder.getStatistics().getForCurrentTest().setSuccess(False)
            
    def deleteResource(self, resourceType, resourceName, namespace):
        success = self.basicCli.deleteResource(resourceType, resourceName, namespace)
        if(not success):
            grinder.getStatistics().getForCurrentTest().setSuccess(False)
                        
#    def __del__(self):
#        self.basicCli.deleteNewAddedRC(self.namelist, "perf1")
#        namelistFile.close()
#        print "update and delete all rc"
#        self.basicCli.cleanAllRC("default")
        

    testWrapper1 = Test(1, "create RC, until success").wrap(createRC)
    testWrapper2 = Test(2, "update RC, replicas 1->5, until success").wrap(expandRC)
    testWrapper3 = Test(3, "update RC, replicas 5->0, until success").wrap(reduceRC)
    testWrapper4 = Test(4, "delete RC").wrap(deleteResource)


    def __call__(self): 
      
        resourcename = "perftest-%s-%s-%s-%s" %(prefix, grinder.threadNumber, int(time.time()), rand.nextInt(100000))
        self.namelist.append(resourcename)
        resourceType = 'replicationcontrollers'
        ns=rand.nextInt(4000)
        self.namespace = "default"
        #self.namespace = "perf1"
        
            
        #create     
        self.testWrapper1(resourcename, self.namespace)
          
        #reduce RC 
        self.testWrapper3(resourcename, self.namespace, "0")
          
        #delete    
        self.testWrapper4(resourceType, resourcename, self.namespace)
        
        
        
        
        
