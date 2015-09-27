from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import RequestContext
from app.models import Word
from django.template import Context
from django.template.loader import get_template
import predict
import os,time
import subprocess as sub
import json
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

	tweet=[]
	sentiment=[]
	count1=0
	count2=0
	os.system('javac -classpath "lib/*:." SimpleStream.java')
	var=['java -classpath' , '"lib/*:."' , 'SimpleStream']
	var.append(m)
	command =  " ".join(var)
	p = os.popen(command,"r")
	count=0
	while count<13:
		line = p.readline()
		if count>2:
			if count%2==0:
				sentiment.append(line)
				if "Positive" in line:
					count1+=1
				if "Negative" in line:
					count2+=1
			elif count%2==1:
				tweet.append(line)
		count+=1

	json_tweet = json.dumps(tweet)
	json_sentiment = json.dumps(sentiment)

	cont = RequestContext(request,{'tweets_array':tweet,'sent_array':sentiment,'count1':count1,'count2':count2})


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