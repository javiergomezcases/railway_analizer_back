import logging

from django.contrib.gis.geos import GEOSGeometry

from exceptions.custom_exceptions import Conflict

logger = logging.getLogger('sicaf_middleware.apps')


class GeometriesProvider:
    @staticmethod
    def geojson_2_geometry(geojson: str):
        try:
            if not geojson:
                return None
            return GEOSGeometry(str(geojson))

        except Exception as e:
            logger.error(f"Geometries Provider - Error during geojson transformation: {geojson}")
            raise Conflict("Error durante la transformación a geometría")
