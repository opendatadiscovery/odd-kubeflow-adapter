from typing import List, Dict
import logging
from urllib.parse import urlparse


def generate_pipeline_oddrn(host: str, pip_id: str) -> str:
    return f'//kubeflow/{host}/pipeline/{pip_id}'


def generate_experiment_oddrn(host: str, exp_id: str) -> str:
    return f'//kubeflow/{host}/experiment/{exp_id}'


def generate_run_oddrn(host: str, exp_id: str, run_id: str) -> str:
    return f'//kubeflow/{host}/experiment/{exp_id}/run/{run_id}'


def generate_input_oddrn(parameters: Dict[str, str]) -> str or None:
    try:
        if parameters.get('value', None) is not None:
            value = parameters.get('value')
            url = urlparse(value)
            if url.scheme in ('s3', 'gs'):
                bucket = f'/{url.scheme}/{url.netloc}/prefixes{url.path}'
                return bucket
            else:
                return value

    except Exception:
        logging.error('Parameter value is None')
        logging.exception(Exception)
        return None
