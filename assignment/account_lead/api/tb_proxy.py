## Standard library imports (pure Python)
import json #@UnresolvedImport

## Related third party imports (Django and other 3rd party)
from django.conf import settings
import requests #@UnresolvedImport

## Local application/library specific imports
from assignment.account_lead.utils.date_converter import to_tb_date_format


### STATUS CODES ###
STATUS_OK = 1
STATUS_ALREADY_EXISTS = 2
STATUS_ERROR = 3
STATUS_DOES_NOT_EXISTS = 4
####################

def delete(account_lead):
    url = '%s?%s'  % (account_lead.resource_uri, settings.CREDENTIALS_AS_PARAMS)
    headers = {"Content-Type": "application/json"}
    r = requests.delete(url, headers=headers)
    print r.status_code
    print r.headers
    print r.text
    if r.status_code == 204:
        return STATUS_OK
    elif r.status_code == 410 or r.status_code == 404:
        return STATUS_DOES_NOT_EXISTS
    else:
        return STATUS_ERROR


def save(account_lead):
    if account_lead.resource_uri:
        # Exit now, so we don't hit remote DB
        return STATUS_ALREADY_EXISTS
    url = '%s%s/?%s' % (settings.DB_URL, 'account_lead', settings.CREDENTIALS_AS_PARAMS)
    headers = {"Content-Type": "application/json"}
    payload = {### Mandatory fields ###
               "email" : account_lead.email, 
               "mailing_lists" : account_lead.mailing_list.number,
               "ip_address" : account_lead.tr_ip_address,
               "tr_referral" : account_lead.tr_referral,
               ### End mandatory fields ###
               "birth_date" : to_tb_date_format(account_lead.birth_date),
               "city" : account_lead.city or "",
               "country" : account_lead.country or "",
               "first_name" : account_lead.first_name or "",
               "last_name" : account_lead.last_name or "",
               "lead" : account_lead.lead,
               "phone" : account_lead.phone or "",
               "street_number" : account_lead.street_number or "",
               "tr_language" : account_lead.tr_language or "",
               "utm_campaign" : account_lead.utm_campaign or "",
               "utm_source" : account_lead.utm_source or "",
               "zipcode" : account_lead.zipcode or ""}
    if account_lead.gender:
        payload["gender"] = account_lead.gender
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print payload
    print r.status_code
    print r.headers
    print r.text
    if r.status_code == 201:
        location = r.headers.get('location', None)
        if location:
            account_lead.resource_uri = location
        return STATUS_OK
    elif r.status_code == 409:
        return STATUS_ALREADY_EXISTS
    else:
        return STATUS_ERROR


