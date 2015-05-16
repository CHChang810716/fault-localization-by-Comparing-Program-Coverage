#!/usr/bin/python
import sys as sys
from copy import deepcopy
pass_stmt = {}
fail_stmt = {}
now_stmt = {}
target_prefix = "/" 
caculate = False
def tracer(frame, event, arg):
    global now_stmt
    global target_prefix
    global caculate
    code = frame.f_code
    function = code.co_name
    filename = code.co_filename
    line = frame.f_lineno
    #print filename + ":" + `line` + ":" + function + "():", event, arg
    try:
        if filename.find(target_prefix) == -1:
            return tracer
    except TypeError:
        return tracer
    if caculate == True:
        try:
            if line in now_stmt:
                now_stmt[(filename, function, line)] += 1
            else:
                now_stmt[(filename, function, line)] = int(1)
        except TypeError:
            pass    
    return tracer
def merge(map1, map2):
    for key, value in map2.iteritems():
        if key in map1:
            map1[key] += value
        else:
            map1[key] = value

def show_cov( container, file_path, func, start, end ):
    for i in range(start,end):
        if (file_path, func, i) in container:
            print container[(file_path, func, i)]
        else:
            print 0
def show_con( container ):
    for key, value in container.iteritems():
        print "%s\t%d" % (key, value)
def start_trace():
    global caculate
    global now_stmt
    caculate = True

def end_trace():
    global now_stmt
    global caculate
    caculate = False
def set_target_prefix(s):
    global target_prefix
    target_prefix = s
def set_last_trace_result(s):
    global now_stmt
    global pass_stmt
    global fail_stmt
    if s == 'pass':
        merge(pass_stmt, now_stmt)
    elif s == 'fail':
        merge(fail_stmt, now_stmt)
    now_stmt.clear()

