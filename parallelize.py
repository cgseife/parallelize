############
#
# Parallelize: a module for simple parallel execution of an arbitrary function
#
# v 1.0, 10/30/2020
#
# Charles Seife, cs129@nyu.edu
#
############
#
# Usage:
#   To run multiple instances of a function, func, which takes arguments *args
# [tuple] and (optional) keyword arguments **kwargs [dictionary] in parallel --
#       a) create a list of argument tuples that will be fed to the function
#       b) create an optional list of kwargument dicts that will be fed to the function
#       c) start main body of program with:
#           if __name__ == "__main__":
#       d) execute via the function parallel_vector_execute
#
#   The MAXPROCESSES global determines the maximum number of processes in
#   the pool; default is four.
#
#   The serial_vector_execute function will operate the same way that
#   parallel_vector_execute does, without parallelization (for debugging.)
#
#   Example code should be included in this archive.
#
############


import multiprocessing as mp
import functools

MAXPROCESSES = 4


###
# procedure record_answer
#
# IN:   a result to record
#       a job number associated with this result
#       a dictionary of results (with keys = jobnumbers and values = results)
#       (optional) the number of jobs being processed by the parent function
#
# OUT:  None
#
# DOES: records the result to the dictionary under the appropriate job number.
#       if verbosenum > 0, prints to screen the job number being recorded
#
#       This function serves as the callback function
#
###
def record_answer(result,jobnumber,resultlog,verbosenum=0):
    resultlog[jobnumber] = result
    if verbosenum > 0:
        print("Recording job #",jobnumber," of ",verbosenum,".",sep="")
    return;


###
# procedure parallel_vector_execute
#
# IN:   an arbitrary function
#       a list of arguments (each argument is a tuple)
#       kwargslist = a list of keyword arguments. If used, must be same length
#           as the list of arguments.
#       verbose = a flag to determine if the execution is verbose
#       maxprocesses = the maximum number of processes running in parallel
#
# OUT:  a dictionary of results (keys = job numbers; values = results)
#
# DOES: Executes the function a maximum of maxprocesses times in parallel, going
#       down the list of arguments (and optionally kwargs) and feeding them to
#       the function
#
###
def parallel_vector_execute(function,argslist,kwargslist=[],verbose=True,maxprocesses=MAXPROCESSES):
    answerdict = {}
    numjobs = len(argslist)
    if len(kwargslist)>0:
        kwevaluate = True
    else:
        kwevaluate = False
    if verbose:
        verbnum = numjobs
    else:
        verbnum = 0        
    pool = mp.Pool(processes = maxprocesses)
    for job in range(0,numjobs):
        callback_record_answer = functools.partial(record_answer,jobnumber=job,
                                                   resultlog=answerdict,verbosenum=verbnum)
        if not kwevaluate:
            pool.apply_async(function,argslist[job],callback=callback_record_answer)
        else:
            pool.apply_async(function,argslist[job],kwds=kwargslist[job],callback=callback_record_answer)
    pool.close()
    pool.join()
    return answerdict;


###
# procedure serial_vector_execute
#
# DOES: Executes the function in the same way as parallel_vector_execute, but
#       without parallelization. Useful for debugging/timing.
#
###
def serial_vector_execute(function,argslist,kwargslist=[]):
    answerdict = {}
    numjobs = len(argslist)
    if len(kwargslist)>0:
        kwevaluate = True
    else:
        kwevaluate = False
    for job in range (0,numjobs):
        argset = argslist[job]
        numargs = len(argset)
        if not kwevaluate:
            answerdict[job]=function(*argset)
        else:
            kwargset = kwargslist[job]
            answerdict[job]=function(*argset,**kwargset)
    return answerdict;


### END MODULE ###
