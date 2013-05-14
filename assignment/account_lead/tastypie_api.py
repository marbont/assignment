## Standard library imports (pure Python)
pass

## Related third party imports (Django and other 3rd party)
from django.contrib.auth.models import User
from django.db import models
from tastypie import fields #@UnresolvedImport
from tastypie.authentication import ApiKeyAuthentication #@UnresolvedImport
from tastypie.models import create_api_key #@UnresolvedImport
from tastypie.resources import ModelResource #@UnresolvedImport

## Local application/library specific imports
from assignment.account_lead.models import AccountLead, MailingList
'''
This module maps the db models to the resource models.
The resource models mapped are available through the API endpoint.
'''

class MailingListResource(ModelResource):
    
    class Meta:
        queryset = MailingList.objects.all()
        resource_name = 'mailing_list'
        allowed_methods = ['get']
        authentication = ApiKeyAuthentication()

class AccountLeadResource(ModelResource):
    mailing_list = fields.ForeignKey(MailingListResource, 'mailing_list')
    
    class Meta:
        queryset = AccountLead.objects.all()
        resource_name = 'account_lead'
        excludes = ['id']
        allowed_methods = ['post', 'get', 'put', 'delete']
        authentication = ApiKeyAuthentication()

# Auto register      
models.signals.post_save.connect(create_api_key, sender=User)


