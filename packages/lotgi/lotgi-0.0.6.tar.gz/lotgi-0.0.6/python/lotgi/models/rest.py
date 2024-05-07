from pydantic import BaseModel, Field, model_validator, Extra
from typing import Optional
import shortuuid

uuid_generator = shortuuid.ShortUUID(alphabet="abcdefghijklmnopqrstuvwxyz1234567890")

class ModalCredentials(BaseModel):
    token_id : str
    token_secret : str

class RunpodCredentials(BaseModel):
    api_key : str

class CloudCredentials(BaseModel):
    modal_credentials : Optional[ModalCredentials] = None
    runpod_credentials : Optional[RunpodCredentials] = None

    @model_validator(mode="after")
    def atleast_one_credential(self):
        if not (self.modal_credentials or self.runpod_credentials):
            raise ValueError("At least one set of credentials should be specified.")
        return self

EXECUTION_TRADEOFFS = {
    "Cheapest",
    "Hour",
}

DEFAULT_MAX_OUTPUT_TOKENS = 32
DEFAULT_REGEX = r".*"

class JobSpec(BaseModel):
    job_id : str = Field(default_factory=lambda : f"job-{uuid_generator.uuid()}")
    cloud_credentials : Optional[CloudCredentials] = None
    input_file : str
    target_cost : float
    target_deadline : int # Specified as a unix timestamp
    model : str
    field : str
    execution_tradeoff : str
    max_output_tokens : int = DEFAULT_MAX_OUTPUT_TOKENS
    regex : str = DEFAULT_REGEX
    huggingface_token : Optional[str] = None

    # @model_validator(mode="after")
    # def valid_execution_tradeoff(self):
    #     if self.execution_tradeoff not in EXECUTION_TRADEOFFS:
    #         raise ValueError(f"execution_tradeoff must be one off {EXECUTION_TRADEOFFS}")
    #     return self

class JobStatus(BaseModel, extra=Extra.allow):
    job_id : str
    state : str
    model : str
    submission_time : int
    execution_tradeoff : str
    input_file : str
    target_cost : float
    target_deadline : int # Specified as a unix timestamp
    field : str

class JobExecutionOptionsInput(BaseModel):
    input_token_count : int
    num_requests : int
    model : str
    max_output_tokens : int = 32

class JobExecutionTradeoffOption(BaseModel):
    option_name : str
    expected_cost : float
    expected_duration : int # In seconds

class MetricInput(BaseModel):
    job_id: str
    metric_name: str
    metric_value: float

