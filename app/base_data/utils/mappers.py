import logging

from rest_framework.request import Request

from app.base_data.models import Tracing

from exceptions.custom_exceptions import BadRequest, Conflict

logger = logging.getLogger('railway_analyzer_back.apps')


class TracingMapper:
    @staticmethod
    def csv_data_ready(csv):
        try:
            data = csv.read().decode('ISO-8859-1').split('\n')
            # Delete file header
            return [line.split(';') for line in data[1:-1]]
        except Exception as e:
            logger.error(f"Tracing Mapper: Error reading csv: {e}")
            raise BadRequest(f"El fichero CSV no puede ser tratado")

    @staticmethod
    def csv_data_line_2_dict(csv_data_line, created_by='yo') -> dict:
        try:
            return {
                "line": csv_data_line[0],
                "track": csv_data_line[1],
                "km": csv_data_line[2],
                "geometry_type": csv_data_line[3],
                "radius": csv_data_line[4],
                "arrow": csv_data_line[5],
                "theo_width": csv_data_line[6],
                "radius_width": csv_data_line[7],
                "use_width": csv_data_line[8],
                "project_cant": csv_data_line[9],
                "created_by": created_by
            }
        except Exception as e:
            logger.error(f"Tracing Mapper: Error converting csv data to dict: {e}")
            raise BadRequest(f"Error al tratar datos del csv en P.K {csv_data_line[2]}. Verificar columnas y valores")

    def csv_data_2_list(self, csv_data: list) -> list:
        return [self.__csv_data_line_2_model(csv_data_line) for csv_data_line in csv_data]

    @staticmethod
    def __csv_data_line_2_model(data_line) -> Tracing:
        try:
            return Tracing(
                line=data_line['line'],
                track=data_line['track'],
                km=data_line['km'],
                geometry_type=data_line['geometry_type'],
                radius=data_line['radius'],
                arrow=data_line['arrow'],
                theo_width=data_line['theo_width'],
                radius_width=data_line['radius_width'],
                use_width=data_line['use_width'],
                project_cant=data_line['project_cant'],
                created_by=data_line['created_by']
            )
        except Exception as e:
            logger.error(f"Tracing Mapper: Error converting csv data to Tracing object: {e}")
            raise BadRequest(f"Error en el tipo de dato alojado en csv. P.K {data_line['km']}")

    @staticmethod
    def delete_request_2_dict(pk: str, request: Request):
        try:
            request_dict = {}
            if pk:
                request_dict['line'] = pk
            if request.query_params.get('track'):
                request_dict['track'] = request.query_params.get('track')
            if request.query_params.get('km_i'):
                request_dict['km_i'] = request.query_params.get('km_i')
            if request.query_params.get('km_f'):
                request_dict['km_f'] = request.query_params.get('km_f')
            return request_dict
        except Exception as e:
            logger.error(f"Tracing Mapper: Error converting delete request to dict: {e}")
            raise BadRequest(f"Error en los parámetros enviados en la request")


