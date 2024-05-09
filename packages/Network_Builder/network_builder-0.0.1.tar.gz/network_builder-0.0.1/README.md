# Network-Builder

## Device config json example:
```json
{
  "devices": [
    {
      "name": "Device_Name_1",
      "ip": "192.168.1.1",
      "port": 22,
      "type": "cisco_ios"
    },
    {
      "name": "Device_Name_2",
      "ip": "10.10.0.23",
      "port": 22,
      "type": "cisco_ios"
    }
  ]
}
```

## Task list json example:
``` json
{
    "tasks": [
        {
            "taskname": "Task Name 1",
            "taskdescription": "Task without argument",
            "target": "Device_Name_1",
            "command": "command_of_your_choice",
            "arguments": []
        },
        {
            "taskname": "Task Name 2",
            "taskdescription": "Task with argument",
            "target": "Device_Name_2",
            "command": "command_of_your_choice_with_argument",
            "arguments": [
                "argument_1",
                "argument_2"
            ]
        }
    ]
}
```
