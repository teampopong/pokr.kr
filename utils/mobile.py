# -*- coding: utf-8 -*-

from collections import defaultdict
import os.path
import re

from flask import current_app, redirect, request, url_for


dict_path = 'data/mobile_user_agents.txt'


class PopongMobile(object):
    mobile_agents_re_dict = defaultdict(set)

    def __init__(self, app):
        self.init_app(app)

    def init_app(self, app):
        self.load_mobile_agents(app)

        @app.route('/mobile')
        def mobile():
            if not self.is_mobile():
                return redirect(url_for('person_main'))
            return 'mobile'

        @app.before_request
        def redirect_if_mobile():
            if self.is_mobile() and request.endpoint != 'mobile':
                return redirect(url_for('mobile'))

    def load_mobile_agents(self, app):
        with open(os.path.join(app.root_path, dict_path), 'r') as f:
            agents = map(str.strip, f)

        self.mobile_agents_re_dict[app.name] = re.compile('|'.join(agents))

    @property
    def mobile_agents_re(self):
        return self.mobile_agents_re_dict[current_app.name]

    def is_mobile(self):
        user_agent = request.user_agent.string.lower()
        return bool(self.mobile_agents_re.search(user_agent))
