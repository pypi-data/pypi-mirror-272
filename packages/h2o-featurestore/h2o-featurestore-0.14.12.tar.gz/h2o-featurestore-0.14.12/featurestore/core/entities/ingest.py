import ai.h2o.featurestore.api.v1.CoreService_pb2 as pb
from featurestore.core import interactive_console

from ..retrieve_holder import RetrieveHolder
from ..utils import Utils
from .revert_ingest_job import RevertIngestJob


class Ingest:
    def __init__(self, stub, feature_set, ingest):
        self._stub = stub
        self._feature_set = feature_set
        self._ingest = ingest

    def retrieve(self):
        """Retrieve data.

        Returns:
            RetrieveHolder: Returns a link as output for reference.

        Typical example:
            fs.retrieve()
        """
        return RetrieveHolder(self._stub, self._feature_set, "", "", self._ingest.ingest_id)

    @interactive_console.record_stats
    def revert(self):
        """Revert to a specific ingest.

        Reverting creates a new minor version with the data corresponding to the specific ingest removed.

        Typical example:
            ingest.revert()

        For more details:
            https://docs.h2o.ai/feature-store/latest-stable/docs/api/ingest_history_api.html#reverting-ingestion
        """
        job = self.revert_async()
        return job.wait_for_result()

    def revert_async(self) -> RevertIngestJob:
        """Create a revert ingestion job for feature set.

        Returns:
            RevertIngestJob: A job for reverting ingestion.

            A job is created with a unique id and type Revert. For example:

            Job(id=<job_id>, type=Revert, done=False, childJobIds=[])

        Typical example:
            ingest.revert_async()

        Raises:
            Exception: Manual revert is not allowed on derived feature set.
        """
        if self._feature_set.derived_from.HasField("transformation"):
            raise Exception("Manual revert is not allowed on derived feature set")

        request = pb.StartRevertIngestJobRequest()
        request.feature_set.CopyFrom(self._feature_set)
        request.ingest_id = self._ingest.ingest_id
        job_id = self._stub.StartRevertIngestJob(request)
        return RevertIngestJob(self._stub, job_id)

    def __repr__(self):
        return Utils.pretty_print_proto(self._ingest)
