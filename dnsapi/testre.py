import re,os,sys
def validHost(hostname):
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1] # strip exactly one dot from the right, if present
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))

def ipFilter(iplist):
	for ip in iplist.split(","): 
		# find ip with 10.23.*.*
		regex = re.compile("\s*(10\.23\.[0-9]*\.[0-9]*)\s*$")
		match = regex.findall(ip)
		if len(match)!=0: 
			print match[0]
			return match[0]
def processHosts(hostfile):
	newhostfile = hostfile+'.tmp'
	with open(hostfile) as f1:
		line = f1.readlines()
		for p in line: 
			host = p.split("\t")[0]
			iplist = p.split("\t")[1]
			ip = ipFilter(iplist)
			# find last dash from the end, split string into two parts
			regex = re.compile("([A-Za-z0-9-]*)-([A-Za-z0-9]*)$")
			newhost = regex.findall(host)
			f2 = open(newhostfile,'a')
			if len(newhost)!=0:
				print host+" => "+newhost[0][0]
				f2.write(newhost[0][0]+'\t'+ip+'\n')
			else:
				print host+" not changed."
				f2.write(host+'\t'+iplist)
			f2.close()
	f1.close()
	os.remove(hostfile)
	os.rename(newhostfile,hostfile)	
def test():
	string='ov--soswiftstorage1-SwiftScaleoutObject1-btkaswiffhik'
	regex = re.compile("([A-Za-z0-9-]*)-([A-Za-z0-9]*)$")
	print regex.findall(string)
def test2(hostfile):
	with open(hostfile) as f1:
		line = f1.readlines()
		for p in line:
			iplist = p.split("\t")[1]
			ipFilter(iplist)
	f1.close()

# main
hostfile = 'hosts'
processHosts(hostfile)

