#! python3
# Checks if processes are online, or offline or online,
# and outputs this data via JSON for use on Dashboard Website or is just callable by site??.
# Additionally, it is able to bring offline processes back online (automatically, or manually)

# Copyright AGoldfarb on May 2016

import json
import yaml   # pip install pyYAML
import ps
import subprocess
import os
import logging

__version__ = "0.1"
log = logging.getLogger("Process Monitor")
if 'config' not in locals():
    file = os.path.join(os.path.dirname(__file__), "config.yaml")
    with open(file, 'r') as yaml_file:
        config = yaml.load(yaml_file)
        log.info("Config file loaded!")


def check_processes_status():
    """

    :return: Returns a list of dictionaries representing each host.
    Each host contains the hostname ('hostname') and a list of processes ('processes')
    Each list of processes contains a dictionary representing a process with keys: 'name' & 'status'

    :rtype: list[dict]
    """

    # with open("config.yaml", 'r') as yaml_file:
    #     config = yaml.load(yaml_file)
    process_config = config['hosts']

    data = []
    for host in process_config:
        hostname = host['hostname']
        process_data = []
        for process in host['processes']:
            process_status = ps.check_process(process['name'], hostname)
            if process_status == 1:
                status = 'up'
            elif process_status > 1:
                status = 'up'
            else:
                status = 'down'
            process_data.append({'name': process['name'], 'status': status})
        data.append({"name": hostname, 'process_data': process_data})

    return data


def bring_up_process(path, name):
    # subprocess.Popen(name, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    # Todo: Maybe add in some better logic for concat path + name
    os.system(path+name)


def bring_down_process(name):
    raise NotImplementedError


if __name__ == '__main__':
    # bring_up_process("", "notepad.exe")
    logging.basicConfig(level=logging.INFO)
    print(check_processes_status())

