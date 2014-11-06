import pycurl
import StringIO
import sys
import os
import getopt
import xml.etree.ElementTree as ET
import subprocess

class FileReader:
    def __init__(self, fp):
        self.fp = fp
    def read_callback(self, size):
        return self.fp.read(size)

def curl(*args):
    curl_path = '/usr/bin/curl'
    curl_list = [curl_path]
    for arg in args:
        # loop just in case we want to filter args in future.
        curl_list.append(arg)
        
    print curl_list
    curl_result = subprocess.Popen(
                 curl_list,
                 stderr=subprocess.PIPE,
                 stdout=subprocess.PIPE).communicate()[0]
    return curl_result

def getDefaultCurlObject():
    result = pycurl.Curl()
    
    result.setopt(pycurl.HTTPHEADER, ['Content-Type: text/xml'])
    result.setopt(pycurl.VERBOSE, 0)
    result.setopt(pycurl.USERPWD, user)
    result.setopt(pycurl.SSL_VERIFYPEER, False)
    result.setopt(pycurl.SSL_VERIFYHOST, False)
    
    return result
#END getDefaultCurlObject

#Method to search for a record in a given zone, returns true if one exists and false otherwise
def getRecordFromZone(zone, name):
    result = ''
    curlResult = StringIO.StringIO()
    curlCall = getDefaultCurlObject()
    searchUrl = dnsApiUrl + 'zones/' + zone + '/records.xml?search=' + name
    
    print searchUrl
    
    curlCall.setopt(pycurl.URL, searchUrl)
    curlCall.setopt(pycurl.WRITEFUNCTION, curlResult.write)
    curlCall.perform()
    
    root = ET.fromstring(curlResult.getvalue())
    
    if root.tag != nilClasses:
        result = curlResult.getvalue()
        
    curlCall.close()
        
    return result
#END getRecordFromZone

def createPathAsNeeded(path):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
#END createPathAsNeeded

def writeNewDnsRecordXml(xmlTree, name):
    print 'Calling writeNewDnsRecordXml'
    dnsRecordPath = 'records/' + name + '.xml'
    dnsRecordFullPath = os.path.join(os.path.dirname(__file__), dnsRecordPath)
    
    createPathAsNeeded(dnsRecordFullPath)
    xmlTree.write(dnsRecordFullPath)
    
    return dnsRecordFullPath
#END writeNewDnsRecordXml
    
def createNewRecordInZone(zone, name, content):
    print 'Calling createNewRecordInZone'
    #write a default xml file
    recordTag = ET.Element('record')
    
    contentTag = ET.SubElement(recordTag, 'content')
    contentTag.text = content
    
    managePtrTag = ET.SubElement(recordTag, 'manage-ptr')
    managePtrTag.set('type', 'boolean')
    managePtrTag.text = 'false'
    
    nameTag = ET.SubElement(recordTag, 'name')
    nameTag.text = name
    
    prioTag = ET.SubElement(recordTag, 'prio')
    prioTag.set('type', 'integer')
    prioTag.set('nil', 'true')
    
    ttlTag = ET.SubElement(recordTag, 'ttl')
    ttlTag.set('type', 'integer')
    ttlTag.text = '1400'

    typeTag = ET.SubElement(recordTag, 'type')
    typeTag.text = 'A'
    
    zoneIdTag = ET.SubElement(recordTag, 'zone-id')
    zoneIdTag.set('type', 'integer')
    zoneIdTag.text = zone
    
    tree = ET.ElementTree(recordTag)
    filepath = writeNewDnsRecordXml(tree, name)
    
   
    postUrl = dnsApiUrl + 'zones/' + zone + '/records'
    
    print 'Uploading file %s to url %s' % (filepath, postUrl)
    
    #use curl to get the files xml
    print curl('-d', '@' + filepath, postUrl, '-k', '-u', user, '--header', 'Content-Type: text/xml')
   
    #update the file with the id
    dnsRecord = getRecordFromZone(zone, name)
    print dnsRecord
    
    if len(dnsRecord) > 0 :
        print 'Record Inserted Successfully'
        #Turn the string into xml
        recordTag = ET.fromstring(dnsRecord)
        tree = ET.ElementTree(recordTag)
        filepath = writeNewDnsRecordXml(tree, name)
        print 'Original record file updated with record ID'
    else:
        print 'Record Not Added, An Error Occurred'
        exit()
    

