from popong_models import Base
from . import bill
from . import bill_feed
from . import favorite_keyword
from . import favorite_person
from . import feed
from . import party
from . import person
from . import region
from . import query_log
from . import user
from .patch import PatchMixin


def patch_all():
    for subclass in PatchMixin.__subclasses__():
        subclass.patch()

