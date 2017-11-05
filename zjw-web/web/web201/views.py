# -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Article
from django.core.paginator import Paginator

def home(request):
	return render(request,'index.html')
	
def introduction(request):
	return render(request,'introduction.html')
	
def teachers(request,name):
	if name=='li':
		return render(request,'teachers-li.html')
	if name=='wang':
		return render(request,'teachers-wang.html')

def students(request):
	return render(request,'students.html')

def news(request,type):
	articles = Article.objects.all().filter(category__name = type).order_by('-time')
	p = Paginator(articles,10)
	if p.num_pages <= 1:
		article_list = articles
		data = ''
	else:
		page = int(request.GET.get('page',1))
		article_list = p.page(page)
		left = []
		right = []
		left_has_more = False
		right_has_more = False
		first = False
		last = False
		total_pages = p.num_pages
		page_range = p.page_range
		if page == 1:
			right = page_range[page:page+2]
			if right[-1] < total_pages - 1:
				right_has_more = True
			if right[-1] < total_pages:
				last = True
		elif page == total_pages:
			left = page_range[(page-3) if (page-3) > 0 else 0:page-1]
			if left[0] > 2:
				left_has_more = True
			if left[0] > 1:
				first = True
		else:
			left = page_range[(page-3) if (page-3) > 0 else 0:page-1]
			right = page_range[page:page+2]
			if left[0] > 2:
				left_has_more = True
			if left[0] > 1:
				first = True
			if right[-1] < total_pages - 1:
				right_has_more = True
			if right[-1] < total_pages:
				last = True
		data = {
			'left':left,
			'right':right,
			'left_has_more':left_has_more,
			'right_has_more':right_has_more,
			'first':first,
			'last':last,
			'total_pages':total_pages,
			'page':page
		}
	return render(request,'news.html',context={
		'article_list':article_list,'data':data
	})

def contact(request):
	return render(request,'contact.html')

def detail(request,type,pk):
	post=get_object_or_404(Article,pk=pk)
	post.increase_views()
	article_list=Article.objects.all().filter(category__name = type).order_by('-time')
	index_list=[]
	for i in range(len(article_list)):
			index_list.append(article_list[i].pk)
	index = index_list.index(int(pk))
	if index <= 0:
		pre=-1
		next = index_list[index+1]
	elif index >= len(index_list)-1:
		next=-1
		pre = index_list[index-1]
	else:
		pre = index_list[index-1]
		next = index_list[index+1]
	if pre == -1:
		pre_title = '这是第一篇新闻了'
	else:
		pre_title=Article.objects.get(id__exact=pre).title
	if next == -1:
		next_title='这是最后一篇新闻了'
	else:
		next_title=Article.objects.get(id__exact=next).title
	return render(request,'content.html',context={'post':post,'pre':pre,'next':next,'pre_title':pre_title,'next_title':next_title})