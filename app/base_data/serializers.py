import json

from django.contrib.gis.geos import Point

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.base_data.models import Tracing
from app.utils.validators import KmValidators
from exceptions.custom_exceptions import Conflict, BadRequest


class TracingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracing
        fields = '__all__'


class TracingFactorySerializer(serializers.Serializer):
    data = serializers.ListField(allow_empty=False, child=TracingSerializer())


class TracingCreateRequestSerializer(serializers.Serializer):
    csv = serializers.ListField()
    params = serializers.DictField()

    def validate(self, initial_data):
        params = initial_data.get('params')
        csv_data = initial_data.get('csv')

        line, track, km_i, km_f = params.get('line'), params.get('track'), params.get('km_i'), params.get('km_f')

        csv_kms = list(map(lambda data_line: float(data_line.get('km')), csv_data))
        max_km, min_km = max(csv_kms), min(csv_kms)
        if max_km != km_f or min_km != km_i:
            raise BadRequest("La extensión del fichero csv no se ajusta a los km enviados en la request")

        def validate_csv_line(data_line):
            flag_error_validators = [
                lambda csv_line: csv_line.get('line') != line,
                lambda csv_line: csv_line.get('track') != track,
                lambda csv_line: km_i > float(csv_line.get('km')) or km_f < float(csv_line.get('km'))
            ]
            return any(rule(data_line) for rule in flag_error_validators)

        if any([validate_csv_line(data_line) for data_line in csv_data]):
            raise BadRequest("Línea o vía no corresponden con la request o el fichero csv excede los límites indicados")

        csv_data_serializer = TracingFactorySerializer(data={"data": csv_data})
        csv_data_serializer.is_valid(raise_exception=True)
        return csv_data_serializer.validated_data


class TracingCreateParamsSerializer(serializers.Serializer):
    line = serializers.CharField(required=True, max_length=5)
    track = serializers.CharField(required=True, max_length=5)
    km_i = serializers.FloatField(required=True)
    km_f = serializers.FloatField(required=True)

    def validate(self, params):
        KmValidators.validate_km_received(params)
        KmValidators.validate_kms_order(params)
        return params


class TracingDeleteParamsSerializer(serializers.Serializer):
    line = serializers.CharField(required=True, max_length=5)
    track = serializers.CharField(required=True, max_length=5)
    km_i = serializers.FloatField(required=False)
    km_f = serializers.FloatField(required=False)

    def validate(self, params):
        KmValidators.validate_km_received(params)
        KmValidators.validate_kms_order(params)
        return params

#
# class RailDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RailDetails
#         fields = '__all__'
#
#
# class RailDetailsFactorySerializer(serializers.Serializer):
#     data = serializers.ListField(allow_empty=False, child=RailDetailsSerializer())
#
#
# class RailDetailsListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RailDetails
#         fields = '__all__'
#
#     @staticmethod
#     def validate_geometry(geometry: Point()):
#         return json.loads(geometry.geojson)
