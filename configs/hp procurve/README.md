## Template HP Procurve

This template is refactored from Template Net HP Enterprise Switch SNMP because some/all of this models doesn't have the Objects OID

- IFALIAS
- IFNAME

```
root@computer:~# snmpwalk -v 2c -c public IP_SWITCH ifAlias
IF-MIB::ifAlias = No more variables left in this MIB View (It is past the end of the MIB tree)
root@computer:~# snmpwalk -v 2c -c public IP_SWITCH ifName
IF-MIB::ifName = No more variables left in this MIB View (It is past the end of the MIB tree)
```

Other discovery rules like 

- Entity discovery
- FAN discovery
- Memory discovery
- PSU discovery
- Temperature discovery
- Temp Status discovery

are deleted for the same reason (when you try to ask using SNMPWALK it returns)

```
SNMPv2-SMI::enterprises.11.2.14.11.5.1.1.2.1.1.1.1 = No more variables left in this MIB View (It is past the end of the MIB tree)
```

If you try to ask enterprises

```
snmpwalk -On -v 2c -c public 10.15.1.3 SNMPv2-SMI::enterprises
```

It returns 

```
.1.3.6.1.4.1 = No more variables left in this MIB View (It is past the end of the MIB tree)
```

### New features

Also I add some other items to Discovery like 

- Interface Admin status
- Interface Mtu

### Tested on

- HP Procurve J9450A (1810G-24)