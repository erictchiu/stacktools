### check power status of all nodes ***
a="10.22.13.17,TVJDICCN
10.22.13.15,KOOVYPTN
10.22.13.16,ICOOBXLG
10.22.13.33,PHBPDBWF
10.22.13.44,AIYBMPLY
10.22.13.46,XPUARMWT
10.22.13.50,ZLAZOIYV
10.22.13.51,ZZISCAJP
10.22.13.47,EPFAFZRY
10.22.13.55,RBDVPTBH" 
for b in $a; do echo ipmitool -I lanplus -H `echo $b|awk -F"," '{print $1}'` -U Administrator -P `echo $b|awk -F"," '{print $2}'` "power status"; done
