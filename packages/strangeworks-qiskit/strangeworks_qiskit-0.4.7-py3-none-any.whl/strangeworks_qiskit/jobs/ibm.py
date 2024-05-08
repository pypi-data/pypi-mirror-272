"""ibm.py."""

from qiskit.providers import BackendV1 as Backend
from qiskit.result import Result
from strangeworks.sw_client import SWClient as SDKClient
from strangeworks_core.types.job import Job
from strangeworks_core.types.job import Status as JobStatus


IBM_QUANTUM_PRODUCT_SLUG = "ibm-quantum"
IBM_QUANTUM_RESULT_FILENAME = "job_results.json"


def submit(
    sdk_client: SDKClient,
    circuit,
    backend: Backend,
    **kwargs,
) -> Job:
    """Submit job requests to the ibm service.

    Parameters
    ----------
    sdk_client: SDKClient
        client to make requests to the Strangeworks platform.
    circuit:
        circuit which will be run
    backend: Backend
        the backend which will run the circuit

    Returns
    -------
    : Job
        Job object with information about the request.

    """
    circuit_type = type(circuit).__name__
    payload = {
        "qobj_dict": circuit.to_dict(),
        "circuit_type": circuit_type,
        "backend_name": backend().name(),
    }
    payload.update(kwargs)
    raw_result = sdk_client.execute_post(
        product_slug=IBM_QUANTUM_PRODUCT_SLUG,
        payload=payload,
        endpoint="create_job",
    )
    sw_job = Job(**raw_result)
    return sw_job


def status(sdk_client: SDKClient, job_slug: str) -> Job:
    """Retrieve job status.

    Parameters
    ----------
    sdk_client: SDKClient
        client to make requests to the Strangeworks platform.
    job_slug: str
        used to identify a job record.

    Returns
    -------
    : Job
        Job object corresponding to the job slug with updated status info.
    """
    raw_result = sdk_client.execute_post(
        product_slug=IBM_QUANTUM_PRODUCT_SLUG,
        payload={"slug": job_slug},
        endpoint="get_job_status",
    )
    sw_job = Job(**raw_result)
    return sw_job


def result(sdk_client: SDKClient, job_slug: str) -> Result | None:
    """Return job results.

    Job must be in COMPLETED state before results can be retrieved.

    Parameters
    ----------
    sdk_client: SDKClient
        client to make requests to the Strangeworks platform.
    job_slug: str
        used to identify a job record.

    Returns
    -------
    : Result | None
        result object populated with job result or None if result file cannot be found
        or job status is not COMPLETED

    """
    raw_result = sdk_client.execute_post(
        product_slug=IBM_QUANTUM_PRODUCT_SLUG,
        payload={"slug": job_slug},
        endpoint="get_job_results",
    )
    sw_job = Job(**raw_result)
    if sw_job.status == JobStatus.COMPLETED:
        for f in sw_job.files:
            if f.file.file_name == IBM_QUANTUM_RESULT_FILENAME:
                raw_result_data = sdk_client.download_job_files([f.file.url])
                return Result.from_dict(raw_result_data[0])

    return None
