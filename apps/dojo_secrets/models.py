from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
  def login(self, postData):
    errors = []
    if User.objects.filter(eml=postData['eml']).first():
        user_pw = User.objects.get(eml=postData['eml']).pw
        if user_pw != bcrypt.hashpw(postData['pw'].encode('utf8'), user_pw.encode('utf8')):
            errors.append('Password is incorret!')
            return [False, errors]
        else:
            user_id = User.objects.get(eml=postData['eml']).id
            return [True, user_id] 
    else:
        errors.append('User does not exist!')
        return [False, errors]

  def register(self, postData):
    errors = []
    if len(postData['f_n']) == 0:
        errors.append('First name cannot be empty!')
    if len(postData['l_n']) == 0:
        errors.append('Last name cannot be empty!')
    if not EMAIL_REGEX.match(postData['eml']):
        errors.append('Email address is invalid!')
    if len(postData['pw']) < 8:
        errors.append('Passord is too short!')
    if postData['pw'] != postData['c_pw']:
        errors.append('Please confirm password again!')
    if User.objects.filter(eml=postData['eml']).first() != None:
        errors.append('Email address is already registered!')
    if errors != []:
        return [False, errors]
    else:
        User.objects.create(f_n=postData['f_n'], l_n=postData['l_n'], eml=postData['eml'], pw=bcrypt.hashpw(postData['pw'].encode('utf8'), bcrypt.gensalt()))
        user_id = User.objects.get(eml=postData['eml']).id
        return [True, user_id] 

class SecretManager(models.Manager):
  def validate(self, content, user_id):
    info = []
    if len(content) < 4:
      info.append('Secret must be at least three characters long!')
      return (False, info)
    else:
      this_author = User.objects.get(id=user_id)
      Secret.objects.create(content=content, author=this_author)
      return (True, info)
  def like(self, secret_id, user_id):
    info = []
    this_secret = Secret.objects.get(id=secret_id)
    this_user = User.objects.get(id=user_id)
    if this_secret.author.id == user_id:
      info.append('Of course you like your own secret!')
      return (False, info)
    else:
      this_secret.likes.add(this_user)
      info.append('You liked a secret!')
      return (True, info)
  def delete(self, secret_id, user_id):
    info = []
    this_secret = Secret.objects.get(id=secret_id)
    this_user = User.objects.get(id=user_id)
    if this_secret.author.id != user_id:
      info.append("You can not delete other people's secret!")
      return (False, info)
    else:
      this_secret.delete()
      info.append('You deleted your secret!')
      return (True, info)

class User(models.Model):
  f_n = models.CharField(max_length=38)
  l_n = models.CharField(max_length=38)
  eml = models.CharField(max_length=38)
  pw = models.CharField(max_length=38)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UserManager()

class Secret(models.Model):
  content = models.TextField(max_length=255)
  author = models.ForeignKey(User, related_name="created_secrets")
  likes = models.ManyToManyField(User, related_name="liked_secrets")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = SecretManager()



