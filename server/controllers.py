import logging
from datetime import datetime
from typing import List, Tuple, Any, Dict
import pytz

from flask import Response
from odd_contract import ODDController
from odd_contract.encoder import JSONEncoder


class OpenDataDiscoveryController(ODDController):
    __encoder = JSONEncoder()
    __empty_cache_response = Response(status=503, headers={'Retry-After': 30})

    def __init__(self, host, kubeflow_adapter):
        self.__host = host
        self.__kubeflow_adapter = kubeflow_adapter

    def get_data_entities(self, changed_since: Dict[str, Any] = None):
        changed_since = pytz.UTC.localize(datetime.strptime(changed_since['changed_since'], "%Y-%m-%dT%H:%M:%SZ")) \
            if changed_since['changed_since'] is not None \
            else None
        data_entities = self.__kubeflow_adapter.retrieve_data_entities()

        if data_entities is None:
            logging.warning('DataEntities has never been enriched')
            return []

        return self.__build_response(data_entities)

    def __build_response(self, data: Tuple[List, datetime]):
        return Response(
            response=self.__encoder.encode({
                'data_source_oddrn': f'//kubeflow/{self.__host}',
                'items': data[0]
            }),
            headers={'Last-Modified': data[1].strftime("%a, %d %b %Y %H:%M:%S GMT")},
            content_type='application/json',
            status=200
        )
