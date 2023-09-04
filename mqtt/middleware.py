from mqtt.listener import publish_to_toggle
SWITCH_ACTION_TYPE = "switch"
TOGGLE_ACTION_TYPE = "toggle"

def validate_toggle_led_data(room, times):
    if not room or not times:
        return "Both room and times are required"
    if not isinstance(room, int) or not isinstance(times, int):
        return "Both room and times should be integers"

def handle_toggle_led(room:int, times:int):
    publish_to_toggle(str(room), str(times))

def dispatch_led_action(action_type: str, payload:dict):
    if action_type not in [SWITCH_ACTION_TYPE, TOGGLE_ACTION_TYPE]:
        return f"Invalid action type {action_type} requested"
    if action_type == TOGGLE_ACTION_TYPE:
        room = int(payload.get("room"))
        times = int(payload.get("times"))
        error = validate_toggle_led_data(room, times)
        if error:
            return error
        handle_toggle_led(room, times)