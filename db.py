from pymongo import Connection
import json,time


################################################################################
#
#        setting up the database
#
################################################################################

c = Connection()
db = c.summerapplication
users = db.users

    


################################################################################
#
#        User routines
#
################################################################################


def checkCredentials(email,password):
    res=users.find({"email":email,"password":password})
    return len([x for x in res])==1

def addUser(email,password):
    res = users.find({'email':email})
    if len([x for x in res])>0:
        return None
   
    result = users.insert({'email':email,'password':password}) 
    return {'email':email,'password':password}


################################################################################
#
#        main (for testing)
#
################################################################################

if __name__=='__main__':
   pass
