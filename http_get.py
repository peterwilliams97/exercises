import httplib,sys


def comment(s):
    return '<!-- ' + str(s) + ' -->'

spacer = '----------------------------------------------------------'    

def showResponse(path, data):
    print comment(spacer)
    print comment(data)
    print comment(spacer)

    
    
def getTarget(web_site, path):
    conn = httplib.HTTPConnection(sharp_site)
    print comment('GET ' + path)
    conn.request('GET', path)
    r = conn.getresponse()
    print comment(str(r.status) + ' ' + str(r.reason))
    if r.status == 200:
        showResponse(path, r.read())
    conn.close()
 

    
def getLines(lines):
    "Split a string of lines into an array of strings"
    return [l.strip() for l in lines.strip().split('\n')]
    
if __name__ == '__main__':
    if True:
        targets = getLines(target_list)
    else:
        targets = sys.argv[1:]
     
    if len(targets) == 0:
        print 'Usage: http_get web_site target1 target2 ....'
    else:    
        for target in targets:
            getTarget(target)