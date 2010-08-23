import datetime
import time

from google.appengine.ext import db

class DictModel(db.Model):
    def to_dict(self):
        return dict([(p, unicode(getattr(self, p))) for p in self.properties()])

    #used in simplejson as this self.response.out.write(simplejson.dumps([p.to_dict() for p in photos]))

class LoginDataModel(DictModel):
    
    id = db.StringProperty()
    password = db.StringProperty()

class AdminModel(DictModel):
    
    id = db.StringProperty()
    password = db.StringProperty()

class BlogPostModel(DictModel):
    def to_dict(self):
        return dict({"id" : self.key().id() , "title" : unicode(self.title), "content" : unicode(self.content), "created" : unicode(self.created)})
    
    title = db.StringProperty()
    content = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)

class PageModel(DictModel):
    
    title = db.StringProperty()
    content = db.TextProperty()
    updated = db.DateTimeProperty(auto_now=True)
    created = db.DateTimeProperty(auto_now=True)

