import copy
import decimal
import json
import smtplib
import uuid
from datetime import date, datetime, time, timedelta
from io import BytesIO
from threading import Thread

import numpy as np
import pandas as pd
from django.conf import settings
from django.core.files import File
from django.core.mail import EmailMultiAlternatives, get_connection
from django.http import HttpResponse
from django.template import loader
from django.utils.functional import Promise
from django.utils.timezone import is_aware
from xhtml2pdf import pisa
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import QueryDict
from email.utils import make_msgid

def encodeUrl(data):
    return '?data=' + urlsafe_base64_encode(force_bytes(str(data)))

def decodeUrl(request):
    try:
        url_string = force_text(urlsafe_base64_decode(request.META['QUERY_STRING'].split('data=')[1].split('&_')[0]))
        # Create a QueryDict from the URL string
        url_params = QueryDict(url_string, mutable=True)
        # Set the modified QueryDict back to the request
        request.GET = url_params
        request.GET._mutable = False
    except Exception as e:
        if settings.DEBUG: print('decodeUrl --> ', e)
    return request