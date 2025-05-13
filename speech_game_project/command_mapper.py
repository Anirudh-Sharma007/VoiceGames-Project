def map_command(command):
    command_mapping = {
        "up": "MOVE_UP",
        "down": "MOVE_DOWN",
        "left": "MOVE_LEFT",
        "right": "MOVE_RIGHT",
        "stop": "STOP"
    }
    return command_mapping.get(command, None)
