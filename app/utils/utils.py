import logging

from exceptions.custom_exceptions import ExpectationFailed

logger = logging.getLogger('railway_analyzer_back.apps')


class RequestUtils:
    @staticmethod
    def get_request_data(request) -> tuple:
        try:
            file = request.FILES['csv']
        except Exception as e:
            logger.error(f"Request Utils - Error getting file of request: {e}")
            raise ExpectationFailed(f"La request no contiene ningún fichero")
        try:
            params = request.data.dict()
            del params['csv']
        except Exception as e:
            logger.error(f"Request Utils - Error getting params of request: {e}")
            raise ExpectationFailed(f"Los parámetros de la request son erróneos")
        return file, params
