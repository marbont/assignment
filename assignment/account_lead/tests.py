from django.conf import settings
from django.test import TestCase
from assignment.account_lead.models import MailingList, AccountLead
from assignment.account_lead.utils.date_converter import to_python_date_format
from assignment.account_lead.exceptions import TBDBException


class AccountLeadCreationTest(TestCase):
    
    def setUp(self):
        self.init()
        
    def init(self):
        birth_date = to_python_date_format("2010-08-31T10:12:25")
        mailing_list = MailingList.objects.get(number=3)
        self.defaults={'mailing_list' : mailing_list,
                       'birth_date' : birth_date,
                       'city' : 'Amsterdam',
                       'country' : 'nl',
                       'first_name' : 'Jack',
                       'gender' : 'm',
                       'last_name' : 'Williams',
                       'lead' : True,
                       'tr_referral': settings.TR_REFERRAL}
        self.account, _ = AccountLead.objects.get_or_create(email="simple_test@example.com", defaults=self.defaults)
    
    def test_normal_sync(self):
        """
        Tests that inserting a new correct account from the admin raise no error
        """
        self.account.save(admin_call='admin')
        self.assertIsNotNone(self.account.resource_uri)
        
    def test_already_exists(self):
        """
        Tests that inserting (from the admin) a non existing account in the local DB, 
        but already existing in the remote DB raise errors
        """
        existing_account, _ = AccountLead.objects.get_or_create(email="test@example.com", defaults=self.defaults)
        def save():
            existing_account.save(admin_call='admin')
        try:
            save()
        except:
            pass
        self.assertRaises(TBDBException, save)
        
    
    def tearDown(self):
        self.account.delete(admin_call='admin')
