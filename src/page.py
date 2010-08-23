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
from models import PageModel
from models import BlogPostModel
from models import AdminModel
from utils import authenticatedUser
from utils import menuLinks
from utils import validateLoginModel
from google.appengine.ext.db.djangoforms import DateTimeProperty

class PageViewHandler(webapp.RequestHandler):
    def get(self,key_name):
            
        page = PageModel.get_by_key_name(key_name, parent=None)

        user = authenticatedUser(sessions.Session())

        template_values = {
            'menulinks': menuLinks(),
            'page': page,
            'user': user,
            'key_name': key_name,
        }

        if (page):
            path = os.path.join(os.path.dirname(__file__), 'page.html')
            self.response.out.write(template.render(path, template_values))

        else:
            self.error(404)#('/'+key_name[:len(key_name)])
            path = os.path.join(os.path.dirname(__file__), '404.html')
            self.response.out.write(template.render(path, template_values))

class PageJsonHandler(webapp.RequestHandler):
    def get(self,key_name):
        
        page = PageModel.get_by_key_name(key_name, parent=None)
        self.response.out.write(simplejson.dumps([page.to_dict()]))

class PageNewHandler(webapp.RequestHandler):
    def post(self):
        
        if authenticatedUser(sessions.Session()):

            page = PageModel(
                key_name = self.request.get('title').replace(' ','_'),
                title = self.request.get('title'),
                content = self.request.get('content'))
            
            page.put();

            self.redirect('/'+self.request.get('title').replace(' ','_')+'/')
            
        else:
            
            self.redirect('/login/')
        
    def get(self):
        
        user = authenticatedUser(sessions.Session())

        template_values = {  
            'menulinks': menuLinks(),
            'user': user,          
        }
        
        path = os.path.join(os.path.dirname(__file__), 'newPage.html')
        self.response.out.write(template.render(path, template_values))

class PageEditHandler(webapp.RequestHandler):
    def post(self,key_name):
   
        if authenticatedUser(sessions.Session()):

            page = PageModel.get_by_key_name(key_name,parent=None)
            page.key_name = self.request.get('title').replace(' ','_')
            page.title = self.request.get('title')
            page.updated = DateTimeProperty.now()
            page.content = self.request.get('content')
            page.put();
            
            self.redirect('/')
            
        else:
            
            self.redirect('/login/')
        
    def get(self, key_name):

        user = authenticatedUser(sessions.Session())
        page = PageModel.get_by_key_name(key_name,parent=None)

        template_values = {
            'menulinks': menuLinks(),
            'user': user,
            'page': page,          
        }

        path = os.path.join(os.path.dirname(__file__), 'editPage.html')
        self.response.out.write(template.render(path, template_values))

class PageDeleteHandler(webapp.RequestHandler):       
    def get(self, key_name):

        page = PageModel.get_by_key_name(key_name, parent=None)
        db.delete(page)

        self.redirect('/')

