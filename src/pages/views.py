from django.shortcuts import render
from django.template import loader
from django.db import transaction
from .models import Account, Donation
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
        donation_message = request.POST.get('donation')

        transfer(sender, receiver, amount)

        Donation.objects.create(message=donation_message)

        accounts = Account.objects.all()
        donation_messages = Donation.objects.all()

        context = {'accounts': accounts, 'donation_messages': donation_messages}

    accounts = Account.objects.all()
    donation_messages = Donation.objects.all()

    context = {'accounts': accounts, 'donation_messages': donation_messages}

    return render(request, 'pages/donations.html', context)
