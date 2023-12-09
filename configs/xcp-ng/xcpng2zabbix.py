#######################################################################################
# @author: Guille Rodriguez https://github.com/guillerg86
# @version: 2023-12-09 17:30
# @python-version: 2.7 (same as installed on XCP-ng DOM0)
#
# Permite a Zabbix (u otro sistema) extraer la información sobre las VMs
# que residen en el entorno XCP-ng. Es necesario disponer de un Zabbix Agent
# instalado en la DOM0, copiar la configuración con los UserParameter y añadir
# este script en /etc/zabbix/scripts/.
#
# Reiniciar el servicio de Zabbix Agent.
#
# Importar el fichero de template (que contiene 2 templates):
# - Template XCP-NG 8.2
# - Template XCP-NG 8.2 Guest VM
#
# En Zabbix dar de alta el equipo con XCP (recordar habilitar la comunicación en IPTables)
# y asignar el template: Template XCP-NG 8.2
#
#######################################################################################


import argparse
import json
import re
import subprocess
import datetime
import time

class XCPVirtualMachine():

    def __init__(self):
        self.uuid = None
        self.name = None

def configure_parser():
    """
    Configure arguments of this script
    :return:
    """
    # Configure parser
    parser = argparse.ArgumentParser(
        prog="XCPng to JSON",
        description="Export information of all VMs on XCP-NG server"
    )
    parser.add_argument('-a','--action', required=True, help="list/vmdetails", choices=["list","vmdetails"])
    parser.add_argument('-u','--uuid',required=False)
    parser.add_argument('-k','--key', required=False)
    args = parser.parse_args()
    return args

def datetime_from_utc_to_local(utc_datetime):
    #https://stackoverflow.com/questions/4770297/convert-utc-datetime-string-to-local-datetime
    now_timestamp = time.time()
    offset = datetime.datetime.fromtimestamp(now_timestamp) - datetime.datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime+offset


def execute_shell_cmd(cmd):
    return subprocess.check_output(cmd, shell=True)

def get_xe_value_from_key(output, key):
    for line in output:
        if line.strip().startswith(key):
            return (line.split(":")[1]).strip()
    return "Not found key = "+key

def parse_vmlist(shell_output):
    vms = []
    for line in shell_output:
        line = line.strip()
        if line.startswith("uuid"):
            vm = XCPVirtualMachine()
            vm.uuid = (line.split(":")[1]).strip()
            continue
        if line.startswith("name-label"):
            vm.name = (line.split(":")[1]).strip()
            vms.append(vm)

    return vms

def print_vmlist_zabbix_json(vms):
    dicts = { "vmlist": [{"{#VM.UUID}":vm.uuid, "{#VM.NAME}":vm.name} for vm in vms]}
    print json.dumps(dicts)


def get_vmlist():
    cmd = "sudo xe vm-list is-a-template=false is-a-snapshot=false is-control-domain=false is-default-template=false is-vmss-snapshot=false"
    try:
        result = (subprocess.check_output(cmd,shell=True)).split("\n")
        return parse_vmlist(result)
    except:
        print "Problems executing "+cmd


def get_vm_param_by_name(cmd, key):
    cmd += "param-name="+key
    try:
        result = execute_shell_cmd(cmd)
        return result.rstrip("\n")

    except:
        print "Problems executing "+cmd
        exit(-1)

def vm_get_virtual_interfaces(uuid):
    vm_vif_discover = "sudo xe vif-list vm-uuid=" + uuid + " params=uuid"
    vif_list = []
    try:
        result = execute_shell_cmd(vm_vif_discover).split("\n")
        for line in result:
            if line.strip().startswith("uuid"):
                vif_list.append(line.split(":")[1].strip())
        return vif_list
    except:
        print "Problem executing command "+vm_vif_discover
        exit(-1)

if __name__ == '__main__':

    args = configure_parser()
    regex_uuid = r"^[a-z0-9]{8}\-([a-z0-9]{4}\-){3}[a-z0-9]{12}$"
    regex_float = r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$'
    single_value_keys = ["power-state", "requires-reboot","hvm", "VCPUs-number",
                         "memory-actual", "memory-target", "memory-overhead", "memory-static-max",
                         "memory-dynamic-max", "memory-dynamic-min", "memory-static-min"]

    if args.action == "list":
        vms = get_vmlist()
        print_vmlist_zabbix_json(vms)

    elif args.action == "vmdetails":
        if not re.search(regex_uuid,args.uuid):
            print "Not a valid uuid defined, received ["+args.uuid+"]"
            exit(-1)

        vm_paramget_cmd = "sudo xe vm-param-get uuid=" + args.uuid + " "
        vif_command = "sudo xe vif-param-get uuid=" + args.uuid + " "

        if args.key in single_value_keys:
            print get_vm_param_by_name(vm_paramget_cmd, args.key)

        elif args.key == "auto-poweron":
            params = get_vm_param_by_name(vm_paramget_cmd, "other-config").split(";")
            value = "false"
            for param in params:
                if param.strip().startswith("auto_poweron"):
                    value = (param.split(":")[1]).strip()
            print value

        elif args.key == "VCPUs-utilisation":
            data = get_vm_param_by_name(vm_paramget_cmd, "VCPUs-utilisation").strip()
            if len(data) > 0:
                cpus_usage_array = data.split(";")
                num_cpus = len(cpus_usage_array)
                cpu_usage = 0
                for cpu in cpus_usage_array:
                    cpu_usage += float((cpu.split(":"))[1].strip())
                print cpu_usage/num_cpus
            else:
                # VM is powered off, so parameter is empty
                print 0

        elif args.key == "start-time":
            date_str = get_vm_param_by_name(vm_paramget_cmd, args.key)
            date_dt = datetime.datetime.strptime(date_str,"%Y%m%dT%H:%M:%SZ")
            date_tz = datetime_from_utc_to_local(date_dt)
            print time.mktime(date_tz.timetuple())
        elif args.key == "uptime":
            date_str = get_vm_param_by_name(vm_paramget_cmd, "start-time")
            if date_str.startswith("19700101"):
                print 0
            else:
                date_dt = datetime.datetime.strptime(date_str, "%Y%m%dT%H:%M:%SZ")
                date_tz = datetime_from_utc_to_local(date_dt)
                now = datetime.datetime.fromtimestamp(time.time())
                start_timestamp = time.mktime(date_tz.timetuple())
                now_timestamp = time.mktime(now.timetuple())
                print abs(now_timestamp - start_timestamp)


        ## NETWORKS
        elif args.key == "discover-networks":
            vif_list = vm_get_virtual_interfaces(args.uuid)
            dicts = {'vif_list': [{'{#VM.VIF.UUID}': vif} for vif in vif_list]}
            print json.dumps(dicts)

        elif args.key == "vif-mac-addr":
            data = execute_shell_cmd(vif_command+" param-name=MAC")
            print data.rstrip("\n")
        elif args.key == "vif-mtu":
            data = execute_shell_cmd(vif_command+" param-name=MTU")
            print data.rstrip("\n")
        elif args.key == "vif-kbytes-rcvd":
            data = execute_shell_cmd(vif_command+" param-name=io_read_kbs").rstrip("\n")
            if bool(re.match(regex_float,data)):
                print data
            else:
                print 0
        elif args.key == "vif-kbytes-sent":
            data = execute_shell_cmd(vif_command+" param-name=io_write_kbs").rstrip("\n")
            if bool(re.match(regex_float,data)):
                print data
            else:
                print 0
        elif args.key == "vif-network-name":
            data = execute_shell_cmd(vif_command+" param-name=network-name-label")
            print data.rstrip("\n")