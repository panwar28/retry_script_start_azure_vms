#!/usr/bin/python
# Author: Umesh Panwar
# Date: June-05, 2024
# This script is to start and stop the VMs in sequence in Azure
# This script will retry the operation if it fails
# The number of attempts and sleep time between the attempts can be configured
# The script will move to the next VM if the max attempts are reached
# This script will read the virtual machine names and resource group name from a csv file. 
# The csv file should have two columns, the first column should be the resource group name and the second column should be the VM name
# Pass the csv file as an argument to the script to start/stop the VMs. 

# Import the required libraries
import os
import time
import csv
import sys
import subprocess

# Check if the csv file is passed as an argument
if len(sys.argv) < 2:
    print('Please pass the csv file as an argument')
    sys.exit(1)


# Define the maximum attempts and sleep time between the attempts
MAX_ATTEMPTS = 3
SLEEP_TIME = 30
csv_file = sys.argv[1]

# Open the csv file
with open(csv_file, 'r') as file:
    read = csv.reader(file)
    vm_list = list(read)

# Iterate over the vm_list
for row in vm_list:
    resource_group_name = row[0]
    vm_name = row[1]
    print(f'Resource Group Name: {resource_group_name}, VM Name: {vm_name}')
    cmd = f"az vm show --resource-group {resource_group_name} --name {vm_name} -d --query powerState -o tsv"
    # Check command output and start the VM if it is in deallocated state
    returned_value = subprocess.check_output(cmd, shell=True)
    returned_value = returned_value.decode('utf-8').strip()
    print(f'Current Status of the VM {vm_name}:', returned_value)
    if returned_value == 'VM deallocated':
        for i in range(MAX_ATTEMPTS):
            cmd = f"az vm start --resource-group {resource_group_name} --name {vm_name}"
            returned_value = subprocess.check_output(cmd, shell=True)
            # Checking status of the VM
            cmd = f"az vm show --resource-group {resource_group_name} --name {vm_name} -d --query powerState -o tsv"
            returned_value = subprocess.check_output(cmd, shell=True)
            returned_value = returned_value.decode('utf-8').strip()
            print(f'Current Status of the VM {vm_name}:', returned_value)
            if returned_value == 'VM starting':
                print('VM is starting, waiting for 30 seconds')
                time.sleep(SLEEP_TIME)
                continue           
            if returned_value == 'VM running':
                print('VM started successfully')
                break
            else:
                print('VM start failed')
                time.sleep(SLEEP_TIME)
        else:
            print(f'Max attempts reached, Could not start the VM {vm_name} in resource group {resource_group_name}')
            continue
    else:
        print(f'VM {vm_name} was not in deallocated state so did not attempt to restart VM {vm_name} in resource group {resource_group_name}.')
        print(f'Current status of VM {vm_name} is:', returned_value)
        continue
print('Been through all the VMs in the list, their status has been checked and started if they were stopped.')