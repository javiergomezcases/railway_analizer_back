from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response

from app.base_data.providers import TracingProvider
from app.base_data.serializers import TracingDeleteParamsSerializer, TracingCreateRequestSerializer, \
    TracingCreateParamsSerializer
from app.base_data.utils.mappers import TracingMapper
from app.utils.utils import RequestUtils
from app.utils.validators import TracingValidators

from exceptions.exception_handler import helper_exceptions


class TracingViewSet(ViewSet):
    tracing_mapper = TracingMapper()
    tracing_provider = TracingProvider()
    request_utils = RequestUtils()

    @helper_exceptions
    def create(self, request):
        file, params = self.request_utils.get_request_data(request)
        params_serializer = TracingCreateParamsSerializer(data=params)
        params_serializer.is_valid(raise_exception=True)
        csv_raw_data = self.tracing_mapper.csv_data_ready(file)
        csv_ready_data = [self.tracing_mapper.csv_data_line_2_dict(data) for data in csv_raw_data]  # TODO username
        # in csv_data_line_2_dict function
        serializer = TracingCreateRequestSerializer(data={"csv": csv_ready_data,
                                                          "params": params_serializer.validated_data})
        serializer.is_valid(raise_exception=True)
        TracingValidators().validate_existing_data(params_serializer.validated_data, serializer.validated_data['data'])
        self.tracing_provider.create_tracing(serializer.validated_data['data'])
        return Response({}, status=status.HTTP_201_CREATED)

    @helper_exceptions
    def retrieve(self, request, pk):
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    @helper_exceptions
    def delete(self, request, pk):
        serializer = TracingDeleteParamsSerializer(data=self.tracing_mapper.delete_request_2_dict(pk, request))
        serializer.is_valid(raise_exception=True)
        return Response(self.tracing_provider.delete_tracing(serializer.validated_data), status=status.HTTP_200_OK)


# class RailDetailsViewSet(ViewSet):
#     rail_details_mapper = RailDetailsMapper()
#     rail_details_provider = RailDetailsProvider()
#
#     @helper_exceptions
#     def create(self, request):
#         csv_data = self.rail_details_mapper.csv_data_ready(request.FILES['data'])
#         rail_detail_objects = self.rail_details_mapper.csv_data_2_rail_detail_objects(csv_data)
#         serializer = RailDetailsFactorySerializer(data={"data": rail_detail_objects})
#         serializer.is_valid(raise_exception=True)
#         self.rail_details_provider.create_rail_details(serializer.validated_data['data'])
#         return Response({}, status=status.HTTP_201_CREATED)
#
#     @helper_exceptions
#     def list(self, request):
#         params_serializer = BasicParamsSerializer(data=request.query_params)
#         params_serializer.is_valid(raise_exception=True)
#         validated_params = params_serializer.validated_data
#         rail_details_data = self.rail_details_provider.list_rail_details(validated_params)
#         rail_details_data_serializer = RailDetailsListSerializer(data=rail_details_data, many=True)
#         rail_details_data_serializer.is_valid(raise_exception=True)
#         return Response(rail_details_data_serializer.validated_data, status=status.HTTP_200_OK)
#
#     @helper_exceptions
#     def retrieve(self, request, pk):
#         return Response({}, status=status.HTTP_400_BAD_REQUEST)
#
#     @helper_exceptions
#     def delete(self, request, pk):
#         serializer = DataVersionSerializer(data={'data_version': pk})
#         serializer.is_valid(raise_exception=True)
#         return Response(self.rail_details_provider.delete_rail_details(serializer.validated_data),
#                         status=status.HTTP_200_OK)
