from flask import url_for

from popong_models import Region

from . import PatchMixin


class RegionPatch(PatchMixin):
    model = Region

    @property
    def url(self):
        return url_for('region', region_id=self.id)

