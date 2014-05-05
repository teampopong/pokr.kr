from popong_models import Base
import bill_feed
import favorite_keyword
import favorite_person
import feed
import query_log
import user


class PatchMixin(object):

    @property
    def session(self):
        return self.query.session

    @classmethod
    def patch(cls):
        for key, val in cls.__dict__.iteritems():
            if not key.startswith('_'):
                setattr(cls.model, key, val)


def patch_all():
    import bill
    import party
    import person
    import region
    for subclass in PatchMixin.__subclasses__():
        subclass.patch()

