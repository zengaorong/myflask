#coding=utf-8
from datetime import datetime

def log(func):
    def decorator(*args, **kw):
        print "log is print"
        print args
        print kw
        kw['c']()
        return func(*args, **kw)
    return decorator

@log
def now(*args, **kw):
    time = datetime.now()
    print time.strftime('%Y-%m-%d')

# 等价于 now = log(now)
def test():
    print "me me me"

now('a','b',test,a=1,b=2,c=test)



