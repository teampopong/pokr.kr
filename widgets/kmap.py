# -*- coding: utf-8 -*-

from flask import current_app, render_template


def kmap(region_or_id=None, **kwargs):
    region_id = getattr(region_or_id, 'id', region_or_id) if region_or_id else None

    return render_template('widgets/kmap.html', region_id=region_id, **kwargs)
