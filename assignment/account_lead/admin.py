## Standard library imports (pure Python)
pass

## Related third party imports (Django and other 3rd party)
from django.contrib import admin, messages

## Local application/library specific imports
from assignment.account_lead.models import AccountLead, MailingList
from assignment.account_lead.exceptions import TBDBException

class AccountLeadAdmin(admin.ModelAdmin):
    actions=['custom_delete_selected']
    
    def get_actions(self, request):
        actions = super(AccountLeadAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions
    
    fields = ('email',
              'mailing_list',
              'tr_ip_address',
              'tr_referral', 
              'lead', 
              'birth_date',
              ('first_name', 'last_name'),
              'gender',
              'tr_language',
              ('country', 'city', 'street_number', 'zipcode'),
              'phone',
              'utm_campaign',
              'utm_medium',
              'utm_source'
              )
    
    list_display = ('email',
                    'mailing_list',
                    'tr_ip_address',
                    'tr_referral',
                    'resource_uri',)
    
    def save_model(self, request, obj, form, change):
        '''
        Since the override save function of AccountLead 
        can raise custom exceptions, we catch and convert
        them in error messages for the user.
        The function delete() is called passing the arg admin_call, 
        so the action is reflected to the remote DB.
        '''
        try:
            obj.save(admin_call='admin')
        except TBDBException as e:
            messages.set_level(request, messages.WARNING)
            messages.error(request, e.msg)
    
    def custom_delete_selected(self, request, queryset):
        '''
        Need to override the default delete action, because it
        doesn't really call the obj.delete() function.
        The function delete() is called passing the arg admin_call, 
        so the action is reflected to the remote DB.
        Also, since the override delete function of AccountLead
        can raise custom exceptions, we catch and convert them
        in error messages for the user.
        '''
        for obj in queryset:
            try:
                obj.delete(admin_call='admin')
            except TBDBException as e:
                messages.set_level(request, messages.WARNING)
                messages.error(request, e.msg)
            
        if queryset.count() == 1:
            message_bit = "1 account lead entry was"
        else:
            message_bit = "%s account lead entries were" % queryset.count()
        self.message_user(request,"%s successfully deleted." % message_bit)
    custom_delete_selected.short_description = "Delete selected account leads"
        
    
    

admin.site.register(AccountLead, AccountLeadAdmin)
admin.site.register(MailingList)
