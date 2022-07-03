from django.db import models
from django.contrib.gis.db import models as gis_models

from app.base_data.utils.enumerators import *


class CommonField(models.Model):
    line = models.CharField(max_length=5, null=False, blank=False)
    track = models.CharField(max_length=5, null=False, blank=False)
    km = models.FloatField(null=False, blank=False)
    created = models.DateField(auto_now_add=True)
    created_by = models.CharField(max_length=20, null=False, blank=False)

    class Meta:
        abstract = True
        ordering = ['line', 'track', 'km']


class Tracing(CommonField):
    geometry_type = models.CharField(max_length=20, null=False, blank=False, choices=RailGeometryEnum.description())
    radius = models.CharField(max_length=20, null=False, blank=False)
    arrow = models.CharField(max_length=20, null=False, blank=False)
    theo_width = models.CharField(max_length=20, null=False, blank=False)
    radius_width = models.CharField(max_length=20, null=False, blank=False)
    use_width = models.CharField(max_length=20, null=False, blank=False)
    project_cant = models.CharField(max_length=20, null=False, blank=False)


class RailDetails(CommonField):
    category = models.CharField(max_length=20, null=False, blank=False, choices=RailCirculationCategory.description())
    direction = models.CharField(max_length=20, null=False, blank=False, choices=RailDirection.description())
    rail_typology_code = models.CharField(
        max_length=20, null=False, blank=False,
        choices=RailTypologyCode.description()
    )
    armament = models.CharField(max_length=20, null=False, blank=False, choices=RailArmamentEnum.description())
    fastening = models.CharField(max_length=20, null=True, blank=True, default='')
    rail_typology = models.CharField(max_length=20, null=False, blank=False, choices=RailTypologyEnum.description())
    circulation_speed = models.CharField(max_length=5, null=False, blank=False)
    technical_location_code = models.CharField(max_length=20, null=False, blank=False)
    inter_station_code = models.CharField(max_length=20, null=True, blank=True, default='')
    geometry = gis_models.PointField()
