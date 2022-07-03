import logging

from app.base_data.models import Tracing
from app.base_data.utils.mappers import TracingMapper
from app.base_data.utils.geometries_provider import GeometriesProvider

from exceptions.custom_exceptions import Conflict, ExpectationFailed, BadRequest

logger = logging.getLogger('railway_analyzer_back.apps')


class TracingProvider:
    tracing_mapper = TracingMapper()

    def create_tracing(self, csv_data) -> None:
        if not csv_data:
            logger.error(f"Tracing Provider - No csv provided")
            raise BadRequest
        tracing_list = self.tracing_mapper.csv_data_2_list(csv_data)
        try:
            Tracing.objects.bulk_create(tracing_list)
            return None
        except Exception as e:
            logger.error(f"Tracing Provider - Error saving tracing data in db: {e}")
            raise ExpectationFailed(f"Error en la inserción del trazado en la base de datos")

    @staticmethod
    def list_tracing(params) -> list:
        try:
            line, track, km_i, km_f = params.get('line'), params.get('track'), params.get('km_i'), params.get('km_f')
        except Exception as e:
            logger.error(f"Tracing Provider - Error getting list params: {e}")
            raise ExpectationFailed("Error en los parámetros pasados para listar datos de trazado.")
        try:
            tracing_data = Tracing.objects.filter(line=line, track=track)
            if km_i and km_f:
                tracing_data = tracing_data.filter(km__gte=params.get('km_i'), km__lte=params.get('km_f'))
        except Exception as e:
            logger.error(f"Tracing Provider - Error during list tracing data: {e}")
            raise ExpectationFailed("Error en la base de datos al obtener datos de trazado.")
        if not tracing_data:
            return []
        return tracing_data.order_by('km')

    @staticmethod
    def delete_tracing(params: dict) -> None:
        if not params:
            logger.error(f"Tracing Provider - Error, delete params not provided")
            raise Conflict("Los parámetros de borrado no han sido enviados")
        try:
            query = Tracing.objects.filter(line=params.get('line'), track=params.get('track'))
            if params.get('km_i') and params.get('km_f'):
                query = query.filter(km__gte=params.get('km_i'), km__lte=params.get('km_f'))
            query.delete()
            return None
        except Exception as e:
            logger.error(f"Tracing Provider - Error during delete tracing data in db: {e}")
            raise ExpectationFailed(f"Error al borrar el trazado de la base de datos")


# class RailDetailsProvider:
#     rail_details_mapper = RailDetailsMapper()
#     geometries_provider = GeometriesProvider()
#
#     def create_rail_details(self, csv_data) -> None:
#         if not csv_data:
#             logger.error(f"RailDetail Provider - No csv provided")
#             raise BadRequest("No se ha adjuntado un CSV")
#         try:
#             rail_details_list = self.rail_details_mapper.csv_data_2_list(csv_data)
#             RailDetails.objects.bulk_create(rail_details_list)
#             return None
#         except Exception as e:
#             logger.error(f"RailDetail Provider - Error during creating rail details data in db: {e}")
#             raise ExpectationFailed(" Error en la inserción de detalles de vía ")
#
#     @staticmethod
#     def list_rail_details(params, listed=True) -> list:
#         try:
#             pk_i_geo, pk_f_geo, line, track, current, params = BasicParamsProvider().get_basic_params(params)
#             rail_details_data = RailDetails.objects.filter(
#                     pk_geo__gte=pk_i_geo, pk_geo__lte=pk_f_geo, line=line, track=track, current=current, **params
#                 )
#         except Exception as e:
#             logger.error(f"RailDetail Provider - Error during list tracing data in db: {e}")
#             raise ExpectationFailed("Error en la base de datos al listar los detalles de vía")
#
#         if not rail_details_data:
#             logger.warning(f"Rail Details Provider - No rail details filtered for this params {params}")
#             return []
#         if listed:
#             return list(rail_details_data.values().order_by('pk_geo'))
#         return rail_details_data
#
#     @staticmethod
#     def delete_rail_details(data_version: str) -> None:
#         if not data_version:
#             logger.error(f"RailDetail Provider - no data version provided for deleting rail details")
#             raise Conflict("No se ha provisto una versión para el borrado de datos de vía")
#         try:
#             RailDetails.objects.filter(data_version=data_version).delete()
#             return None
#         except Exception as e:
#             logger.error(f"RailDetail Provider - Error during deleting rail details data in db: {e}")
#             raise ExpectationFailed("Error durante el borrado de detalles de vía")
#
#     """ Function return a geometries dictionary with pk_geo in keys """
#     @staticmethod
#     def get_geometries_dict(rail_details: list) -> dict:
#         geometries_dict = {}
#         for detail in rail_details:
#             geometries_dict[detail.get('pk_geo')] = detail.get('geometry')
#         return geometries_dict
