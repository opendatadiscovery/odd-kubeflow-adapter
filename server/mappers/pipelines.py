import logging
from odd_contract.models import DataEntity
from typing import List, Iterable, Dict
from mappers.oddrn import generate_pipeline_oddrn


def map_pipelines(host: str, pipeline: Dict) -> DataEntity:
    """
    Raw pipeline example:
        {
        'id': '45f34f06-1461-49d4-a881-251a789dacf2',
        'created_at': datetime.datetime(2021, 3, 11, 12, 58, 19, tzinfo=tzutc()),
        'name': '[Demo] XGBoost - Training with confusion matrix',
        'description': '[source code] A trainer that does end-to-end distributed training for XGBoost models.',
        'parameters':
            [{'name': 'output', 'value': 'gs://{{kfp-default-bucket}}'},
            {'name': 'project', 'value': '{{kfp-project-id}}'},
            {'name': 'diagnostic_mode', 'value': 'HALT_ON_ERROR'},
            {'name': 'rounds', 'value': '5'}],
        'url': None,
        'error': None,
        'default_version':
            {'id': '45f34f06-1461-49d4-a881-251a789dacf2',
            'name': '[Demo] XGBoost - Training with confusion matrix',
            'created_at': datetime.datetime(2021, 3, 11, 12, 58, 19, tzinfo=tzutc()),
            'parameters': [{'name': 'output', 'value': 'gs://{{kfp-default-bucket}}'},
                            {'name': 'project', 'value': '{{kfp-project-id}}'},
                            {'name': 'diagnostic_mode', 'value': 'HALT_ON_ERROR'},
                            {'name': 'rounds', 'value': '5'}],
            'code_source_url': None,
            'package_url': None,
            'resource_references': [{'key':
                                        {'type': 'PIPELINE',
                                        'id': '45f34f06-1461-49d4-a881-251a789dacf2'},
                                        'name': None,
                                        'relationship': 'OWNER'}]}}
    """
    pip_id = pipeline.get('id')
    name = pipeline.get('name', pip_id)
    created_at = pipeline.get('created_at').isoformat()
    resource_references = pipeline.get('default_version')['resource_references'][0]
    description = pipeline.get('description', None)
    inputs = pipeline.get('parameters', None)
    url = pipeline.get('url', None)

    try:
        result = DataEntity.from_dict({
            'oddrn': generate_pipeline_oddrn(host, pip_id),
            'name': name,
            'owner': None,
            'updated_at': None,
            'created_at': created_at,
            # TODO check metadata component
            'metadata': resource_references or None,
            'data_transformer': {
                'description': description,
                'source_code_url': url,
                'sql': None,
                'inputs': inputs or [],
                'outputs': [],
                'subtype': 'DATATRANSFORMER_JOB'
            }
        })
        return result

    except (TypeError, KeyError, ValueError):
        logging.warning(
            "Problems with DataEntity JSON serialization. " 
            "Returning: {}.")
        return {}
