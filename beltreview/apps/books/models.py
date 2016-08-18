from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import bcrypt, re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
	def validateReg(self, request):
		errors = self.validate_inputs(request)
		if len(errors) > 0:
			return (False, errors)
		pw_hash = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt())
		user = self.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password=pw_hash)
		return (True, user)

	def validateLogin(self, request):
		try:
			user = User.objects.get(email=request.POST['email'])
			password = request.POST['password'].encode()
			if bcrypt.hashpw(password, user.password.encode()):
				return (True, user)
		except ObjectDoesNotExist:
			pass
		return (False, ["Email/password don't match."])

	def validate_inputs(self, request):
		errors = []
		if len(request.POST['name']) < 2 or len(request.POST['alias']) < 2:
			errors.append("Please include a first and/or ALIAS name longer than two characters.")
		if not EMAIL_REGEX.match(request.POST['email']):
			errors.append("Please include a valid email.")
		if len(request.POST['password']) < 8 or request.POST['password'] != request.POST['confirm_pw']:
			errors.append("Passwords must match and be at least 8 characters.")
		return errors
	

class BookManager(models.Manager):
	def add(self, title, select_author, add_author, review, stars, id):
		if select_author == '':
			if add_author == '':
				return (False)
			else:
				author=add_author
		else:
			author=select_author
		if title == '' or review == '' or stars == '':
			return (False)
		else:
			Book.objects.create(title=title, author=author)
			book_id = Book.objects.get(title=title, author=author)
			user_id = User.objects.get(id=id)
			Review.objects.create(review=review,rating=stars, book_id=book_id, user_id=user_id)
			return (True)
		

class ReviewManager(models.Manager):	
	def addrev(self, review, stars, bid, id):
		if review == '' or stars == '':
				return (False)
		else:
			user_id = User.objects.get(id=id)
			book_id = Book.objects.get(id=bid)
			Review.objects.create(review=review,rating=stars, book_id=book_id, user_id=user_id)
			return (True)

	def remreview(self, rid):
		Review.objects.get(id=rid).delete()
class User(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class Book(models.Model):
	title = models.CharField(max_length=1000)
	author = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = BookManager()

class Review(models.Model):
	review = models.TextField(max_length=1000)
	rating = models.IntegerField(max_length=1)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	user_id = models.ForeignKey(User)
	book_id = models.ForeignKey(Book)
	objects = ReviewManager()