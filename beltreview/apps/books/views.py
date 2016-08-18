from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from models import User, Book, Review

# Create your views here.
def index(request):
	return render(request, 'books/index.html')

def register(request):
	result = User.objects.validateReg(request)
	if result[0] == False:
		print_messages(request, result[1])
		return redirect(reverse ('index'))
	return log_user_in(request, result[1])
	return redirect('/bookhome')	

def login(request):
	result = User.objects.validateLogin(request)
	if result[0] == False:
		print_messages(request, result[1])
		return redirect(reverse ('index'))
	return log_user_in(request, result[1])
	request.session['name'] = request.POST['name']
	return redirect('/bookhome')

def print_messages(request, message_list):
	for message in message_list:
		messages.add_message(request, messages.INFO, message)

def log_user_in(request, user):
	userobject = User.objects.get(email=user.email)
	userid = userobject.id
	request.session['user'] = {
		'id' : userid,
		'alias' : user.alias,
	}
	return redirect('/bookhome')

def addbook(request):
	books = Book.objects.all()
	return render(request,'books/add.html', context={'books':books})

def add(request):
	id = request.session['user']
	uid = id['id']
	print uid
	Book.objects.add(request.POST['title'], request.POST['select_author'], request.POST['add_author'], request.POST['review'], request.POST['rating'], uid)
	return redirect("/bookhome")	

def logout(request):
	request.session.pop('user')
	return redirect(reverse('index'))	

def bookhome(request):
	books = Book.objects.all()
	reviews = Review.objects.all().order_by('-created_at')[:3]
	users = User.objects.all()
	return render(request, 'books/bookhome.html', context={'books':books, 'reviews':reviews, 'users':users})

def user(request, id):
	users = User.objects.get(id=id)
	userreviews = Review.objects.filter(user_id=id)
	books = Book.objects.all()
	reviews = Review.objects.all()
	count = 0
	for x in userreviews:
		count += 1
	return render(request, 'books/user.html', context={'users':users, 'count':count, 'books':books, 'reviews':reviews})

def bookreview(request, id):
	books = Book.objects.get(id=id)
	reviews = Review.objects.filter(book_id=books).order_by('-created_at')[:3]
	users = User.objects.all()
	return render(request, 'books/bookreview.html', context={'books':books, 'reviews':reviews, 'users':users})

def addreview(request, id):
	userid = request.session['user']
	uid = userid['id']
	Review.objects.addrev(request.POST['review'], request.POST['rating'], id, uid)
	return redirect('/bookreview/'+str(id))

def remreview(request, rid, bid):
	Review.objects.remreview(rid)
	return redirect('/bookreview/'+str(bid))
