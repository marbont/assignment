## Standard library imports (pure Python)
pass

## Related third party imports (Django and other 3rd party)
from haystack import indexes, site #@UnresolvedImport

## Local application/library specific imports
from assignment.account_lead.models import AccountLead


class AccountLeadIndex(indexes.SearchIndex):
    '''
    Create a simple index for AccountLead model
    
    @author: Marco B.
    '''
    
    text = indexes.CharField(document=True, use_template=True)
    email = indexes.CharField(model_attr='email')
    
    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return AccountLead.objects.all()
    
site.register(AccountLead, AccountLeadIndex)
