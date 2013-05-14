## Standard library imports (pure Python)
pass

## Related third party imports (Django and other 3rd party)
from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api #@UnresolvedImport

## Local application/library specific imports
from assignment.account_lead.tastypie_api import AccountLeadResource,\
    MailingListResource

v1_api = Api(api_name='v1')
v1_api.register(AccountLeadResource())
v1_api.register(MailingListResource())

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'assignment.views.home', name='home'),
    # url(r'^assignment/', include('assignment.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^api/', include(v1_api.urls)),
    
    url(r'^search/', include('haystack.urls')),
)
