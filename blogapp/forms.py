#coding:utf-8

from django import forms

class VoteTitle(forms.Form):

	# vote_title = forms.CharField(label="title",min_length=5, error_messages={"required":"必填",})
	vote_title = forms.ChoiceField(choices=[
		('title','tilte'),('标题1','标题1'),('标题2','title2') #元组第二个值为前端显示效果，第一个为后端实际存储
	])

class Userlogin(forms.Form):

	username = forms.CharField(label="用户名",required=True,min_length=1,max_length=10, widget=forms.TextInput(attrs=
																											{'placeholder':'用户名'}))
	passwd = forms.CharField(label="密码",required=True, min_length=1, max_length=10,widget=forms.TextInput(attrs={'placeholder':'密码'}))
	# passwd_check = forms.CharField(label="密码确认",required=True, min_length=1, max_length=10)

class UserReg(forms.Form):

	username = forms.CharField(label="用户名",required=True,min_length=1,max_length=10)
	passwd = forms.CharField(label="密码",required=True, min_length=1, max_length=10)
	passwd_check = forms.CharField(label="密码确认",required=True, min_length=1, max_length=10)

