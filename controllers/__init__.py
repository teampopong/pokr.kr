# -*- coding: utf-8 -*-

from base import Controller
from bill import BillController
from person import PersonController
from region import RegionController
from user import UserController


CONTROLLERS = Controller.__subclasses__()


def controllers(model):
    _controllers = [controller for controller in CONTROLLERS
                               if controller.model == model]
    if len(_controllers) > 1:
        raise RuntimeError('Too many controllers with the same model: %s' % model)
    return _controllers.pop()


def init_controller(app):
    for controller in CONTROLLERS:
        controller.init(app)

