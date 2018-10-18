# This is not a good practice and is used for the presentation
# to limit the files I need to change, you should declared models
# in this file or you should only include the models you need,
# not everything in api.
# Example: from .api import TranslationHistory
try:
    from .api import *
except ImportError:
    # This means api.py hasn't been created yet
    pass
