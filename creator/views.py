from django.shortcuts import render

# Create your views here.
def index(request):
    # Sessions which works as global variable in add_fee fee function
    request.session['fee_cors'] = ''
    request.session['fee_nam'] = ''
    return render(request, 'cit/index.html')