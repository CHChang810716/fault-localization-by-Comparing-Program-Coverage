#!/usr/bin/python
# --- INITIALIZATION
import sys,outputters,getopt,getcov,os
xmlproc_path = os.path.abspath('./')
sys.path.append(xmlproc_path + '/xml/parsers/xmlproc')      
import xmlproc
from math import sqrt
import operator
getcov.set_target_prefix(xmlproc_path)
def mainF(args):
#    print args
    """
    A command-line interface to the xmlproc parser. It continues parsing
    even after fatal errors, in order to be find more errors, since this
    does not mean feeding data to the application after a fatal error
    (which would be in violation of the spec).
    """

    usage=\
    """        
    Usage:
    
      xpcmd.py [options] [urltodoc]
    
      ---Options:  
      -l language: ISO 3166 language code for language to use in error messages
      -o format:   Format to output parsed XML. 'e': ESIS, 'x': canonical XML
                   and 'n': normalized XML. No data will be output if this
                   option is not specified.
      urltodoc:    URL to the document to parse. (You can use plain file names
                   as well.) Can be omitted if a catalog is specified and contains
                   a DOCUMENT entry.
      -n:          Report qualified names as 'URI name'. (Namespace processing.)
      --nowarn:    Don't write warnings to console.
      --entstck:   Show entity stack on errors.
      --extsub:    Read the external subset of documents.
    """
    
    
    # --- Interpreting options
    
    try:
        (options,sysids)=getopt.getopt(args,"l:o:n",
                                       ["nowarn","entstck","rawxml","extsub"])
    except getopt.error,e:
        print "Usage error: "+e
        print usage
        sys.exit(1)
        
    pf=None
    namespaces=0
    app=xmlproc.Application()
    warnings=1
    entstack=0
    rawxml=0
    extsub=0
    
    p=xmlproc.XMLProcessor()
    
    for option in options:
        if option[0]=="-l":
            try:
                p.set_error_language(option[1])
            except KeyError:
                print "Error language '%s' not available" % option[1]
        elif option[0]=="-o":
            if option[1]=="e" or option[1]=="E":
                app=outputters.ESISDocHandler()            
            elif option[1]=="x" or option[1]=="X":
                app=outputters.Canonizer()
            elif option[1]=="n" or option[1]=="N":
                app=outputters.DocGenerator()
            else:
                print "Error: Unknown output format "+option[1]
                print usage
        elif option[0]=="-n":
            namespaces=1
        elif option[0]=="--nowarn":
            warnings=0
        elif option[0]=="--entstck":
            entstack=1
        elif option[0]=="--rawxml":
            rawxml=1
        elif option[0]=="--extsub":
            extsub=1
    
    # Acting on option settings
    
    err=outputters.MyErrorHandler(p, p, warnings, entstack, rawxml)
    p.set_error_handler(err)
    
    if namespaces:
        from xml.parsers.xmlproc import namespace
    
        nsf=namespace.NamespaceFilter(p)
        nsf.set_application(app)
        p.set_application(nsf)
    else:
        p.set_application(app)
    
    if len(sysids)==0:
        print "You must specify a file to parse"
        print usage
        sys.exit(1)
    
    if extsub:
        p.set_read_external_subset(extsub)
        
    # --- Starting parse    
    
    print "xmlproc version %s" % xmlproc.version
    
    for sysid in sysids:
        print
        print "Parsing '%s'" % sysid
        p.set_data_after_wf_error(0)
        p.parse_resource(sysid)
        print "Parse complete, %d error(s)" % err.errors,
    
        if warnings:
            print "and %d warning(s)" % err.warnings
        else:
            print
        
        err.reset()
        p.reset()

cf_cs_uf = {}

sys.settrace(getcov.tracer)

pass_list = ['com.adobe.versioncue.plist', 'com.apple.AppleFileServer.plist', 'com.apple.BezelServices.plist', 'com.apple.ByteRangeLocking.plist', 'com.apple.dockfixup.plist', 'com.apple.HIToolbox.plist', 'com.apple.iWork.Installer.plist', 'com.apple.keyboardtype.plist', 'com.apple.Keynote.plist', 'com.apple.networkConfig.plist', 'com.apple.print.defaultpapersize.plist', 'com.apple.print.FaxPrefs.plist', 'com.apple.RemoteManagement.plist', 'com.apple.SetupAssistant.plist', 'com.apple.SoftwareUpdate.plist', 'com.apple.windowserver.plist', 'com.apple.xgrid.agent.plist', 'com.apple.xgrid.controller.plist', 'com.skype.skype.plist']
fail_list = ['com.apple.Asteroid.plist', 'com.apple.Cell.plist', 'com.apple.Tiger.plist']
def m1_Tarantula(s):
    global pass_list
    global fail_list
    Nf = float(len(fail_list))
    Ns = float(len(pass_list))
    if s in cf_cs_uf:
        (tNcf_s, tNcs_s, tNuf_s) = cf_cs_uf[s]
        Ncf_s = float(tNcf_s)
        Ncs_s = float(tNcs_s)
        Nuf_s = float(tNuf_s)

    return float(float((Ncf_s/Nf))/float((Ncf_s/Nf)+float(Ncs_s/Ns)))