# class RailDetailsMapper:
#     geometries_provider = GeometriesProvider()
#
#     @staticmethod
#     def csv_data_ready(csv):
#         try:
#             data = csv.read().decode('ISO-8859-1').split('\n')
#             return [line.split(';') for line in data[1:-1]]
#         except Exception as e:
#             logger.error(f"Rail details Mapper: Error when reading csv: {e}")
#             raise BadRequest(f"El fichero CSV no puede ser tratado o no está debidamente exportado")
#
#     def csv_data_2_rail_detail_objects(self, csv_data) -> list:
#         try:
#             x_coords, y_coords = [float("{0:.4f}".format(float(csv_data_line[13]))) for csv_data_line in csv_data], \
#                                  [float("{0:.4f}".format(float(csv_data_line[14]))) for csv_data_line in csv_data]
#         except Exception as e:
#             logger.error(f"Rail Details Mapper: Error when getting coordinates {e}")
#             raise BadRequest(f"Error en CSV al obtener coordenadas. P.K : {csv_data[1]}")
#
#         lat_list, lon_list = self.__get_utm_2_geo_coordinate_lists(x_coords, y_coords)
#         geojsons_list = [self.__build_geojson_geometry(lat, lon) for lat, lon in zip(lat_list, lon_list)]
#         return [self.__build_rail_detail_object(csv_data_line, geojson_geometry)
#                 for csv_data_line, geojson_geometry in zip(csv_data, geojsons_list)]
#
#     @staticmethod
#     def __build_rail_detail_object(csv_data_line, geojson_geometry):
#         try:
#             return {
#                 "pk_geo": csv_data_line[0],
#                 "pk_client": csv_data_line[1],
#                 "line": csv_data_line[2],
#                 "track": csv_data_line[3],
#                 "category": csv_data_line[4],
#                 "direction": csv_data_line[5],
#                 "rail_typology_code": csv_data_line[6],
#                 "armament": csv_data_line[7],
#                 "fastening": csv_data_line[8],
#                 "rail_typology": csv_data_line[9],
#                 "circulation_speed": csv_data_line[10],
#                 "technical_location_code": csv_data_line[11],
#                 "inter_station_code": csv_data_line[12],
#                 "geometry": geojson_geometry,
#                 "created_by": csv_data_line[15],
#                 "data_version": csv_data_line[16]
#             }
#         except Exception as e:
#             logger.error(f"Rail details Mapper: error when getting data of csv. {e}")
#             raise BadRequest(f"Error en CSV P.K {csv_data_line[1]}. Verificar columnas y valores")
#
#     @staticmethod
#     def __get_utm_2_geo_coordinate_lists(x_list, y_list):
#         try:
#             # UTM 30N WGS84 -> 25830
#             # GEO WGS84 -> 4326
#             # Valencian Community AOI -> -1.5º, 37.5º, 1.5º, 41º
#             transformer = Transformer.from_crs(25830, 4326, area_of_interest=AreaOfInterest(-1.5, 37.5, 1.5, 41))
#             return transformer.transform(x_list, y_list)
#         except Exception as e:
#             logger.error(f"Rail Details Mapper: Error when transform coordinates utm to geo: {e}")
#             raise Conflict(f"Error en la transformación de coordenadas UTM a Geográfias WGS84")
#
#     @staticmethod
#     def __build_geojson_geometry(lat, lon):
#         return '{"type": "Point","coordinates": [' + str(lon) + ',' + str(lat) + ']}'
#
#     def csv_data_2_list(self, csv_data: list) -> list:
#         return [self.__csv_data_line_2_model(csv_data_line) for csv_data_line in csv_data]
#
#     def __csv_data_line_2_model(self, data_line) -> RailDetails:
#         try:
#             geometry = self.geometries_provider.geojson_2_geometry(data_line['geometry'])
#             return RailDetails(
#                 pk_geo=data_line['pk_geo'],
#                 pk_client=data_line['pk_client'],
#                 line=data_line['line'],
#                 track=data_line['track'],
#                 category=data_line['category'],
#                 direction=data_line['direction'],
#                 rail_typology_code=data_line['rail_typology_code'],
#                 armament=data_line['armament'],
#                 fastening=data_line['fastening'],
#                 rail_typology=data_line['rail_typology'],
#                 circulation_speed=data_line['circulation_speed'],
#                 technical_location_code=data_line['technical_location_code'],
#                 inter_station_code=data_line['inter_station_code'],
#                 geometry=geometry,
#                 created_by=data_line['created_by'],
#                 data_version=data_line['data_version']
#             )
#         except Exception as e:
#             logger.error(f"Rail details Mapper: Error when reading csv: {e}")
#             raise BadRequest(f"Error en el tipo de dato alojado en csv. P.K {data_line['pk_client']}")
