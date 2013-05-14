## Standard library imports (pure Python)
pass

## Related third party imports (Django and other 3rd party)
from dateutil.parser import parse #@UnresolvedImport

## Local application/library specific imports
pass

def to_tb_date_format(date):
    ''' 
    This function takes a datetime object and returns 
    a timestamp string in the format "yyyy-mm-ddThh:mm:ss"
    E.g. : 2010-11-10T03:07:43
    
    @author: Marco B.
    '''
    if not date:
        return None
    return '%s-%s-%sT%s:%s:%s' % (date.year, "%02d" % date.month, 
                              "%02d" % date.day, "%02d" % date.hour, 
                              "%02d" % date.minute, "%02d" % date.second)

def to_python_date_format(tb_date):
    ''' 
    This function takes a timestamp string in this format:
    yyyymmddThhmmss
    and returns a datetime object
    
    @author: Marco B.
    '''
    if not tb_date:
        return None
    return parse(tb_date)
