
from ringerdb import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
db = RingerDB('jodafons','postgres://ringer:6sJ09066sV1990;6@postgres-ringer-db.cahhufxxnnnr.us-east-2.rds.amazonaws.com/ringer')

print (db.isConnected())


#session.drop_all()  
#user = User( name='jodafons' )
#user2 = Username( username='mverissi' )
#session.add(user)
#session.add(user2)
session.close()







