import json,os,pprint

def getHost(fname):
	f = open(fname)	
	try: 
		data = json.load(f)
		hostname = data['payload']['hostname']
		ip= data['payload']['ipv4_address']		
		hostfile = open('hosts','a')
		hostfile.write(hostname+'\t'+ip+'\n')
		print hostname,ip 
		hostfile.close()
	except:
		pass
	f.close()
def getHostFile(tmpdir):
	for fname in os.listdir(tmpdir):
		getHost(tmpdir+fname)
def readIronic(fname):
	with open(fname) as f1:
		line = f1.readlines()
		for i in range(0,len(line)):
			f2 = open(tmpdir+str(i)+'.json','w')
			f2.write(line[i])
        	f2.close()
	f1.close()
def checkDir(d):
	if not os.path.exists(d):
		os.makedirs(d)

tmpdir = 'tmp/'
checkDir(tmpdir)
readIronic("testironic2.json")
getHostFile(tmpdir)
