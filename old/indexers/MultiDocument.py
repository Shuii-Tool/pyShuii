import json
import asyncio
import aiohttp
import ssl
import certifi


class MultiDocument:
    def __init__(self, retry_limit, proxies):
        self.proxies = proxies
        self.SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
        self.jobs = {}
        self.session = None
        self.results = {}
        self.retry_limit = retry_limit

    async def create_job(self, job_id, job):
        self.jobs[job_id] = job

    def modify_job(self, job_id, job):
        if not job_id in self.jobs:
            raise Exception("MultiDocument: Invalid job_id")

        self.jobs[job_id] = job

    async def execute_jobs(self):
        async with aiohttp.ClientSession(trust_env=True) as session:
            self.session = session
            await asyncio.gather(*[
                MultiDocument.retrieve(
                    session=self.session,
                    ssl=self.SSL_CONTEXT,
                    job_id=job_id,
                    job=self.jobs[job_id],
                    retry_limit=self.retry_limit,
                    results=self.results
                ) for job_id in self.jobs]
            )
            self.jobs = {}
            print("MultiDocument: Jobs have been executed")

    def clear_results(self):
        self.results = {}

    @staticmethod
    async def retrieve(session, ssl, job_id, job, retry_limit, results):
        for _ in range(retry_limit):
            try:
                async with session.get(job, ssl=ssl, proxy="http://user-sp32149926:1sio17IeU0AI2soX@gate.smartproxy.com:7000") as response:
                    if not response.status == 200:
                        raise Exception("Failed")

                    res = await response.read()
                    decoded_res = json.loads(res.decode("utf8"))
                    results[job_id] = decoded_res
                    return
            except:
                continue

        print(f'MultiDocument: {job_id} - {job}')
