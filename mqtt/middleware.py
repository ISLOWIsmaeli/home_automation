from mqtt.listener import (
    publish_to_toggle,
    publish_to_switch,
    LED_TOGGLE_STATUS,
    LED_SWITCH_STATUS,
    mqttc,
    TOGGLE_FEEDBACK_TOPIC,
)

SWITCH_ACTION_TYPE = "switch"
TOGGLE_ACTION_TYPE = "toggle"


def validate_data(room, times_or_state):
    if not isinstance(room, int) or not isinstance(times_or_state, int):
        return "Both parameters should be integers"
    if not room or (not times_or_state and times_or_state != 0):
        return "Both parameters are required"


def handle_switch_led(room: int, state: int):
    publish_to_switch(str(room), str(state))


def handle_toggle_led(room: int, times: int):
    publish_to_toggle(str(room), str(times))


def dispatch_led_action(action_type: str, payload: dict):
    try:
        if action_type not in [SWITCH_ACTION_TYPE, TOGGLE_ACTION_TYPE]:
            return f"Invalid action type {action_type} requested"
        if action_type == TOGGLE_ACTION_TYPE:
            room = int(payload.get("room"))
            times = int(payload.get("times"))
            error = validate_data(room, times)
            if error:
                return error
            handle_toggle_led(room, times)
        elif action_type == SWITCH_ACTION_TYPE:
            room = int(payload.get("room"))
            state = int(payload.get("state"))
            error = validate_data(room, state)
            if error:
                return error
            handle_switch_led(room, state)

    except:
        return "An error occurred ensure you have selected a room"
