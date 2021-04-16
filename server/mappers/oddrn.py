
def generate_pipeline_oddrn(host: str, pip_id: str) -> str:
    return f'//kubeflow/{host}/pipeline/{pip_id}'


def generate_experiment_oddrn(host: str, exp_id: str) -> str:
    return f'//kubeflow/{host}/experiment/{exp_id}'


def generate_run_oddrn(host: str, exp_id: str, run_id: str) -> str:
    return f'//kubeflow/{host}/experiment/{exp_id}/run/{run_id}'
