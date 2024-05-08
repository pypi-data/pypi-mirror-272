import rpy2.robjects as ro

def modifyinput(func):
    def wrapper(*args, **kwargs):
        outargs = []
        for arg in args:
            if isinstance(arg, int):
                arg = arg+1
                outargs.append(arg)
        result = func(*outargs, **kwargs)
        print("After calling the function")
        return result
    return wrapper

@modifyinput
def pt(a):
    print('number is {}'.format(a))
    return a


ro.r('''
    f <- function(a){
        print(a)
        return(a)
    }''')
sum([1,2,3])