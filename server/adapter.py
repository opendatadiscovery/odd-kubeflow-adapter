from datetime import datetime
from typing import List, Iterable, Tuple, Dict
from itertools import chain
from odd_contract.models import DataEntity
from api import ApiGetter
from mappers.pipelines import map_pipelines
from mappers.runs import map_runs

KubeflowDataEntry = Tuple[List[DataEntity], datetime]


class KubeflowAdapter:
    __DATA_ENTITIES: KubeflowDataEntry = None

    def __init__(self, host: str, namespace: str, session_cookie0: str, session_cookie1: str) -> None:
        self.__host = host
        self.__cookies = f"{session_cookie0};{session_cookie1}"
        self.__namespace = namespace
        self.__api = ApiGetter(self.__host, self.__cookies, self.__namespace)

    def __get_pipelines(self) -> Iterable[DataEntity]:
        all_pipelines = self.__api.get_all_pipelines()
        return [self.__process_pipeline_raw_data(pipeline) for pipeline in all_pipelines]

    def __get_runs(self) -> Iterable[DataEntity]:
        all_runs = self.__api.get_all_runs()
        return [self.__process_run_raw_data(run) for run in all_runs]

    def __process_pipeline_raw_data(self, pipeline: Dict) -> DataEntity:
        return map_pipelines(self.__host, pipeline)

    def __process_run_raw_data(self, run: Dict) -> DataEntity:
        return map_runs(self.__host, run)

    def retrieve_data_entities(self) -> Tuple[list, datetime]:
        self.__DATA_ENTITIES = list(chain(self.__get_pipelines(), self.__get_runs())), datetime.utcnow()
        return self.__DATA_ENTITIES
