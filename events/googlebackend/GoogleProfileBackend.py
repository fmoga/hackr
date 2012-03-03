from urllib import urlencode
from urllib2 import Request, urlopen

from django.utils import simplejson

from social_auth.backends import USERNAME
from social_auth.backends.google import GoogleOAuth2, GoogleOAuth2Backend, BACKENDS

from events.models import HackrUser

from pprint import pprint

import settings


class GoogleProfileBackend(GoogleOAuth2Backend):
  """Google OAuth2 authentication backend"""
  name = 'google-profile'
  DEFAULT_PICTURE = 'https://lh3.googleusercontent.com/-XdUIqdMkCWA/AAAAAAAAAAI/AAAAAAAAAAA/4252rscbv5M/photo.jpg'

  def get_user_details(self, response):
    """Return user details from Google account"""
    user = HackrUser(
      google_id=response.get('id'),
      first_name=response.get('given_name'),
      last_name=response.get('family_name'),
      full_name=response.get('name'),
      email=response.get('email'),
      profile=response.get('link'),
      picture=response.get('picture', self.DEFAULT_PICTURE)
    )
    user.save()

    email = response['email']
    return {
      USERNAME: email.split('@', 1)[0],
      'email': email,
      'first_name': response.get('id',''),
    }


class GoogleProfile(GoogleOAuth2):
  """Google OAuth2 support"""
  AUTH_BACKEND = GoogleProfileBackend

  def get_scope(self):
    return ['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'] + \
      getattr(settings, 'GOOGLE_OAUTH_EXTRA_SCOPE', [])

  def user_data(self, access_token):
    """Return user data from Google API"""
    return self.googleapis_profile('https://www.googleapis.com/oauth2/v1/userinfo', access_token)

  def googleapis_profile(self, url, access_token):
    """Loads user data from googleapis service

       Google OAuth documentation at:
       http://code.google.com/apis/accounts/docs/OAuth2Login.html
       """
    data = {'access_token': access_token, 'alt': 'json'}
    request = Request(url + '?' + urlencode(data))
    try:
      return simplejson.loads(urlopen(request).read())
    except (ValueError, KeyError, IOError):
      return None

BACKENDS['google-profile'] = GoogleProfile
