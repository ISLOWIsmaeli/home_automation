from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from mqtt.middleware import (
    dispatch_led_action,
    TOGGLE_ACTION_TYPE,
    SWITCH_ACTION_TYPE,
)
from mqtt.listener import (
    decode_toggle_led_feedback,
    decode_switch_led_feedback,#
    LED_SWITCH_STATUS,
    LED_TOGGLE_STATUS,
)

# trial comment
def home(request: HttpRequest, *args, **kwargs):
    context = {
        "switch_action": SWITCH_ACTION_TYPE,
        "toggle_action": TOGGLE_ACTION_TYPE,
        "rooms": [1, 2],
    }
    if request.method == "POST":
        action_type = request.POST.get("actionType")
        if action_type == TOGGLE_ACTION_TYPE:
            payload = {
                "room": request.POST.get("room"),
                "times": request.POST.get("toggleTimes"),
            }
            error = dispatch_led_action(action_type, payload)
            if error:
                return HttpResponse(error)
        elif action_type == SWITCH_ACTION_TYPE:
            payload = {
                "room": request.POST.get("room"),
                "state": request.POST.get("state"),
            }
            error = dispatch_led_action(action_type, payload)
            if error:
                return HttpResponse(error)
            # else:
            #     return HttpResponse(f"{action_type} Success")
    # context["led_statuses"] = decode_toggle_led_feedback(LED_STATUS)
    return render(request, "monitor/home.html", context)


# def toggle_feedback(request: HttpRequest, *args, **kwargs):
def display_led_status(request: HttpRequest, *args, **kwargs):
    led_toggle_statuses = LED_TOGGLE_STATUS
    led_switch_statuses = LED_SWITCH_STATUS
    print(led_switch_statuses)
    print(decode_switch_led_feedback(led_switch_statuses))
    return JsonResponse(
        {
            "led_toggle_statuses": decode_toggle_led_feedback(led_toggle_statuses),
            "led_switch_statuses": decode_switch_led_feedback(led_switch_statuses),
        }
    )
