from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import RequestContext
from app.models import Word
from django.template import Context
from django.template.loader import get_template
import predict

# Create your views here.

def  home(request):
	return render(request,'sign.html')

@csrf_exempt
def keyword(request):
	return render(request,'keyword.html',content_type="")

@csrf_exempt
def text(request):
	return render(request,'textword.html',content_type="")

@csrf_exempt
def keyres(request):
	if request.method == "POST":
		m  = request.POST.get('key')
	temp = get_template('keyres.html')
	cont = RequestContext(request,{'x':m})
	return HttpResponse(temp.render(cont))

@csrf_exempt
def textres(request):
	if request.method == "POST":
		x  = request.POST.get('content')
	temp = get_template('textres.html')
	new_x = str(x)

	val = predict.main(new_x)

	cont = RequestContext(request,{'string':x,'sentiment':val})
	return HttpResponse(temp.render(cont))