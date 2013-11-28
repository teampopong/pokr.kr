# -*- coding: utf-8 -*-

from base import Controller
from person import PersonController


def controllers(model):
    _controllers = [controller
                    for controller in Controller.__subclasses__()
                    if controller.model == model]
    if len(_controllers) > 1:
        raise RuntimeError('Too many controllers with the same model: %s' % model)
    return _controllers.pop()
