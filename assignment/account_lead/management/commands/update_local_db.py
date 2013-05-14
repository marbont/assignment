## Standard library imports (pure Python)
pass
        
## Related third party imports (Django and other 3rd party)
from django.core.management.base import BaseCommand
    
## Local application/library specific imports
from assignment.account_lead.api import updater
    

class Command(BaseCommand):
    '''
    This command synchronize the remote DB (using REST) with the local DB.
    '''
    
    def handle(self, *args, **options ):
        updater.global_update()