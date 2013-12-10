# -*- coding: utf-8 -*-

from base import Controller
from bill import BillController
from person import PersonController
from region import RegionController
from user import UserController


def init_controller(app):
    controllers = Controller.__subclasses__()
    for controller in controllers:
        controller.init(app)
        app.jinja_env.globals.update({
            controller.__name__: controller
        })

