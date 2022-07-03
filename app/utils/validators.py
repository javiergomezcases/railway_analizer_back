from rest_framework import serializers

from app.base_data.models import Tracing
from exceptions.custom_exceptions import BadRequest


class KmValidators:
    @staticmethod
    def validate_km_received(params: dict):
        try:
            if params.get('km_i') and not params.get('km_f'):
                raise serializers.ValidationError("km_f is not provided")
            if params.get('km_f') and not params.get('km_i'):
                raise serializers.ValidationError("km_i is not provided")
        except Exception:
            raise BadRequest

    @staticmethod
    def validate_kms_order(params: dict):
        try:
            if not params.get('km_i') or not params.get('km_f') \
                    or float(params.get('km_i')) >= float(params.get('km_f')):
                raise serializers.ValidationError("Incorrect kms provided")
        except Exception:
            raise BadRequest


class TracingValidators:
    @staticmethod
    def validate_existing_data(params: dict, data_2_insert: list):
        try:
            existing_kms = list(Tracing.objects.filter(line=params.get('line'), track=params.get('track'),
                                                       km__gte=params.get('km_i'), km__lte=params.get('km_f'))
                                .values_list('km', flat=True))
            km_2_insert = list(map(lambda data: float(data.get('km')), data_2_insert))
            intersection = set(km_2_insert).intersection(existing_kms)
            if intersection:
                raise serializers.ValidationError(f"Algunos km a insertar ya existen en la base de datos")
        except Exception as e:
            raise BadRequest(e)

