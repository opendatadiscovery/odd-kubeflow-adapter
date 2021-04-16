## OpenDataDiscovery Kubeflow adapter
* [Requirements](#requirements)
* [ENV variables basic](#env-variables-for-basic-auth)
* [ENV variables non-basic](#env-variables-for-non-basic-auth)
* [Pipeline DataEntity example](#dataset-structure-example)
* [Experiment DataEntity example](#metadata-structure-example)

 
## Requirements 
* --extra-index-url https://test.pypi.org/simple/
* python-dateutil==2.8.1
* flask==1.1.2
* gunicorn===20.0.4
* odd-contract-dev==0.0.22
* more-itertools==8.6.0
* pytz==2021.1
* kfp==1.4.0


## ENV variables for basic auth
```
KUBEFLOW_HOST=kf-access-odd-704581925.us-east-2.elb.amazonaws.com
KUBEFLOW_NAMESPACE=main
```

## ENV variables for Non-basic auth
Follow these steps: https://www.kubeflow.org/docs/aws/pipeline/#authenticate-kubeflow-pipeline-using-sdk-inside-cluster
```
KUBEFLOW_HOST=kubeflow.ws.provectus.io
KUBEFLOW_NAMESPACE=main
KUBEFLOW_SESSION_COOKIE0=AWSELBAuthSessionCookie-0=YOUR-COOKIE0
KUBEFLOW_SESSION_COOKIE1=AWSELBAuthSessionCookie-1=YOUR-COOKIE1
```

## Pipeline DataEntity example:
```
{
    "oddrn": "//kubeflow/kf-access-odd-704581925.us-east-2.elb.amazonaws.com/pipeline/b2747932-bb39-47af-8fc8-c5e1eb1c0a60",
    "name": "downloader_aumget",
    "metadata": [],
    "created_at": "2021-03-12T11:04:52+00:00",
    "data_transformer": 
        {
            "description": "Downloads data from s3 and augments it",
            "inputs": [
                "{'name': 's3_data_path', 'value': 's3://worker-safety-dataset-ws/KubeFlow/data/data-kf.zip'}",
                "{'name': 'list_file_path', 'value': 'data/list-train-stratified.txt'}",
                "{'name': 'output_path', 'value': 'augmented'}",
                "{'name': 'repetitions', 'value': '3'}",
                "{'name': 'max_workers', 'value': '5'}"
            ],
            "outputs": [],
            "subtype": "DATATRANSFORMER_JOB"
        }
}
```

## Experiment DataEntity example:
```
{
    "oddrn": "//kubeflow/kf-access-odd-704581925.us-east-2.elb.amazonaws.com/experiment/86078488-0809-43d0-8177-31cec3d88302",
    "name": "test-run",
    "metadata": [],
    "data_transformer_run": {
        "transformer_oddrn": "//kubeflow/kf-access-odd-704581925.us-east-2.elb.amazonaws.com/experiment/86078488-0809-43d0-8177-31cec3d88302/run/438382df-8c03-44aa-a400-71c413473f85",
        "start_time": "2021-03-11T17:21:44+00:00",
        "end_time": "2021-03-11T17:30:50+00:00",
        "status": "FAIL"
    }
}
```
