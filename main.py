#!/usr/bin/env python

"""
main.py -- Udacity conference server-side Python App Engine
    HTTP controller handlers for memcache & task queue access

$Id$

created by wesc on 2014 may 24

"""

__author__ = 'wesc+api@google.com (Wesley Chun)'

import webapp2
from google.appengine.api import app_identity
from google.appengine.api import mail
from google.appengine.api import memcache
from google.appengine.ext import ndb
from models import Conference
from models import Session

from conference import ConferenceApi

MEMCACHE_SPEAKER_KEY = 'SPEAKER'
SPEAKER_TPL = 'More sessions from %s: %s.'

class SetAnnouncementHandler(webapp2.RequestHandler):
    def get(self):
        """Set Announcement in Memcache."""
        ConferenceApi._cacheAnnouncement()
        self.response.set_status(204)


class SendConfirmationEmailHandler(webapp2.RequestHandler):
    def post(self):
        """Send email confirming Conference creation."""
        mail.send_mail(
            'noreply@%s.appspotmail.com' % (
                app_identity.get_application_id()),     # from
            self.request.get('email'),                  # to
            'You created a new Conference!',            # subj
            'Hi, you have created a following '         # body
            'conference:\r\n\r\n%s' % self.request.get(
                'conferenceInfo')
        )

class SetFeatureSpeakerHandler(webapp2.RequestHandler):
    def post(self):
        """Sets the featured speaker in memcache"""
        # Retrieves a list of sessions from the same speaker at this conference

        p_key = ndb.Key(urlsafe=self.request.get('websafeConferenceKey'))

        sessions_by_speaker = Session.query(ancestor=p_key)\
                                     .filter(Session.speaker == self.request.get('speaker'))

        if sessions_by_speaker.count() > 0:
            sessions_str = ''
            for session in sessions_by_speaker:
                sessions_str += session.name + ', '

            sessions_str = sessions_str[:-2]

            speaker_memcache_message = SPEAKER_TPL % (self.request.get('speaker'), sessions_str)
            memcache.set(MEMCACHE_SPEAKER_KEY, speaker_memcache_message)


app = webapp2.WSGIApplication([
    ('/crons/set_announcement', SetAnnouncementHandler),
    ('/tasks/send_confirmation_email', SendConfirmationEmailHandler),
    ('/tasks/setFeaturedSpeaker', SetFeatureSpeakerHandler),
], debug=True)