def updateRecordInZone(dnsRecord, zone, name, content):
    print 'Calling updateRecordInZone'
    #update the xml file and write it back out to the records dir
    recordsTag = ET.fromstring(dnsRecord) #when searching the result is nested in a records tag
    recordTag = recordsTag[0]
    
    print ET.tostring(recordTag)
    
    recordTag.find('name').text = name
    recordTag.find('content').text = content
    recordId = recordTag.find('id').text
    
    tree = ET.ElementTree(recordTag)
    filepath = writeNewDnsRecordXml(tree, name)
    
    #use cURL to post the file and update the dns entry
    postUrl = dnsApiUrl + 'zones/' + zone + '/records/' + recordId + '.xml'
    print curl('-T', filepath, postUrl, '-k', '-u', user, '--header', 'Content-Type: text/xml')

#
# THE REAL WORK STARTS HERE
#

dnsApiUrl = 'https://dnsapi-test.cicd.useast.hpcloud.net/dnsapi/api/v1/'
#dnsApiUrl = 'https://ops-dnsapi01-aw2.ops.uswest.hpcloud.net/dnsapi/api/v1/'
usage = 'dnsapi.py -u <user:password> -n <dns name> -c <dns content> -z <zone id>'
letters = 'u:n:c:z:' # the : means an argument needs to be passed after the letter
keywords = ['user', 'name=', 'content=', 'zone-id=' ] # the = means that a value is expected after the keyword
nilClasses = 'nil-classes'

options, extraparams = getopt.getopt(sys.argv[1:], letters, keywords)

# starts at the second element of array since the first one is the script name
# extraparms are extra arguments passed after all option/keywords are assigned
# opts is a list containing the pair "option"/"value"
print 'Opts:',options
print 'Extra parameters:',extraparams

#Variables needed to pass to cURL
user = ''
name = ''
content = ''
zone = ''

#Check for the correct number of arguments
for opt, arg in options:
    if opt in ('-u', '--user'):
        user = arg
    elif opt in ('-n', '--name'):
        name = arg
    elif opt in ('-c', '--content'):
        content = arg
    elif opt in ('-z', '--zone-id'):
        zone = arg
        
if len(user) == 0 or len(name) == 0 or len(content) == 0 or len(zone) == 0:
    print usage
    exit()

print 'We may continue'

dnsRecord = getRecordFromZone(zone, name)

if len(dnsRecord) > 0 :
    print 'Record Found'
    updateRecordInZone(dnsRecord, zone, name, content)
else:
    print 'Record Not Found'
    createNewRecordInZone(zone, name, content)




#DEAD CODE HERE -- KEEP FOR REFERENCE
 #use curl to post the file - kept getting 500 errors
#    postUrl = dnsApiUrl + 'zones/' + zone + '/records'
#    
#    curlCall = getDefaultCurlObject()
#    curlResult = StringIO.StringIO()
#    curlCall.setopt(pycurl.WRITEFUNCTION, curlResult.write)
#    curlCall.setopt(pycurl.URL, postUrl)
#    
#    curlCall.setopt(pycurl.UPLOAD, 1)
#    #curlCall.setopt(pycurl.POST, 1)
#    filesize = os.path.getsize(filepath)
#    curlCall.setopt(pycurl.INFILESIZE, filesize)
#    curlCall.setopt(pycurl.POSTFIELDSIZE, filesize)
#    curlCall.setopt(pycurl.READFUNCTION, open(filepath, 'rb').read)

#    curlCall.setopt(pycurl.POST, 1)
#    curlCall.setopt(pycurl.POSTFIELDS, ET.tostring(recordTag))
#    curlCall.setopt(pycurl.HTTPPOST, [(name + '.xml', (pycurl.FORM_FILE, filepath))])
#    filesize = os.path.getsize(filename)
#    curlCall.setopt(pycurl.POSTFIELDSIZE, filesize)
#    fin = open(filename, 'rb')
#    curlCall.setopt(pycurl.READFUNCTION, fin.read)
    #curlCall.perform()
