## Template OS FreeBSD

This template is the same as Template OS FreeBSD but with a new item in Discovery Network Interfaces. 

- Interface Operational Status

You need to add this UserParameter to agents (remember reboot the agent after add UserParameter)

```
UserParameter=net.if.operstatus[*],ifconfig $1 | grep status | cut -d ':' -f 2 | sed 's/ //g'
```

Also all discovered interfaces has a new application tag for group all info of that interface in one tag.

```
Application: Interface {#IFNAME}
```` 