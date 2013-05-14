## Standard library imports (pure Python)
pass

## Related third party imports (Django and other 3rd party)
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

## Local application/library specific imports
from assignment.account_lead.api import tb_proxy
from assignment.account_lead.exceptions import TBDBException

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

class MailingList(models.Model):
    number = IntegerRangeField(_("Number"), blank=False, default=1, help_text=_("A number in the range (1,5)"), max_value=5, min_value=1, null=False, unique=True)
    name = models.CharField(_("Name"), blank=True, default="", max_length=30, null=False, unique=False)
    
    def __unicode__(self):
        return u'%s - %s' % (self.number, self.name)

class AccountLead(models.Model):
    GENDER_CHOICES = (
                  ('m', _('Male')),
                  ('f', _('Female')),
    )
    
    birth_date = models.DateTimeField(_("Birth date"), blank=True, null=True, unique=False)
    city = models.CharField(_("City"), blank=True, default="", max_length=30, null=False, unique=False)
    country = models.CharField(_("Country"), blank=False, default="nl", max_length=30, null=False, unique=False)
    email = models.CharField(_("Email"), blank=False, default="", max_length=30, null=False, unique=True)
    first_name = models.CharField(_("First Name"), blank=True, default="", max_length=30, null=False, unique=False)
    gender = models.CharField(_("Gender"), blank=True, choices=GENDER_CHOICES, default="", max_length=1, null=False, unique=False)
    last_name = models.CharField(_("Last Name"), blank=True, default="", max_length=30, null=False, unique=False)
    lead = models.BooleanField(_("Lead"), blank=False, default=True, null=False, unique=False)
    mailing_list = models.ForeignKey(MailingList, verbose_name=_('Mailing List'), blank=False, null=False)
    phone = models.CharField(_("Phone"), blank=True, default="", max_length=30, null=False, unique=False)
    resource_uri = models.CharField(_("Resource Uri"), blank=True, max_length=30, null=False, unique=False)
    street_number = models.CharField(_("Street Number"), blank=True, default="", max_length=30, null=False, unique=False)
    tr_input_method = models.CharField(_("Input method"), blank=True, default="", max_length=30, null=False, unique=False)
    tr_ip_address = models.CharField(_("Ip address"), default=settings.IP_ADDRESS, blank=False, max_length=30, null=True, unique=False)
    tr_language = models.CharField(_("Language"), blank=True, default="", max_length=30, null=False, unique=False)
    tr_referral = models.CharField(_("Referral"), default="mbontempi", blank=False, max_length=30, null=False, unique=False)
    utm_campaign = models.CharField(_("Campaign"), blank=True, default="", max_length=30, null=False, unique=False)
    utm_medium = models.CharField(_("Medium"), blank=True, default="", max_length=30, null=False, unique=False)
    utm_source = models.CharField(_("Source"), blank=True, default="", max_length=30, null=False, unique=False)
    zipcode = models.CharField(_("Zipcode"), blank=True, default="", max_length=30, null=False, unique=False)
    #tb_synchronized = models.BooleanField(_("Syncrhonized with Remote DB"), blank=False, default=True, null=False, unique=False)
    
    def __unicode__(self):
        return u'Account with email %s' % self.email
    
    def delete(self, *args, **kwargs):
        '''
        Ovveride the default delete function. 
        If the function is called by the admin panel, then we try to delete the remote resource first.
        If it's successful or if the remote resource doesn't exist, we delete the local one.
        Else, if there's some other error we don't delete the local resource and launch an exception.
        
        If this function is not called from the admin panel, 
        then the original delete function is called.
        
        @author: Marco B.
        '''
        called_by_admin = kwargs.get('admin_call', None)
        if called_by_admin:
            kwargs.pop('admin_call')
            if not self.resource_uri:
                super(AccountLead, self).delete(*args, **kwargs)
            else:
                response = tb_proxy.delete(self)
                if response == tb_proxy.STATUS_OK or response == tb_proxy.STATUS_DOES_NOT_EXISTS:
                    super(AccountLead, self).delete(*args, **kwargs)
                else:
                    raise TBDBException(_("Cannot delete this Account now. Try later!"))
        else:
            super(AccountLead, self).delete(*args, **kwargs)
        
        
    def save(self, *args, **kwargs):
        '''
        Ovveride the default save. 
        If this function is called by the admin panel, then we try to save the remote resource first.
        If it's successful we save the local one too.
        Else, if the account already exists, we raise the proper exception.
        Else, if there's some other error we raise a generic exception.
        
        If this function is not called from the admin panel, 
        then the original save function is called.
        
        @author: Marco B.
        '''
        called_by_admin = kwargs.get('admin_call', None)
        if called_by_admin:
            kwargs.pop('admin_call')
            response_status = tb_proxy.save(self)
            if response_status == tb_proxy.STATUS_OK:
                super(AccountLead, self).save(*args, **kwargs)
            elif response_status == tb_proxy.STATUS_ALREADY_EXISTS:
                raise TBDBException(_("This account already exists, and cannot be modified!"))
            else:
                raise TBDBException(_("This account cannot be saved now. Try again later!"))
        else:
            super(AccountLead, self).save(*args, **kwargs)
            
    def get_admin_url(self):
        return reverse('admin:%s_%s_change' % ('account_lead', 'accountlead'), args=(self.pk,))

    
