from google.appengine.ext import db

class LoginDataModel(db.Model):
    
    id = db.StringProperty()
    password = db.StringProperty()

class AdminModel(db.Model):
    
    id = db.StringProperty()
    password = db.StringProperty()

class BlogPostModel(db.Model):
    
    title = db.StringProperty()
    content = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)

class PageModel(db.Model):
    
    title = db.StringProperty()
    content = db.TextProperty()
    updated = db.DateTimeProperty(auto_now=True)
    created = db.DateTimeProperty(auto_now=True)