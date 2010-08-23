#!/usr/bin/env python
#
#    Copyright (C) 2010 Joerund Nydal
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import wsgiref.handlers
import logging, os, re
import random, string, cgi

from google.appengine.ext.webapp import template
from appengine_utilities import sessions
from google.appengine.ext import webapp
from google.appengine.ext import db
from django.core.paginator import ObjectPaginator
from django.utils import simplejson

from utils import authenticatedUser
from utils import menuLinks
from utils import validateLoginModel

from models import BlogPostModel
from models import LoginDataModel

from page import PageViewHandler
from page import PageDeleteHandler
from page import PageEditHandler
from page import PageNewHandler
from page import PageJsonHandler

from google.appengine.ext.db.djangoforms import DateTimeProperty


class NewsViewHandler(webapp.RequestHandler):
    def get(self):
        
        page = int(self.request.get('page', '0')) 
        
        paginator = ObjectPaginator(db.GqlQuery('SELECT * FROM BlogPostModel ORDER BY created DESC'),10)
        
        blogposts = paginator.get_page(page)
        
        nextPageNumber = 0
        prevPageNumber = 0
        
        if paginator.has_next_page(page):
            nextPageNumber = str(page+1)
        
        if paginator.has_previous_page(page):
            prevPageNumber = str(page-1)
        
        template_values = {
            'menulinks':menuLinks(),
            'blogposts': blogposts,
            'user': authenticatedUser(sessions.Session()),
            'nextPageNumber': nextPageNumber,
            'prevPageNumber': prevPageNumber,
        }

        path = os.path.join(os.path.dirname(__file__), 'news.html')
        self.response.out.write(template.render(path, template_values))

class NewsJsonHandler(webapp.RequestHandler):
    def get(self,page):
        
        #rpc = db.create_rpc(deadline=10, read_policy=db.EVENTUAL_CONSISTENCY)
        
        paginator = ObjectPaginator(db.GqlQuery('SELECT * FROM BlogPostModel ORDER BY created DESC'),10)
        
        try:
            blogposts = paginator.get_page(page)
            self.response.out.write(simplejson.dumps([p.to_dict() for p in blogposts]))
        
        except:
            self.error(404)

class PostNewHandler(webapp.RequestHandler):
    def post(self):
   
        if authenticatedUser(sessions.Session()):

            blogpost = BlogPostModel(
                title = self.request.get('title'),
                content = self.request.get('content'))
            
            blogpost.put();
            
            self.redirect('/')
            
        else:
            
            self.redirect('/login/')
        
    def get(self):

        user = authenticatedUser(sessions.Session())

        template_values = {
            'menulinks': menuLinks(),
            'user': user,             
        }

        path = os.path.join(os.path.dirname(__file__), 'newPost.html')
        self.response.out.write(template.render(path, template_values))

class PostEditHandler(webapp.RequestHandler):
    def post(self,id):
   
        if authenticatedUser(sessions.Session()):

            blogpost = BlogPostModel.get_by_id(int(id), parent=None)
            blogpost.title = self.request.get('title')
            blogpost.content = self.request.get('content')
            blogpost.updated = DateTimeProperty.now()
            blogpost.put()
            
            self.redirect('/')
            
        else:
            
            self.redirect('/login/')
        
    def get(self,id):

        user = authenticatedUser(sessions.Session())
        blogpost = BlogPostModel.get_by_id(int(id), parent=None)

        template_values = {
            'menulinks': menuLinks(),
            'user': user,
            'post': blogpost,          
        }

        path = os.path.join(os.path.dirname(__file__), 'editPost.html')
        self.response.out.write(template.render(path, template_values))

class PostDeleteHandler(webapp.RequestHandler):       
    def get(self,id):

        blogpost = BlogPostModel.get_by_id(int(id), parent=None)
        db.delete(blogpost)

        self.redirect('/')

class Error404(webapp.RequestHandler):
    def get(self,garbage):
        
        user = authenticatedUser(sessions.Session())

        template_values = {  
            'menulinks': menuLinks(),
            'user': user,
            'garbage': garbage,          
        }
        
        self.error(404)
        path = os.path.join(os.path.dirname(__file__), '404.html')
        self.response.out.write(template.render(path, template_values))

class Login(webapp.RequestHandler):
    def post(self):
        
        loginModel = LoginDataModel(id = cgi.escape(self.request.get('user')),password = cgi.escape(self.request.get('password')))
        
        validLogin = validateLoginModel(loginModel)
        
        if validLogin == "true":
            
            self.sess = sessions.Session()
            self.sess["LOGIN_DATA"] = loginModel
            self.redirect('/')

        else:
            self.redirect('/login/?failed_login=1')
        
    def get(self):

        failedLogin = cgi.escape(self.request.get('failed_login'))

        template_values = {
            'menulinks': menuLinks(),
            'failedLoginValue': failedLogin,
        }

        path = os.path.join(os.path.dirname(__file__), 'login.html')
        self.response.out.write(template.render(path, template_values))

class Logout(webapp.RequestHandler):       
    def get(self):

        sessions.Session().delete()

        self.redirect('/')

def main():
    
    application = webapp.WSGIApplication([('/', NewsViewHandler),
                                          ('/rest/news/(\d*)/', NewsJsonHandler),
                                          ('/login/', Login),
                                          ('/logout/', Logout),
                                          ('/new/post/',PostNewHandler),
                                          ('/edit/post/(\d*)/',PostEditHandler),
                                          ('/delete/post/(\d*)/',PostDeleteHandler),
                                          ('/new/page/',PageNewHandler),
                                          ('/edit/page/(.*)/',PageEditHandler),
                                          ('/delete/page/(.*)/', PageDeleteHandler),
                                          ('/rest/page/(.*)/', PageJsonHandler),
                                          ('/(.*)/', PageViewHandler),
                                          ('/(.*)', Error404),
                                          ],
                                         debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()
    
