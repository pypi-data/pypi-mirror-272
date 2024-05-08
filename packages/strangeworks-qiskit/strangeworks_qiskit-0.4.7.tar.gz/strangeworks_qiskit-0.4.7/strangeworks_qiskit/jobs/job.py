"""job.py."""

from typing import Optional

import strangeworks
from qiskit.providers import JobStatus
from qiskit.providers import JobV1 as Job
from qiskit.providers.jobstatus import JOB_FINAL_STATES
from qiskit.result import Result
from strangeworks.sw_client import SWClient as SDKClient
from strangeworks_core.types.job import Job as SWJob

from strangeworks_qiskit.jobs import ibm


sw_service_lookup: dict = {
    "ibm-quantum": {
        "submit": ibm.submit,
        "status": ibm.status,
        "result": ibm.result,
    }
}


class StrangeworksJob(Job):
    """Strangeworks implementation of a Qiskit Job."""

    def __init__(
        self, backend, circuit, remote, sdk_client: Optional[SDKClient] = None, **kwargs
    ):
        super().__init__(
            backend=backend,
            job_id=None,
            **kwargs,
        )
        self._remote: bool = remote
        self._circuit = circuit

        self._sdk_client = sdk_client or strangeworks.client

        if not self._remote:
            self._run_config = kwargs
        # we only need a resource, etc if the job is remote.
        if self._remote:
            # pick the first resource that matches backend product slug
            product_slug = backend.product_slug()
            if product_slug not in sw_service_lookup:
                raise NotImplementedError(
                    f"Unable to handle job requests for product {product_slug}. Please contact Strangeworks support."  # noqa
                )

            self._product_slug = backend.product_slug()
            self.service_methods = sw_service_lookup.get(self._product_slug)

        self._result = None
        self._status: JobStatus = None

    def status(self):
        """Return job status.

        Jobs run on local simulators will have a status in terminal state once they
        return from submit.

        Jobs running remotely will make a remote call to retrieve job status until it
        reaches a terminal state.
        """
        if self._remote and self._status not in JOB_FINAL_STATES:
            sw_job: SWJob = self.service_methods.get("status")(
                self._sdk_client, self._job_slug
            )

            self._status = JobStatus[sw_job.remote_status]

        return self._status

    def result(self) -> Result:
        """Obtain job result.

        Jobs run on local simulators will already have a terminal status and a result
        if they terminated with a status of DONE.

        If a job is running remotely, this method will block until it reaches a
        terminal state. If the job finishes with a status of DONE, its results will
        be retrieved.

        Job results stored as a part of the object once they are available.
        """
        if not self._result and self._remote:
            self.wait_for_final_state()
            if self._status == JobStatus.DONE:
                self._result = self.service_methods.get("result")(
                    self._sdk_client, self._job_slug
                )

        return self._result

    def submit(self, **kwargs):
        """Submit a job.

        The method will wait for a result for jobs running on local simulators. For jobs
        running remotely, the method will return once the job request has been accepted
        successfully.
        """
        if self._remote:
            return self._submit_remote(**kwargs)
        return self._submit_local(**kwargs)

    def cancel(self):
        """Cancel job.

        Only jobs that are running remotely can be cancelled.
        """
        # make sure we have _status set to something other than None to ensure job has
        # been submitted prior to this call.
        if self._remote and self._status:
            self._sdk_client.execute_post(
                product_slug=self._product_slug,
                payload={"slug": self._job_slug},
                endpoint="cancel_job",
            )

    def _submit_local(self, **kwargs):
        backend = self.backend()
        simulator = getattr(backend, "simulator", **self._run_config)
        if not simulator:
            self._status = JobStatus.ERROR
            return

        job = simulator.run(self._circuit, **self._run_config)
        self._result = job.result()
        self._status = JobStatus.ERROR
        if self._result:
            self._status = JobStatus.DONE
            self._job_id = job.job_id()

    def _submit_remote(self, **kwargs):
        sw_job: SWJob = self.service_methods.get("submit")(
            self._sdk_client, self._circuit, self.backend, **kwargs
        )
        self._job_slug = sw_job.slug
        self._job_id = sw_job.external_identifier
        self._status = JobStatus[sw_job.remote_status]
