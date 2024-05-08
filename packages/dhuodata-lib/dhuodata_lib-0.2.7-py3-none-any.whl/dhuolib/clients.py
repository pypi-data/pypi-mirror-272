from pydantic import ValidationError
import json
from dhuolib.config import logger
from dhuolib.services import ServiceAPIML
from dhuolib.validations import ExperimentBody, RunExperimentBody, PredictModelBody


class DhuolibClient:
    def __init__(self, service_endpoint=None):
        if not service_endpoint:
            raise ValueError("service_endpoint is required")

        self.service = ServiceAPIML(service_endpoint)

    def create_experiment(self, experiment_params: dict) -> dict:
        files = {}
        response = None
        try:
            ExperimentBody.parse_obj(experiment_params)
            experiment_params["experiment_tags"] = json.dumps(
                experiment_params["experiment_tags"]
            )
            if "requirements_file" in experiment_params.keys() and "model_pkl_file" in experiment_params.keys() :
                try:
                    files = {
                        "requirements_file": (
                            "requirements.txt",
                            open(experiment_params["requirements_file"], "rb"),
                            "text/plain",
                        ),
                        "model_pkl_file": (
                            "model.pkl",
                            open(experiment_params["model_pkl_file"], "rb"),
                            "application/octet-stream",
                        ),
                    }
                except FileNotFoundError as e:
                    logger.error(f"Error: {e}")
                    return {"error": str(e)}

                response = self.service.create_experiment_by_conf_json(
                    experiment_params=experiment_params, files=files
                )
            else:
                response = self.service.create_experiment_by_conf_json(
                    experiment_params=experiment_params
                )

            experiment = response.json()
            logger.info(
                f"Experiment Name: {experiment_params['experiment_name']}"
                f"Experiment ID: {experiment['experiment_id']} created"
            )
            return experiment
        except ValidationError as e:
            logger.error(f"Error: {e}")
            return {"error": str(e)}

    def run_experiment(self, run_params) -> dict:
        files = {}
        try:
            RunExperimentBody.parse_obj(run_params)
            
            try:
                files = {
                    "requirements_file": (
                        "requirements.txt",
                        open(run_params["requirements_file"], "rb"),
                        "text/plain",
                    ),
                    "model_pkl_file": (
                        "model.pkl",
                        open(run_params["model_pkl_file"], "rb"),
                        "application/octet-stream",
                    ),
                }
            except FileNotFoundError as e:
                logger.error(f"Error: {e}")
                return {"error": str(e)}
            
            if run_params["experiment_id"] is None:
                experiment_id = self.create_experiment(
                    run_params=run_params)
                run_params["experiment_id"] = experiment_id

            response = self.service.run_experiment(run_params=run_params, files=files)
            logger.info(f"Experiment ID: {run_params['experiment_id']} running")
            return response.json()
        except ValidationError as e:
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
        files = {}
        try:
            PredictModelBody.parse_obj(run_params)
            
            try:
                files = {
                    "data": (
                        "data_predict.csv",
                        open(run_params["data"], "rb"),
                        "csv",
                    )
                }
            except FileNotFoundError as e:
                logger.error(f"Error: {e}")
                return {"error": str(e)}
        
            response = self.service.predict_online(run_params=run_params, files=files)
            logger.info(f"Model Name: {run_params['modelname']} predictions")
            return response.json()
        
        except ValidationError as e:
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
