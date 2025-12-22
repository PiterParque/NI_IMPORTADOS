import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("Site.settings")

application = get_wsgi_application()
