import pycricket
from django.conf import settings

if settings.USE_CA_FILECACHE:
  ca_cache = pycricket.FileStorageHandler(settings.BASE_DIR+"/") 
else:
  ca_cache = pycricket.CricketApiStorageHandler()

CRICKET_API = pycricket.CricketApiApp(settings.CA_ACCESS_KEY, \
              settings.CA_SECRET_KEY, \
              settings.CA_APP_ID, \
              ca_cache,
              settings.CA_DEVICE_ID
            )



