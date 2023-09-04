from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from mqtt.middleware import dispatch_led_action, TOGGLE_ACTION_TYPE, SWITCH_ACTION_TYPE

def home(request: HttpRequest, *args, **kwargs):
    if request.method == "POST":
        print(request.POST)
        action_type = request.POST.get("actionType")
        if action_type == TOGGLE_ACTION_TYPE:
            payload = {"room": request.POST.get("room"), "times": request.POST.get("toggleTimes")}
            error = dispatch_led_action(action_type, payload)
            if error:
                return HttpResponse(error)
            else:
                return HttpResponse("Success")
    context = {"switch_action":SWITCH_ACTION_TYPE, "toggle_action":TOGGLE_ACTION_TYPE}
    return render(request, "monitor/home.html", context)