from django.http import HttpResponse
from decimal import Decimal
from fleximembers.models import FlexiCashMember


def check_limit_handler(request, session_id, phone_number, text):
    member = FlexiCashMember.objects.filter(phone=phone_number).first()
    
    if not member:
        return HttpResponse("END Member not found. Please register first.", content_type="text/plain")

    # Calculate loan limit based on criteria
    if member.member_balance > 0:
        response = "END You have an outstanding balance. Please clear it to qualify for a limit."
    elif member.credit_score < 50:  # Example credit score threshold
        response = "END You dont qualify for a loan,please try again later."
    else:
        # Calculate loan limit based on credit score or other criteria
        loan_limit = member.loan_limit 
        member.save()  # Update loan limit in database

        response = f"END Your loan limit is {loan_limit}. You can apply for a loan within this limit."
    
    return HttpResponse(response, content_type="text/plain")