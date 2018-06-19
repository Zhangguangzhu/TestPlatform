# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.http import HttpResponse, HttpResponseRedirect, Http404, StreamingHttpResponse
from django.shortcuts import render
from . import models
# from django.core.urlresolvers import  reverse
from django.urls import reverse
from . import forms
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required



# Create your views here.


def index(Request):
	return HttpResponse('hello')

@login_required #setting 中设置变量LOGIN_URL = '/login/',不使用装饰器可通过request.user.is_authenticate()判断
def homepage(Request):
	userinfo = {}
	userinfo['username'] = Request.user.username
	userinfo['status'] = True
	title_obj = forms.VoteTitle()
	articles = models.Article.objects.all()
	return render(Request, 'blogapp/homepage.html', {'articles': articles,'title_obj':title_obj,'userinfo':userinfo})


def articlepage(request, article_prikey):
	if request.method == "POST":
		article = models.Article.objects.get(pk=article_prikey)
		article.counter += 1
		article.save()
		return HttpResponseRedirect(reverse('blog:article_page', args=(article_prikey,)))
	else:
		article = models.Article.objects.get(pk=article_prikey)
		return render(request,'blogapp/article_page.html',{'article':article})

def myArticle(request):
	if request.method == "POST":
		print('nonononon!')
		article = forms.Article(request.POST)
		if article.is_valid():
			title = article.cleaned_data['title']
			content = article.cleaned_data['content']
			author = request.user.username
			models.Article.objects.create(title=title, content=content, author=author)
			return HttpResponseRedirect(reverse('blog:myArticle'))
	else:
		articles = models.Article.objects.filter(author=request.user.username)
		articleform = forms.Article()
		return render(request, 'blogapp/myArticle.html', {'articles':articles,'articleform':articleform})

def editArticle(request, article_prikey):
	article = models.Article.objects.get(author=request.user.username, pk=article_prikey)
	if article:
		if request.method == "POST":
			# article.title = request.POST['title']
			article.content = request.POST['content']
			article.save()
			return HttpResponse("修改成功哦")
		else:
			article_form = forms.Article()
			return render(request, 'blogapp/editarticle.html', {'article':article, 'article_form':article_form})
	else:
		raise Http404('访问的内容不存在')




def test_page(Request, num):
	return HttpResponse('this is test page:%s' % (num))

def vote_all_result(request):
	errors_obj = " "
	if request.method == "POST":
		form_post = forms.VoteTitle(request.POST)
		if form_post.is_valid():
			title = form_post.cleaned_data['vote_title'] #is_valid 返回true后，post的值保存在cleaned_data 中以字典形式
			article = models.Article.objects.get(pk=title)
			article.counter += 1
			article.save()
		else:
			# print 'error'
			errors_obj = form_post.errors
			# print form_post.errors["vote_title"]
			# print form_post.errors["vote_title"][0]
			# print type(form_post.errors["vote_title"])
	title_obj = forms.VoteTitle(
		initial={'vote_title':'标题1'} #列表默认值
	)
	articles = models.Article.objects.all()
	return HttpResponseRedirect(reverse('blog:homepage'))

def upload_file(request):
	articles = models.Article.objects.all()
	if request.method == "POST":
		# print type(request.FILES['file']), len(request.FILES['file']),dir(request.FILES['file'])
		handle_upload_file(request.FILES['file'], str(request.FILES['file']))
		return HttpResponse('success')

def handle_upload_file(file, name):
	path = '/home/upload/'
	if not os.path.exists(path):
		os.mkdir(path)
	with open(os.path.join(path, name), 'wb+') as destination:
		for chunk in file.chunks():
			print(len(chunk))
			destination.write(chunk)



def download(request, file):
	root_download_path = '/home/download/'
	request_download_path = request.path.replace('/download/','')
	download_path = os.path.join(root_download_path, request_download_path)
	if os.path.exists(download_path):
		if os.path.isdir(download_path):
			dir_list = [ (os.path.join(request_download_path, name), name) for name in os.listdir(download_path) if os.path.isdir(os.path.join(download_path,name)) ]
			file_list = [ (os.path.join(request_download_path, name), name, os.path.getsize(download_path)) for name in os.listdir(download_path) if os.path.isfile(os.path.join(download_path,name)) ]
			return render(request, 'blogapp/download_page.html', {'dir_list':dir_list,'file_list':file_list})
		else:
			response = StreamingHttpResponse(readFile(download_path))
			response['Content-Type'] = 'multipart/form-data'
			response['Content-Disposition'] ='attachment;filename="{0}"'.format(file)
			return response

	else:
		raise Http404('file not exist')

def readFile(filename, chunk_size=512):
	with open(filename, 'rb') as f:
		while True:
			c = f.read(chunk_size)
			print(len(c))
			if c:
				yield c
			else:
				break



def login(request):
	if request.method == 'POST':
		form = forms.Userlogin(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			passwd = form.cleaned_data['passwd']
			user = authenticate(username=username, password=passwd)
			print(type(user))
			userinfo = forms.Userlogin()
			if user:
				# if request.session.has_key('IS_LOGIN'):
				if request.session.has_key('username'):
					if request.session['username'] == username:
						context = {'tips':"用户已经登录，请勿重复登录"}
						return render(request, 'blogapp/login.html', {'userinfo':userinfo,'context':context})
				request.session['username'] = username
				auth.login(request, user)
				return HttpResponseRedirect(reverse('blog:homepage'))
				# else:
				# 	request.session['IS_LOGIN'] = True
				# 	request.session['username'] = username
				# 	auth.login(request, user)
				# 	return HttpResponseRedirect(reverse('blog:homepage'))
			else:
				context = {'isLogin':False,'passwd':False,'tips':"用户不存在或密码错误"}
				return render(request, 'blogapp/login.html', {'userinfo':userinfo,'context':context})
		else:
			userinfo = forms.Userlogin()
			errors =  form.errors
			context = {'isLogin':False,'passwd':False}
			return render(request, 'blogapp/login.html', {'errors':errors, 'userinfo':userinfo})
	else:
		userinfo = forms.Userlogin()
		# print(userinfo)
		return render(request,'blogapp/login.html',{'userinfo':userinfo})

def register(request):
	context = {}
	if request.method == "POST":
		form = forms.UserReg(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			passwd = form.cleaned_data['passwd']
			# user = auth.authenticate(username=username, password=passwd)
			# if user:
			if User.objects.filter(username=username):
				context['msg'] = '用户名存在'
				context['userinfo'] = forms.UserReg()
				return render(request, 'blogapp/register.html', context)
			user = User.objects.create_user(username=username, password=passwd)
			user.save()
			auth.login(request, user)
			return HttpResponseRedirect(reverse('blog:homepage'))
	else:
		# context = {'isLogin':False}
		userinfo = forms.UserReg()
		# print(userinfo)
		return render(request, 'blogapp/register.html', {'userinfo':userinfo})

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect(reverse('blog:homepage'))

@login_required()
def chatroom(Request):
	username = Request.user.username
	return render(Request, 'blogapp/chatroom.html',{'username':username})