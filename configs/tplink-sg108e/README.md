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
