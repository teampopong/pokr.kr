# -*- coding: utf-8 -*-

from builtins import object
from collections import defaultdict
import os.path
import re

from flask import current_app, request


agents = '''
sony
symbian
nokia
samsung
mobile
windows ce
epoc
opera mini
nitro
j2me
midp-
cldc-
netfront
mot
up.browser
up.link
audiovox
blackberry
ericsson,
panasonic
philips
sanyo
sharp
sie-
portalmmm
blazer
avantgo
danger
palm
series60
palmsource
pocketpc
smartphone
rover
ipaq
au-mic,
alcatel
ericy
up.link
docomo
vodafone/
wap1.
wap2.
plucker
480x640
sec
fennec
android
google wireless transcoder
nintendo
webtv
playstation
'''
agents = [agent.strip() for agent in agents.split('\n') if agent.strip()]
agents_re = re.compile('|'.join(agents))


class PopongMobile(object):
    mobile_agents_re_dict = defaultdict(set)

    def __init__(self, app):
        self.init_app(app)

    def init_app(self, app):
        self.mobile_agents_re_dict[app.name] = agents_re

        @app.context_processor
        def inject_mobile():
            return dict(mobile=self.is_mobile())

    @property
    def mobile_agents_re(self):
        return self.mobile_agents_re_dict[current_app.name]

    def is_mobile(self):
        user_agent = request.user_agent.string.lower()
        return bool(self.mobile_agents_re.search(user_agent))

