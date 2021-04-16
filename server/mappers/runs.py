import logging
from odd_contract.models import DataEntity
from typing import Dict
from mappers.oddrn import generate_experiment_oddrn, generate_run_oddrn

KUBEFLOW_STORAGE_STATE = {
    'Error': 'ABORTED',
    'Succeeded': 'SUCCESS',
    'Failed': 'FAIL',
}


def map_runs(host: str, run: Dict) -> DataEntity:
    """
    Raw run example:
        {  'created_at': datetime.datetime(2021, 3, 11, 17, 21, 44, tzinfo=tzutc()),
           'description': None,
           'error': None,
           'finished_at': datetime.datetime(2021, 3, 11, 17, 30, 50, tzinfo=tzutc()),
           'id': '438382df-8c03-44aa-a400-71c413473f85',
           'metrics': None,
           'name': 'test-run',
           'pipeline_spec': {'parameters': [{'name': 'data_s3_url',
                                             'value': None},
                                            {'name': 'yolov4_config_s3_url',
                                             'value': None},
                                            {'name': 'yolov4_weights_s3_url',
                                             'value': None}],
                             'pipeline_id': None,
                             'pipeline_manifest': None,
                             'pipeline_name': None,
                             'workflow_manifest': '{"kind":"Workflow","apiVersion":"argoproj.io/v1alpha1",
                                                    ....
                                                   "container":{"name":"",
                                                   "image":"394544957709.dkr.ecr.eu-central-1.amazonaws.com/training_yolov4:latest",
                                                  "command":["darknet","detector","train"]},
           'resource_references': [{'key': {'id': '86078488-0809-43d0-8177-31cec3d88302',
                                            'type': 'EXPERIMENT'},
                                    'name': 'default',
                                    'relationship': 'OWNER'},
                                   {'key': {'id': '22f26341-e96f-4758-b515-98bc9be55b40',
                                            'type': 'PIPELINE_VERSION'},
                                    'name': 'test1-2',
                                    'relationship': 'CREATOR'}],
           'scheduled_at': datetime.datetime(1970, 1, 1, 0, 0, tzinfo=tzutc()),
           'service_account': 'default-editor',
           'status': 'Failed',
           'storage_state': None}
    """
    status = KUBEFLOW_STORAGE_STATE.get(run['status'], 'OTHER')

    experiment_id = run['resource_references'][0]['key']['id']
    run_id = run['id']
    name = run['name']
    parameters = run['pipeline_spec']['parameters']
    created_at = run['created_at'].isoformat()
    finished_at = run['finished_at'].isoformat()

    try:
        result = DataEntity.from_dict({
            'oddrn': generate_experiment_oddrn(host, experiment_id),
            'name': name,
            'owner': None,
            # TODO check metadata component
            'metadata': {'parameters': parameters},
            'data_transformer_run': {
                'start_time': created_at,
                'end_time': finished_at,
                'transformer_oddrn': generate_run_oddrn(host, experiment_id, run_id),
                'status_reason': None,
                'status': status
            }
        })
        return result
    except (TypeError, KeyError, ValueError):
        logging.warning(
            "Problems with DataEntity JSON serialization. " 
            "Returning: {}.")
        return {}

