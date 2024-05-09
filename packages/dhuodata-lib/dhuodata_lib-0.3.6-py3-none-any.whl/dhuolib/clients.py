from pydantic import ValidationError
import json
from dhuolib.config import logger
from dhuolib.services import ServiceAPIML
from dhuolib.validations import ExperimentBody, RunExperimentBody, PredictModelBody
from werkzeug.datastructures import FileStorage


class DhuolibClient:
    def __init__(self, service_endpoint=None):
        if not service_endpoint:
            raise ValueError("service_endpoint is required")

        self.service = ServiceAPIML(service_endpoint)

    def create_experiment(self, experiment_params: dict) -> dict:
        params = {}
        response = None

        try:
            ExperimentBody.parse_obj(experiment_params)
        except ValidationError as e:
            logger.error(f"Error: {e}")
            return {"error": str(e)}
        
        if "requirements_file" in experiment_params.keys() and "model_pkl_file" in experiment_params.keys():
            params["experiment_tags"] = json.dumps(
                experiment_params["experiment_tags"]
            )
            try:
                with open(experiment_params["requirements_file"], "rb") as f1, open(
                    experiment_params["model_pkl_file"], "rb"
                ) as f2:
                    params = {
                        "requirements_file": FileStorage(
                            stream=f1, filename="requirements.txt", content_type="text/plain"
                        ),
                        "model_pkl_file": FileStorage(
                            stream=f2,
                            filename="model.pkl",
                            content_type="application/octet-stream",
                        ),
                    }
                    params = {**params, **experiment_params}
    
                    response = self.service.create_experiment_by_conf_json(params)

                    experiment = response.json()
                    logger.info(
                        f"Experiment Name: {params['experiment_name']}"
                        f"Experiment ID: {experiment['experiment_id']} created"
                    )
                    return experiment
            except FileNotFoundError as e:
                logger.error(f"Error: {e}")
                return {"error": str(e)}
        params = {**params, **experiment_params}
        response = self.service.create_experiment_by_conf_json(params)
        experiment = response.json()
        logger.info(
            f"Experiment Name: {params['experiment_name']}"
            f"Experiment ID: {experiment['experiment_id']} created"
        )
        return experiment

    def run_experiment(self, params) -> dict:
        try:
            RunExperimentBody.parse_obj(params)
        except ValidationError as e:
            logger.error(f"Error: {e}")
            return {"error": str(e)}
        
        try:
            with open(params["requirements_file"], "rb") as f1, open(
                params["model_pkl_file"], "rb"
            ) as f2:
                files = {
                    "requirements_file": FileStorage(
                        stream=f1, filename="requirements.txt", content_type="text/plain"
                    ),
                    "model_pkl_file": FileStorage(
                        stream=f2,
                        filename="model.pkl",
                        content_type="application/octet-stream",
                    ),
                }
             
                if params["experiment_id"] is None:
                    experiment_id = self.create_experiment(params)
                    params["experiment_id"] = experiment_id

                response = self.service.run_experiment(params=params, files=files)
                logger.info(f"Experiment ID: {params['experiment_id']} running")
                return response.json()
        except FileNotFoundError as e:
            logger.error(f"Error: {e}")
            return {"error": str(e)}

    def create_model(self, model_params) -> dict:
        try:
            if model_params["stage"] is None:
                model_params["stage"] = "STAGING"

            response = self.service.create_model(model_params)
            logger.info(f"Model Name: {model_params['modelname']} created")
            return response.json()
        except ValidationError as e:
            logger.error(f"Error: {e}")
            return {"error": str(e)}

    def predict_online(self, run_params) -> dict:
        try:
            PredictModelBody.parse_obj(run_params)
        except ValidationError as e:
            logger.error(f"Error: {e}")
            return {"error": str(e)}
        try:
            with open(run_params["data"], "rb") as f1:
                files = {
                    "data": FileStorage(
                        stream=f1, filename="data.csv", content_type="csv"
                    )
                }
                response = self.service.predict_online(params=run_params, files=files)
                logger.info(f"Model Name: {run_params['modelname']} predictions")
                return response.json()
        except FileNotFoundError as e:
            logger.error(f"Error: {e}")
            return {"error": str(e)}

    def load_model(self, model_name, tag) -> str:
        print("loading model")
        return "model_name.pkl"

    def predict(self):
        pass

    def read_from_bucket(self, bucket: str, filename: str):
        # OCI, GCP, AWS
        return f"folder/{filename}"

    # def read_from_bucket(self, filename: str):
    #     default_bucket = "s3://default"
    #     return self.read_from_bucket(default_bucket, filename)

    def execute_select(self, statement: str):
        # Acesso pela API ML Service
        # Processo assíncrono
        file = "s3://bucket/temp/file1.csv"
        return file

    def execute_dml(self, statement: str):
        # rows_count - linhas afetadas

        rows_count = 0
        return rows_count

    # Promover o model_name para "production"

    # - [ ] criar cluster no Dataflow
    # - [ ] informar o dado de schedule e criação de aplicação Dataflow
    # - [ ] inserção de lista de dependencias: libs + zip + script.py

    # @hydra.main(config_path="config", config_name="deploy")
    def deploy(self, params):

        # Enfileira o serviços

        return None

    def save_predictions(
        self, dataset_predictions, inputs, predictions, model_name, tag
    ):

        return ""


if __name__ == "__main__":
    dhuolib = DhuolibClient()

    experiment = "classificacao para recomendação"
    experiment_id = dhuolib.create_experiment(experiment)

    file = "pickle.file"
    model_name = "model_decision_tree"
    tag = "1.0.1"

    save_status = dhuolib.save_model(experiment_id, file, model_name, tag)
    print(save_status)

    file = "pickle.file"
    model_name = "model_logistic"
    tag = "1.0.2"

    save_status = dhuolib.save_model(experiment_id, file, model_name, tag)
    print(save_status)

    file = dhuolib.load_model("model_decision_tree", "1.0.1")

    data_input = {"x": 1}
    predictions = dhuolib.predict("model_decision_tree", "1.0.1", data_input)

    dhuolib.deploy()
