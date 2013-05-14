# The BASE URL: do not put any / in the end of the string.
BASE_URL = 'http://api.example.com'

# The remote DB URL - DO NOT touch this variable
DB_URL = '%s/v1/' % BASE_URL

# The user credentials
CREDENTIALS = {'username' : '',
               'api_key'  : '',
               'format'   : 'json'}

# Credentials in get params
CREDENTIALS_AS_PARAMS = 'username=%s&api_key=%s&format=%s' % (CREDENTIALS['username'],
                                                              CREDENTIALS['api_key'],
                                                              CREDENTIALS['format'])
# Insert tr_referral here
TR_REFERRAL = ''

# Mailing list default value: can be a number from 1 to 5
MAILING_LISTS = 1

# Default IP address: a valid IP address
IP_ADDRESS = 'xxx.xxx.xxx.xxx'
