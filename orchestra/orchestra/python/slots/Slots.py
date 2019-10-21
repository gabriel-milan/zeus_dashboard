
__all__ = ["GPUNode","CPUNode", "Slots"]


from Gaugi import Logger, NotSet
from Gaugi.messenger.macros import *
from Gaugi import retrieve_kw
from Gaugi import StatusCode
from collections import deque
from orchestra import Status
from orchestra.Consumer import Consumer



class GPUNode( object ):
  def __init__(self, name, device ):
    self.__name = name
    self.__device = device
    self.__available = True

  def name(self):
    return self.__name

  def device(self):
    return self.__device

  def isAvailable( self ):
    return self.__available

  def lock( self ):
    self.__available = False

  def unlock( self ):
    self.__available = True



class CPUNode( object ):
  def __init__(self, name):
    self.__name = name
    self.__available = True

  def name(self):
    return self.__name

  def isAvailable( self ):
    return self.__available

  def lock( self ):
    self.__available = False

  def unlock( self ):
    self.__available = True

  def device(self):
    return None







class Slots( Logger ):

  def __init__(self,name, nodes ) :
    Logger.__init__(self,name=name)
    self.__total = len(nodes)
    self.__slots = list()
    self.__available_nodes = nodes


  def setDatabase( self, db ):
    self.__db = db


  def setOrchestrator( self, orc ):
    self.__orchestrator = orc


  def db(self):
    return self.__db


  def orchestrator(self):
    return self.__orchestrator


  def initialize(self):

    if self.db() is NotSet:
      MSG_FATAL( self, "Database object not passed to slot." )

    if self.orchestrator() is NotSet:
      MSG_FATAL( self, "Orchestrator object not passed to slot.")

    MSG_INFO( self, "Creating cluster stack with %s slots", self.size() )
    return StatusCode.SUCCESS



  def execute(self):
    self.update()
    return StatusCode.SUCCESS


  def finalize(self):
    return StatusCode.SUCCESS


  def size(self):
    return self.__total



  def isAvailable(self):
    return True if len(self.__slots) < self.size() else False


  #def increment( self ):
  #  self.__total+=1


  #def decrement( self ):
  #  self.__total-=1


  #def setSize( self, total ):
  #  self.__total=total


  def unlockAll(self):
    for node in self.__available_nodes:
      node.unlock()


  def getAvailableNode(self):
    for node in self.__available_nodes:
      if node.isAvailable():
        return node
    return None


  def update(self):
    for idx, consumer in enumerate(self.__slots):

      # consumer.status is not DB like, this is internal of kubernetes
      # In DB, the job was activated but here, we put as pending to wait the
      # kubernetes. If everything its ok, the internal status will be change
      # to (running,failed or done).
      if consumer.status() is Status.PENDING:
        # TODO: Change the internal state to RUNNING
        # If, we have an error during the message,
        # we will change to BROKEN status
        if consumer.execute().isFailure():
          # Tell to DB that this job is in broken status
          consumer.job().setStatus( Status.BROKEN )
          consumer.finalize()
          consumer.node().unlock()
          self.__slots.remove(consumer)
        else: # change to running status
          # Tell to DB that this job is running
          consumer.job().setStatus( Status.RUNNING )

      elif consumer.status() is Status.FAILED:
        # Tell to db that this job was failed
        consumer.job().setStatus( Status.FAILED )
        consumer.finalize()
        # Remove this job into the stack
        consumer.node().unlock()
        self.__slots.remove(consumer)
      # Kubernetes job is running. Go to the next slot...
      elif consumer.status() is Status.RUNNING:
        continue

      elif consumer.status() is Status.DONE:
        consumer.job().setStatus( Status.DONE )
        consumer.finalize()
        consumer.node().unlock()
        self.__slots.remove(consumer)

    self.db().commit()


  #
  # Add an job into the stack
  # Job is an db object
  #
  def push_back( self, job ):
    if self.isAvailable():
      node = self.getAvailableNode()
      # Create the job object
      obj = Consumer( job, node )
      # Tell to database that this job will be activated
      obj.setOrchestrator( self.orchestrator() )
      # TODO: the job must set the internal status to ACTIVATED mode
      obj.initialize()
      obj.job().setStatus( Status.ACTIVATED )
      self.__slots.append( obj )
      node.lock()
    else:
      MSG_WARNING( self, "You asked to add one job into the stack but there is no available slots yet." )









