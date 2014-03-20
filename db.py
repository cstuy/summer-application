from pymongo import Connection
import json,time

qfile = "questions.json"

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

def getCredentials(email):
    res=users.find({"email":email})
    if res.count() == 1:
        return res[0]
    else:
        return None

def addUser(email,password):
    res = users.find({'email':email})
    if len([x for x in res])>0:
        return None
   
    result = users.insert({'email':email,'password':password}) 
    return {'email':email,'password':password}


################################################################################
#
#        questions
#
################################################################################
def updateanswers(email,questions):
    questions['email']=email
    result = db.answers.update({'email':email},questions,upsert=True)
    print result

def getanswers(email):
    result = list(db.answers.find({'email':email}))
    qs = json.load(qfile)
    if len(result)==1:
        r = result[0]
        keys = [ x['name'] for x in r['questions']]
        for q in qs['questions']:
            print q
            if q['name'] not in keys:
                r['questions'].append(q)
        return r
    return qs


################################################################################
#
#        main (for testing)
#
################################################################################

if __name__=='__main__':
   pass
