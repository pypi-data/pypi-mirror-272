from lotgi._openai import OpenAI

__all__ = [
    "OpenAI",
]


from lotgi.rest_client import RestClient
from lotgi.tokens import estimate_token_usage
from lotgi.logging import init_logging
from lotgi.models import rest

import click
from tabulate import tabulate
from datetime import timedelta
from typing import Optional
import sys
import requests
import datetime
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper
import os
import hashlib
import binascii


@click.group
def cli():
    """
    Lotgi CLI tool.
    """
    init_logging()


def format_duration(duration_s : int) -> str:
    total_hours = duration_s // (60 * 60)
    minutes = (duration_s // 60) % 60
    seconds = duration_s % 60
    if total_hours > 0:
        return f"{total_hours}h{minutes}m{seconds}s"
    return f"{minutes}m{seconds}s"

def format_execution_options(options) -> str:
    columns = {
        "Tradeoff": [
            option.option_name for option in options
        ],
        "Estimated Price": [
            f"${option.expected_cost:.2f}" for option in options
        ],
        "Estimated Duration (s)": [
            format_duration(option.expected_duration) for option in options
        ],
    }
    return tabulate(columns, headers="keys")

def get_tradeoff() -> str:
    while True:
        selection = input(f"Select a tradeoff ({repr(rest.EXECUTION_TRADEOFFS)}): ")
        if selection in rest.EXECUTION_TRADEOFFS:
            return selection
        else:
            print(f"Invalid tradeoff. Select from {rest.EXECUTION_TRADEOFFS}")

def upload_file(client : RestClient, filename : str, path : str):
    assert path.endswith(".jsonl"), f"The path must be to a jsonl file, not {path}"
    url = client.get_upload_url(filename)
    file_size = os.stat(path).st_size
    with open(path, "rb") as f:
        with tqdm(total=file_size, unit="B", unit_scale=True, unit_divisor=1024) as t:
            wrapped_file = CallbackIOWrapper(t.update, f, "read")
            requests.put(url, data=wrapped_file)

def sha256_file(f) -> str:
    """
    Return a string of the sha256 hash of a file. Do it in a streaming fashion to be memory efficient.
    """
    sha256 = hashlib.sha256()
    to_hash = f.read(2**20)
    while to_hash:
        sha256.update(to_hash)
        to_hash = f.read(2**20)
    return binascii.hexlify(sha256.digest()).decode()

@cli.command
@click.option("--model", required=True, help="The model to run inference with.")
@click.option("--input-file", required=False, help="The name of the file (uploaded with `lotgi upload`)to run inference on.")
@click.option("--input-path", required=False, help="The url or path to a file to run inference on.")
@click.option("--field", required=True, help="The field within a row containing the data.")
@click.option("--tradeoff", required=False, default=None, help=f"The tradeoff ({rest.EXECUTION_TRADEOFFS}).")
@click.option("--prompt", required=False, help="Prompt to use for inference. Leave empty if prompt is already included in the dataset.")
@click.option("--max-output-tokens", required=False, help="The maximum number of output tokens. [default=32]. Changing this value may affect the job cost.")
@click.option("--regex", required=False, help="Force the output to match a given regular expression.")
def submit(
        model : str,
        input_file : str,
        input_path : str, field : str,
        tradeoff : Optional[str],
        prompt: Optional[str],
        max_output_tokens : Optional[int],
        regex : Optional[str],
):
    """
    Submit a new batch inference job.

    Your job file is expected to be formatted as a jsonl file. Each line corresponds to a request and should be a json object. Use the `--field` argument to specify which field of the json object contains the text to complete.

    For example, if a file stored at `example.com/dataset.jsonl` contains the contents

    \b\n
    ```
    {"my_completion_text": "hello"}
    {"my_completion_text": "lorem"}
    ```

    You can run 
        `lotgi submit --model mistralai/Mistral-7B-Instruct-v0.2 
            --input-url example.com/dataset.jsonl 
            --field "my_completion_text" 
            --tradeoff Cheapest 
            --prompt "Summarize the following text"`. 
    
    This will run the mistral-7b model against the inputs "hello" and "lorem" with the provided prompt, optimizing for cost.
    """
    client = RestClient()

    # if tradeoff is None:
    #     print(f"Scanning job to estimate costs...")
    #     job_execution_options_input = estimate_token_usage(input_file=input_file, prompt="", model=model, field=field)
    #     options = client.job_exection_options(job_execution_options_input=job_execution_options_input)

    #     print(format_execution_options(options))
    #     tradeoff = get_tradeoff()

    if (not (input_file or input_path)) or (input_file and input_path):
        print("Must specify exactly one of --input-file or --input-path", file=sys.stderr)
        sys.exit(1)

    if input_path:
        with open(input_path, "rb") as f:
            input_file = "sha256:" + sha256_file(f)
        upload_file(client, input_file, input_path)

    result = client.submit_job(
        model=model,
        input_file=input_file,
        field=field,
        target_cost=-1,
        target_deadline=-1,
        execution_tradeoff=tradeoff,
        max_output_tokens=max_output_tokens,
        regex=regex,
    )
    print("Success!")
    print(result)


@cli.command
def list():
    """
    List your batch inferences jobs.
    """
    client = RestClient()
    jobs = sorted(client.list_jobs(), key=lambda job: job.submission_time, reverse=True)

    to_display = {
        "Job ID": [job.job_id for job in jobs],
        "Model": [job.model for job in jobs],
        "Status": [job.state for job in jobs],
        "Submission time": [datetime.datetime.fromtimestamp(job.submission_time).strftime('%Y-%m-%d %H:%M:%S') for job in jobs],
        "Tradeoff": [job.execution_tradeoff for job in jobs],
        "Field": [job.field for job in jobs],
        "Input": [job.input_file for job in jobs],
    }

    print(tabulate(to_display, headers="keys"))


@cli.command
@click.argument("job_id", required=True)
def get(job_id : str):
    """
    Get the results of a specific job.

    Job results are written to stdout. (Human readable text/errors are written to stderr).

    To store your job results, consider redirecting the job output to a file. `lotg get <job_id> > saved_job_results.jsonl`
    """
    client = RestClient()
    url = None
    try:
        url = client.get_job_results(job_id)
    except KeyError:
        print("Job not found!", file=sys.stderr, flush=True)
        sys.exit(1)
    assert url is not None

    result = requests.get(url)
    if not result.ok:
        print(f"Couldn't download result from {url}. {result.status_code} : {result.text}")
        sys.exit(1)

    print(result.text)

def upload_file(client : RestClient, filename : str, path : str):
    assert path.endswith(".jsonl"), f"The path must be to a jsonl file, not {path}"
    url = client.get_upload_url(filename)
    file_size = os.stat(path).st_size
    with open(path, "rb") as f:
        with tqdm(total=file_size, unit="B", unit_scale=True, unit_divisor=1024) as t:
            wrapped_file = CallbackIOWrapper(t.update, f, "read")
            requests.put(url, data=wrapped_file)


@cli.command
@click.argument("filename", required=True)
@click.argument("path", required=True)
def upload(filename : str, path : str):
    """
    Upload a dataset/file to be used for inference.

    Usage: lotgi upload <filename> <path>

    filename: The filename used to reference this file when running jobs.

    path: The path the file is currently stored at.
    """
    client = RestClient()
    upload_file(client, filename, path)