def m2_Ochiai(s):
    global pass_list
    global fail_list
    Nf = float(len(fail_list))
    Ns = float(len(pass_list))
    if s in cf_cs_uf:
        (tNcf_s, tNcs_s, tNuf_s) = cf_cs_uf[s]
        Ncf_s = float(tNcf_s)
        Ncs_s = float(tNcs_s)
        Nuf_s = float(tNuf_s)
    (filename, function, line) = s
    #print "%s\t%d\t%lf\t%lf\t%lf" % (filename, line, Ncf_s, Ncs_s, Nuf_s)
    return float(Ncf_s / sqrt(float(Nf*float(Ncf_s+Ncs_s))))
def m3_Ochiai(s):
    global pass_list
    global fail_list
    Nf = float(len(fail_list))
    Ns = float(len(pass_list))
    if s in cf_cs_uf:
        (tNcf_s, tNcs_s, tNuf_s) = cf_cs_uf[s]
        Ncf_s = float(tNcf_s)
        Ncs_s = float(tNcs_s)
        Nuf_s = float(tNuf_s)
    return float(Ncf_s - float(Ncs_s/(Ns+1)))

def m4_Dstar(s, star):
    global pass_list
    global fail_list
    Nf = float(len(fail_list))
    Ns = float(len(pass_list))
    if s in cf_cs_uf:
        (tNcf_s, tNcs_s, tNuf_s) = cf_cs_uf[s]
        Ncf_s = float(tNcf_s)
        Ncs_s = float(tNcs_s)
        Nuf_s = float(tNuf_s)
    if Nuf_s + Ncs_s == 0:
        return float('Inf')
    else:
        return float(float(Ncf_s**star)/float(Nuf_s+Ncs_s))


for arg in pass_list:
    getcov.start_trace()
    path = "../XMLdata/passing/" + arg
    mainF([path])
    getcov.end_trace()
    #getcov.merge(getcov.pass_stmt, getcov.now_stmt)
    getcov.set_last_trace_result('pass')
    getcov.now_stmt.clear()

for arg in fail_list:
    getcov.start_trace()
    path = "../XMLdata/failing/" + arg
    try:
        mainF([path])
    except:
        pass
    getcov.end_trace()
    #getcov.merge(getcov.fail_stmt, getcov.now_stmt)
    getcov.set_last_trace_result('fail')
    getcov.now_stmt.clear()

u = {}
u.update(getcov.pass_stmt)
u.update(getcov.fail_stmt)
for key in u.keys():
    cf = 0
    cs = 0
    if key in getcov.fail_stmt:
        cf = getcov.fail_stmt[key]
    if key in getcov.pass_stmt:
        cs = getcov.pass_stmt[key]
    uf = len(fail_list) - cf
    cf_cs_uf[key] = (cf, cs, uf)
m1 = {}
m2 = {}
m3 = {}
m4 = {}
for s in cf_cs_uf.keys():
    m1[s] = m1_Tarantula(s)
    m2[s] = m2_Ochiai(s)
    m3[s] = m3_Ochiai(s)
    m4[s] = m4_Dstar(s, 3)
m1_sort = sorted(m1.items(), key = operator.itemgetter(1), reverse = True)
m2_sort = sorted(m2.items(), key = operator.itemgetter(1), reverse = True)
m3_sort = sorted(m3.items(), key = operator.itemgetter(1), reverse = True)
m4_sort = sorted(m4.items(), key = operator.itemgetter(1), reverse = True)
m1f = open('m1.tsv', 'w')
m2f = open('m2.tsv', 'w')
m3f = open('m3.tsv', 'w')
m4f = open('m4.tsv', 'w')
for s, value in m1_sort:
    (filename, function, line) = s
    ostr = "%s\t%d\t%lf\n" % (filename, line, value)
    m1f.write(ostr)
for s, value in m2_sort:
    (filename, function, line) = s
    ostr = "%s\t%d\t%lf\n" % (filename, line, value)
    m2f.write(ostr)
for s, value in m3_sort:
    (filename, function, line) = s
    ostr = "%s\t%d\t%lf\n" % (filename, line, value)
    m3f.write(ostr)
for s, value in m4_sort:
    (filename, function, line) = s
    ostr = "%s\t%d\t%lf\n" % (filename, line, value)
    m4f.write(ostr)
m1f.close()
m2f.close()
m3f.close()
m4f.close()
