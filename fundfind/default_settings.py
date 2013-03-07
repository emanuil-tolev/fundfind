SECRET_KEY = 'default-key'
# override certain defaults of the Flask-Bootstrap extension
BOOTSTRAP_USE_MINIFIED = False # small performance gain not worth loss of debugging info yet
BOOTSTRAP_JQUERY_VERSION = '1.9.1' # most up-to-date that's tested with the app
BOOTSTRAP_USE_CDN = True # app is far more likely to go down that a Cloud Delivery Network
