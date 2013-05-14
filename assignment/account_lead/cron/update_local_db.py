############# DO NOT TOUCH! sets up execution environment ####
import os
import sys
from os.path import abspath, dirname, join
from django.core import management

sys.path.insert(0, abspath(join(dirname(__file__), "../../../")))
os.environ['DJANGO_SETTINGS_MODULE'] ='assignment.settings'
##############################################################

if __name__ == "__main__":
    # Updating the RSS feeds caching files
    management.call_command('update_local_db', verbosity=0, intercative=False)
