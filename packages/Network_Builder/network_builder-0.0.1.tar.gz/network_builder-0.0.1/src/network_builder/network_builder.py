"""
This is the network_builder module. 
It contains classes and functions to load device and task data from files and handle exceptions.
"""

import json
import netmiko

class UnimplementedDeviceType(Exception):
    """Exception raised when the device system type is not implemented.

    Attributes:
        message -- explanation of the error
    """
    pass

class FileLoader:
    """Class for loading device and task data from files.

    Attributes:
        device_file_path -- path to the device data file
        tasks_file_path -- path to the tasks data file
    """
    def __init__(self, device_file_path, tasks_file_path):
        self.device_file_path = device_file_path
        self.tasks_file_path = tasks_file_path

    def load_device_data(self):
        with open(self.device_file_path, encoding='utf-8') as device_file:
            self.device_data = json.load(device_file)
            return self.device_data

    def load_tasks_data(self):
        with open(self.tasks_file_path, encoding='utf-8') as tasks_file:
            self.tasks_data = json.load(tasks_file)
            return self.tasks_data

class TaskManager:
    """Class for managing tasks.

    Attributes:
        taskname -- name of the task
        taskdescription -- description of the task
        target -- target of the task
        command -- command of the task
        arguments -- arguments of the task
    """
    def __init__(self, taskname, taskdescription, target, command, arguments):
        self.taskname = taskname
        self.taskdescription = taskdescription
        self.target = target
        self.command = command
        self.arguments = arguments

class CommandManager:
    """Class for managing commands.

    Attributes:
        name -- name of the device
        ip -- IP address of the device
        port -- port of the device
        device_type -- type of the device

    Methods:
        send_command -- sends a command to the device
        send_config -- sends a configuration to the device
    """
    def __init__(self, name, ip, port, device_type):
        self.name = name
        self.ip = ip
        self.port = port
        self.device_type = device_type

    def send_command(self, command):
        try:
            if self.device_type == 'cisco_ios':
                connection = netmiko.ConnectHandler(
                    device_type=self.device_type,
                    ip=self.ip,
                    port=self.port,
                    username='admin',
                    password='cisco'
                )
                output = connection.send_command(command)
                print(output)
                connection.disconnect()
            else:
                raise UnimplementedDeviceType(f'{self.device_type} is not implemented')
        except Exception as e:
            print(f'Error: {e}')

    def send_config(self, config):
        try:
            if self.device_type == 'cisco_ios':
                connection = netmiko.ConnectHandler(
                    device_type=self.device_type,
                    ip=self.ip,
                    port=self.port,
                    username='admin',
                    password='cisco'
                )
                output = connection.send_config_set(config)
                print(output)
                connection.disconnect()
            else:
                raise UnimplementedDeviceType(f'{self.device_type} is not implemented')
        except Exception as e:
            print(f'Error: {e}')

def main(task_file, device_file):
    file_loader = FileLoader(device_file, task_file)
    device_data = file_loader.load_device_data()
    tasks_data = file_loader.load_tasks_data()

    device_list = []
    tasks_list = []

    devices = device_data['devices']
    for device in devices:
        name = device['name']
        ip = device['ip']
        port = device['port']
        device_type = device['type']

        network_device = CommandManager(name, ip, port, device_type)
        device_list.append(network_device)

    tasks = tasks_data['tasks']
    for task in tasks:
        name = task['taskname']
        description = task['taskdescription']
        target = task['target']
        command = task['command']
        arguments = task['arguments']

        task = TaskManager(name, description, target, command, arguments)
        tasks_list.append(task)

    for task in tasks_list:
        for device in device_list:
            if device.name == task.target:
                dev = CommandManager(device.name, device.ip, device.port, device.device_type)
                dev.send_command(task.command)
                if task.arguments:
                    dev.send_command(f'{task.command} {task.arguments}')
            else:
                print(f'Device {task.target} not found')
                pass
