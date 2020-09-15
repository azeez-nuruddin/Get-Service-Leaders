# Get AOS Service Leaders
​
This script provides a simple interface to fetch Acropolis OS service leaders in a Nutnaix cluster.
​
This script should be run within a Controller VM SSH session.
​
## Usage
​
At CVM prompt, run the script as follows:
​
```
$ /home/nutanix/serviceability/bin/get_leader.py <service_name>
```
​
## Examples
​
```
$ /home/nutanix/serviceability/bin/get_leader.py lcm
```
​
```
$ /home/nutanix/serviceability/bin/get_leader.py lcm arithmos
```
​
```
$ /home/nutanix/serviceability/bin/get_leader.py lcm arithmos 'health server'
```
​
```
$ /home/nutanix/serviceability/bin/get_leader.py all
```
​
To print usage, simply run the script without any arguments.
​
Author: Azeez Nuruddin
​
## Files
​
- get_leader.py - Script
- get_leader.json - Data file
​
## Script Workflow
​
1. Read and load from JSON, defined AOS services and commands.
2. Read and validate service names in arguments.
3. Fetch Acropolis service leader from the Controller VM.
4. Parse output and print CVM leader IP address for these services.
5. Exit.
​
## Examples
​
```
nutanix@NTNX-19FM6H130137-A-CVM:10.63.18.96:~/azeezn$ ./get_leader.py ngt
ngt : 10.63.18.99
nutanix@NTNX-19FM6H130137-A-CVM:10.63.18.96:~/azeezn$
nutanix@NTNX-19FM6H130137-A-CVM:10.63.18.96:~/azeezn$ ./get_leader.py lcm arithmos "health server"
arithmos : 10.63.18.96
health server : 10.63.18.97
cm : 10.63.18.97
nutanix@NTNX-19FM6H130137-A-CVM:10.63.18.96:~/azeezn$
nutanix@NTNX-19FM6H130137-A-CVM:10.63.18.96:~/azeezn$ ./get_leader.py all
acropolis : 10.63.18.99
alert manager : 10.63.18.99
aplos : 10.63.18.96
aplos engine : 10.63.18.96
aplos stats publisher : <leader not found>
aplos vm scanner : <leader not found>
aplos webhook : <leader not found>
arithmos : 10.63.18.96
arithmoscollector : 10.63.18.98
cassandra : 10.63.18.99
cassandra monitor : 10.63.18.99
catalog : 10.63.18.99
cerebro : 10.63.18.99
...
...
prism monitor : 10.63.18.96
snmp : 10.63.18.99
snmp manager : 10.63.18.99
uhura : 10.63.18.99
zeuscollector : 10.63.18.96
zookeeper : 10.63.18.98
zookeeper monitor : 10.63.18.98
nutanix@NTNX-19FM6H130137-A-CVM:10.63.18.96:~/azeezn$
```
​
 ## Disclaimer
​
 This code is intended as a standalone example.  Subject to licensing restrictions defined on nutanix.dev, 
 this script can be downloaded, copied and/or modified in any way you see fit. Please be aware that all public 
 code samples provided by Nutanix are unofficial in nature, are provided as examples only, are unsupported and 
 will need to be heavily scrutinized and potentially modified before they can be used in a production environment. 
 All such code samples are provided on an as-is basis, and Nutanix expressly disclaims all warranties, express or 
 implied.
