## Template TP-Link SG108E

This template allows to monitor TP-Link SG108E switch. This switch is a home switch, so doesn't have SNMP or SSH, just a website.

Check images folder for examples


### Items

- Hostname
- Firmware
- Hardware
- Mac Address

### Triggers

- Hostname changed
- Firmware changed
- Hardware changed
- MAC address changed

### Discovery rules

There's a discovery rule for detect network ports. When executed, it returns a json with port number and adminstatus

```
{
    "interfaces": [
        {
            "{#IFNUMBER}": 1,
            "{#IFADMINSTATUS}": "1"
        },
        {
            "{#IFNUMBER}": 2,
            "{#IFADMINSTATUS}": "0"
        },
        {
            "{#IFNUMBER}": 3,
            "{#IFADMINSTATUS}": "0"
        },
        {
            "{#IFNUMBER}": 4,
            "{#IFADMINSTATUS}": "0"
        },
        {
            "{#IFNUMBER}": 5,
            "{#IFADMINSTATUS}": "1"
        },
        {
            "{#IFNUMBER}": 6,
            "{#IFADMINSTATUS}": "1"
        },
        {
            "{#IFNUMBER}": 7,
            "{#IFADMINSTATUS}": "1"
        },
        {
            "{#IFNUMBER}": 8,
            "{#IFADMINSTATUS}": "1"
        }
    ]
}
```

Only creates Item prototypes when {#IFADMINSTATUS} = 1 (enabled)

#### Item prototypes 

- Admin status
- Operational status
- Flow control actual
- Flow control configuration
- Received packets
- Received packets error
- Transmitted packets
- Transmitted packets error
- Trunk status
- Speed configuration
- Speed actual
- Speed (bps)

#### Trigger prototypes

- Interface: Link down
- Interface: Link speed is lower than before
- Interface: Flow control changed
- Interface: Speed configuration changed

## Tested on

- TP-Link SG108E v6.0 
  - Firmware: 20230218 ✔
  - Firmware: 20201208 ✔

## Usage

If you want to test before install on Zabbix, you need a machine with Python 3.x installed (tested on 3.12).

**Get System Info**

```
python3 tplinkswitch2zabbix.py -i IP_ADDRESS -u WEBUSERNAME -p WEBPASSWORD -a sysinfo
```

Output be like:

```
{
    "firmware": "1.0.0 Build 20230218 Rel.50633",
    "hardware": "TL-SG108E 6.0",
    "description": "PSC-SW-SG108E",
    "mac_address": "00:31:92:B3:EE:12",
    "ip_address": "10.15.1.2",
    "netmask": "255.255.255.0",
    "gateway": "10.15.1.1",
    "port_number": 0,
    "ports": []
}
```

This method only takes system information, no ports information.

**Discovery ports**

```
python3 tplinkswitch2zabbix.py -i IP_ADDRESS -u WEBUSERNAME -p WEBPASSWORD -a discovery
```

Output be like:

```
{
    "interfaces": [
        {
            "{#IFNUMBER}": 1,
            "{#IFADMINSTATUS}": "1"
        },
        {
            "{#IFNUMBER}": 2,
            "{#IFADMINSTATUS}": "0"
        },
        ...
		...
		{
            "{#IFNUMBER}": 8,
            "{#IFADMINSTATUS}": "1"
        }
    ]
}
```

**Port detail**

```
python3 tplinkswitch2zabbix.py -i IP_ADDRESS -u WEBUSERNAME -p WEBPASSWORD -a portinfo --port-number 8
```

Output be like

```
{
    "port_number": 8,
    "admin_status": "1",
    "trunk_status": "0",
    "operation_status": 1,
    "speed_config": "1",
    "speed_actual": "6",
    "speed_bps": 1000000000,
    "flowcontrol_config": "0",
    "flowcontrol_actual": "0",
    "transmitted_packets": "324937",
    "transmitted_packets_error": "0",
    "received_packets": "615998",
    "received_packets_error": "708"
}
```