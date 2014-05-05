
class PatchMixin(object):

    @property
    def session(self):
        return self.query.session

    @property
    def ses(self):
        return self.query.session

    @classmethod
    def patch(cls):
        for key in dir(cls):
            val = getattr(cls, key)
            if hasattr(val, 'im_func'):
                val = val.im_func
            if key and not key.startswith('_'):
                setattr(cls.model, key, val)

