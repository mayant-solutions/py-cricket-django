import pycricket
from django.conf import settings

if settings.USE_RCA_FILECACHE:
  ca_cache = pycricket.RcaFileStorageHandler(settings.BASE_DIR+"/") 
else:
  ca_cache = pycricket.RcaStorageHandler()

CRICKET_API = pycricket.RcaApp(settings.CA_ACCESS_KEY, \
              settings.CA_SECRET_KEY, \
              settings.CA_APP_ID, \
              ca_cache,
              settings.CA_DEVICE_ID
            )



