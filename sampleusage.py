###
# sampleusage.py: sample program demonstrating use of parallelize module
#
###

import parallelize as pz
import time

def multiply_numbers(*args):
    answer = 1
    for argument in args:
        answer = answer * argument
    return answer;

def sleepy_echo(lengthoftime,instring,punct=""):
    response = instring + punct
    time.sleep(lengthoftime)
    return response;

def print_answerdict(indict,argslist,kwargslist=[]):
    if len(kwargslist)>0:
        kwevaluate = True
    else:
        kwevaluate = False
    for job in indict.keys():
        if not kwevaluate:
            print("#",job," : ",argslist[job]," --> ",indict[job])
        else:
            print("#",job," : ",argslist[job]," :: ",kwargslist[job],
                  " --> ",indict[job])

### MAIN BODY ###

if __name__ == "__main__":

    argslist = [(1,3), (2,4,6), (3,5,7,9), (4,6,8), (5,7), (3,11,3,2),
                (4,3,1),(33,13)]

    starttime = time.perf_counter()
    answersdict = pz.parallel_vector_execute(multiply_numbers,argslist)
    endtime = time.perf_counter()
    print_answerdict(answersdict,argslist)
    print("Parallel execution time: %0.6f seconds."%(endtime-starttime))
    print()
    
    starttime = time.perf_counter()
    answersdict = pz.serial_vector_execute(multiply_numbers,argslist)
    endtime = time.perf_counter()
    print_answerdict(answersdict,argslist)
    print("Serial execution time: %0.6f seconds."%(endtime-starttime))
    print()
    print()

    argslist = [(1,"First"), (2,"Second"), (8,"Third"), (4,"Fourth"),
                (10,"Fifth"), (2,"Sixth"), (6,"Seventh"),(1,"Eighth")]
    kwargslist = [{"punct":"!"},{},{"punct":"?"},{},{},
                  {"punct":"."},{},{"punct":"!"}]

    starttime = time.perf_counter()
    answersdict = pz.parallel_vector_execute(sleepy_echo,argslist,kwargslist=kwargslist)
    endtime = time.perf_counter()
    print_answerdict(answersdict,argslist,kwargslist=kwargslist)
    print("Parallel execution time: %0.6f seconds."%(endtime-starttime))
    print()
    
    starttime = time.perf_counter()
    answersdict = pz.serial_vector_execute(sleepy_echo,argslist,kwargslist=kwargslist)
    endtime = time.perf_counter()
    print_answerdict(answersdict,argslist,kwargslist=kwargslist)
    print("Serial execution time: %0.6f seconds."%(endtime-starttime))
    
