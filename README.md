## VM Start Retry

This repository contains a Python script (`vm_start_retry.py`) that manages the start operations of virtual machines (VMs) in Azure. The script reads the names of the VMs and their associated resource groups from a CSV file, checks the current power state of each VM, and attempts to start the VM if it is in a deallocated state.

## Requirements

- Python 3.6 or higher
- Azure CLI

## Usage

1. Prepare a CSV file with two columns: the first column should contain the resource group names and the second column should contain the VM names.

2. Run the script with the CSV file as an argument:

```bash
python vm_start_retry.py <path_to_your_csv_file>
```

The script will iterate over each row in the CSV file, check the power state of the corresponding VM, and attempt to start the VM if it is deallocated. The script will make a maximum of `MAX_ATTEMPTS` to start each VM, with a delay of `SLEEP_TIME` seconds between each attempt.

## Output

The script prints the resource group name, VM name, and current state of each VM. If a VM is in a deallocated state, the script will print the status of each attempt to start the VM.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)