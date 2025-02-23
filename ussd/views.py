from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ussd.ussd_handlers.registration import handle_registration
from ussd.ussd_handlers.apply_loan import apply_loan
from ussd.ussd_handlers.repay_loan import repay_loan
from ussd.ussd_handlers.check_loan_limit import check_loan_limit
from ussd.ussd_handlers.mini_statement import mini_statement
from ussd import constants

@csrf_exempt
def ussd_view(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed", status=405)

    session_id = request.POST.get("sessionId", "").strip()
    phone_number = request.POST.get("phoneNumber", "").strip()
    text = request.POST.get("text", "").strip()
    text_parts = text.split("*")

    response = ""
    
    registered_users = ['+25479904353'] 
    
    is_registered = phone_number in registered_users
    
    if not is_registered:
        if text == "":
            response = constants.WELCOME_MESSAGE_NEW_USER
        else:
            response = handle_registration(text_parts, phone_number)
            
    else:
        if text == "":
            response = constants.WELCOME_MESSAGE_REGISTERED_USER
        elif text_parts[0] == "1":
            response = apply_loan(request,session_id,text, phone_number)
        elif text_parts[1] == "2":
            response = repay_loan(request, session_id, text, phone_number)
        elif text_parts[2] == "3":
            response = check_loan_limit(request, session_id, text, phone_number)
        elif text_parts[3] == "4":
            response = mini_statement(request, session_id, text, phone_number)
        elif text_parts[4] == "5":
            response = constants.EXIT_MESSAGE
        else:
            response = constants.INVALID_OPTION
    

   

    return HttpResponse(response, content_type='text/plain')
