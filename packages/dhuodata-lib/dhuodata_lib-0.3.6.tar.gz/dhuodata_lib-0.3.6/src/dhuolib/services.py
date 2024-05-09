import json

import requests


class ServiceAPIML:
    def __init__(self, service_endpoint):

        if not isinstance(service_endpoint, str):
            raise ValueError("service_endpoint must be a string")

        self.service_endpoint = f"{service_endpoint}/api/experiment"
        self.headers = {"Content-Type": "application/json"}

    def create_experiment_by_conf_json(self, experiment_params):
        if experiment_params is None and isinstance(experiment_params, dict):
            raise ValueError("json_data must be a dict")

        if 'model_pkl_file' in experiment_params.keys():
            return requests.post(
                f"{self.service_endpoint}/save", data=experiment_params, headers={"Content-Type": "multipart/form-data"}
            )
            
        return requests.post(f"{self.service_endpoint}/save", data=json.dumps(experiment_params), headers=self.headers)

    def run_experiment(self, params={}, files=None):
        if params is None and isinstance(params, str):
            raise ValueError("json_data must be a dict")
        
        response = requests.post(
            f"{self.service_endpoint}/run",
            data=params,
            files=files
        )
        return response

    def create_model(self, model_params):
        if model_params is None and not isinstance(model_params, dict):
            raise ValueError("json_data must be a dict")
        response = requests.post(
            f"{self.service_endpoint}/model",
            data=json.dumps(model_params),
            headers=self.headers,
        )
        return response

    def predict_online(self, params={}, files=None):
        if params is None and not isinstance(params, dict):
            raise ValueError("json_data must be a dict")
        response = requests.post(
            f"{self.service_endpoint}/predict_online",
            data=params,
            files=files
        )
        return response
