from django.shortcuts import render
from django.template import loader
from django.db import transaction
from .models import Account
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils.html import escape


# Create your views here.

#@transaction.atomic
#@login_required
def transfer(sender, receiver, amount):
	acc1 = Account.objects.get(iban=sender)
	acc2 = Account.objects.get(iban=receiver)

	if acc1 != acc2:
		if amount >= 0 and amount <= acc1.balance:
			acc1.balance -= amount
			acc2.balance += amount

	acc1.save()
	acc2.save()

@csrf_exempt
#@login_required
def homePageView(request):
	if request.method == 'POST':
		sender = request.POST.get('from')
		receiver = request.POST.get('to')
		amount = int(request.POST.get('amount'))
		greeting = request.POST.get('greeting')
		transfer(sender, receiver, amount)

	accounts = Account.objects.all()
	context = {'accounts': accounts, 'greeting': greeting}

	success_message = "Payment with following greeting succeeded: " + greeting
	#success_message = f"Payment with following greeting succeeded: {escape(greeting)}"
	messages.success(request, success_message)
	
	return render(request, 'pages/index.html', context)
