## Standard library imports (pure Python)
pass

## Related third party imports (Django and other 3rd party)
from django.conf import settings
import requests #@UnresolvedImport

## Local application/library specific imports
from assignment.account_lead.models import AccountLead, MailingList
from assignment.account_lead.utils.date_converter import to_python_date_format


def _fill_db_from(dic):
    birth_date = to_python_date_format(dic.get('birth_date',None))
    mailing_list_nr = dic.get('mailing_lists')[0].get('resource_uri').split('/')[-2]
    mailing_list = MailingList.objects.get(number=mailing_list_nr)
    # Get or create the account
    account, _ = AccountLead.objects.get_or_create(email=dic.get('email'), defaults={'mailing_list' : mailing_list})
    ### Fill it with updated values
    account.birth_date=birth_date
    account.city = dic.get('city')
    account.country = dic.get('country')
    account.email = dic.get('email')
    account.first_name = dic.get('first_name')
    account.gender = dic.get('gender')
    account.last_name = dic.get('last_name')
    account.lead = dic.get('lead')
    account.mailing_list=mailing_list
    account.phone = dic.get('phone')
    account.resource_uri = '%s%s' %  (settings.BASE_URL, dic.get('resource_uri'))
    account.street_number = dic.get('street_number')
    account.tr_input_method = dic.get('tr_input_method')
    account.tr_ip_address= dic.get('tr_ip_address')
    account.tr_language = dic.get('tr_language')
    account.tr_referral = dic.get('tr_referral').get('name')
    account.utm_campaign = dic.get('utm_campaign')
    account.utm_medium = dic.get('utm_medium')
    account.utm_source = dic.get('utm_source')
    account.zipcode = dic.get('zipcode')
    account.save()
    

def _iterative_update(url=None):
    if not url:
        url = '%s%s/?%s' % (settings.DB_URL, 'account_lead', settings.CREDENTIALS_AS_PARAMS)
    headers = {"Content-Type": "application/json"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        dic = r.json()
        meta = dic.get('meta', None)
        next_page = None
        if meta:
            next_page = meta.get('next', None)
            objects = dic.get('objects', None)
        for i in range(len(objects)):
            _fill_db_from(objects[i])
        if next_page: # Call the same function till we read all 'pages'
            _iterative_update('%s%s' % (settings.BASE_URL, next_page))
        

def global_update():
    _iterative_update()
    
