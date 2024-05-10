import os


class SlurmJob:
    def __init__(self, nodelist: str | None) -> None:
        self.id: str | None = None
        self.nodelist_raw = nodelist
        self._parse_nodelist()

    def load_from_env(self):
        self.id = SlurmJob.get_id()
        self.nodelist_raw = os.environ.get("SLURM_JOB_NODELIST")
        self._parse_nodelist()

    def _parse_nodelist(self):
        if self.nodelist_raw:
            pass

    @staticmethod
    def get_id() -> str | None:
        return os.environ.get("SLURM_JOBID")
