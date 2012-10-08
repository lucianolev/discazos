import random
import datetime
from hashlib import sha1

def random_code(): 
    salt = sha1(str(random.random())).hexdigest()[:5]
    code = sha1("%s%s" % (datetime.datetime.now(), salt)).hexdigest()
    return code #SHA-1 length is 40 chars