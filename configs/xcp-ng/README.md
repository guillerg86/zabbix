# Templates

Tested on Zabbix 6.4 version but sure will Work on 6.0, 6.2 and maybe earlier versions

## Template XCP-ng 8.2 

This template is for the Hipervisor XCP-ng 8.2. Execute a discovery for all VMs inside Hypervisor, for each VM discovered, Zabbix create a new Host (Host Prototype) and assign a new Template XCP-ng 8.2 Guest VM with this parameters.

- HOST: VM UUID
- VISIBLE NAME: NAME_LABEL VM


## Template XCP-ng 8.2 Guest VM

### Items

|ITEM NAME|INTERVAL|DESCRIPTION|
|-|-|-|
|Auto poweron|1h|Check if VM has configured auto power on|
|CPU Usage|1m|Gets the cpu usage of VM|
|HVM|10m|Check if HVM is enabled|
|Memory actual|1m|Gets the memory actual value|
|Memory dynamic max|10m|Gets the dynamic max memory configured|
|Memory dynamic min|10m|Gets the dynamic min memory configured|
|Memory static max|10m|Gets the static min memory configured|
|Memory static min|10m|Gets the static min memory configured|
|Memory overhead|1m|Gets the memory overhead value|
|Memory target|1m|Gets the memory target value|
|Number of virtual CPUs|10m|Get the number of virtual cpus VM has configured|
|Power state|1m|State of VM (halted, running, suspended, paused)|
|Requires reboot|10m|Check if XCP-ng tells if VM needs a reboot|
|Start-time|10m|Date and time when VM was powered on|
|Uptime|3m|Time since last poweron/reboot|


### Triggers

|TRIGGER NAME|DESCRIPTION|
|-|-|
|VM has been restarted (uptime < 10m)|VM uptime it's between 5s and 10m|
|VM is paused|VM has **autopoweron enabled** and status is paused|
|VM is suspended|VM has **autopoweron enabled** and status is suspended|
|VM is powered off|VM has **autopoweron enabled** and status is powered off|
|VM requires reboot|VM has enabled the **requires reboot** param|

### Discovery

#### Network discovery

Get all virtual interfaces attached to a VM and create items and a group for each VIF.

|ITEM NAME|INTERVAL|DESCRIPTION|
|-|-|-|
|KBytes received|1m|Kilobytes received on this VIF|
|KBytes transmitted|1m|Kilobytes transmitted from this VIF|
|MAC|1h|MAC Address of the VIF|
|MTU|1h|Configured MTU on the VIF|
|Network / vlan name|1h|Network / vlan name where this VIF is attached|




# Installation

Install Zabbix Agent on XCP-NG DOM0 (administration console). 

Copy configuration file xcg-ng.conf which includes UserParameters

```
cp xcp-ng.conf /etc/zabbix/zabbix_agentd.d/xcp-ng.conf
```

Copy xcpng2zabbix.py script. This script extract the info of the VMS, Network VIF.

```
mkdir /etc/zabbix/scripts
cp xcpng2zabbix.py /etc/zabbix/scripts/xcpng2zabbix.py
chmod +x /etc/zabbix/scripts/xcpng2zabbix.py
```

Restart Zabbix Agent

```
systemctl restart zabbix-agentd.service
```

Test the script from zabbix

```
su -c 'python2.7 /etc/zabbix/scripts/xcpng2zabbix.py -a list' -s /bin/bash zabbix
```

Output like this will be shown (but in one line)

```
{
  "vmlist": [
    {
      "{#VM.NAME}": "webserver",
      "{#VM.UUID}": "bc919918-cbdc-8bd6-ad15-dcae0f74c84c"
    },
    {
      "{#VM.NAME}": "puppet-ansible",
      "{#VM.UUID}": "0cf8f762-b654-febd-0cfb-b2dc7b53d67b"
    },
    {
      "{#VM.NAME}": "Splunk",
      "{#VM.UUID}": "9f10841b-37dc-bd58-a1f0-1ae6846b83bf"
    },
    {
      "{#VM.NAME}": "docker02",
      "{#VM.UUID}": "1b51519b-eae5-a2bb-b456-5dc4f20186e0"
    }
  ]
}
```

If some error like Timeout appears, you need to gran permisions to user Zabbix on sudoers. 

```
zabbix ALL=(ALL) NOPASSWD: ALL
```

For more security, you can only grant sudo to xe command. All commands inside script are executed with `sudo xe`

Now it's the time to check if Zabbix Agent daemon can execute and get data from script.

```
zabbix_agentd -t xcpng.vms.discovery
```

Output like 

```
xcpng.vms.discovery [t|{"vmlist": [{"{#VM.NAME}": "webserver", "{#VM.UUID}": "bc919918-cbdc-8bd6-ad15-dcae0f74c84c"}, {"{#VM.NAME}": "puppet-ansible", "{#VM.UUID}": "0cf8f762-b654-febd-0cfb-b2dc7b53d67b"}, {"{#VM.NAME}": "Splunk", "{#VM.UUID}": "9f10841b-37dc-bd58-a1f0-1ae6846b83bf"}, {"{#VM.NAME}": "docker02", "{#VM.UUID}": "1b51519b-eae5-a2bb-b456-5dc4f20186e0"}]}]
```

Now, assign the `Template XCP-NG 8.2` to XCP Server, and that's all

![VM on XCP-NG8.2 LatestData](latest-data-xcpng8.2-vm.png?raw=true "VM Latest Data")