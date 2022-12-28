import json
import asyncio
import aiohttp
import ssl
import certifi
import tqdm
import random

from pyshuii.clients import ProxyClient
from pyshuii.utils import traceCast


class MultiDocument(ProxyClient):
    def __init__(self, retry_limit, proxies=''):
        super().__init__(proxies)

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

    async def execute_jobs(self, fn, params):
        async with aiohttp.ClientSession(trust_env=True) as session:
            self.session = session
            await traceCast(
                desc="Execute jobs",
                fn=fn or MultiDocument.retrieve,
                tasks=[{
                    'session': self.session,
                    'ssl': self.SSL_CONTEXT,
                    'proxy': f'{random.choice(self.proxies)}' if self.proxies else None,
                    'job_id': job_id,
                    'job': job,
                    'retry_limit': self.retry_limit,
                    'results': self.results,
                    **params
                } for job_id, job in self.jobs.items()]
            )

            self.jobs = {}
            print("MultiDocument: Jobs have been executed")

    def clear_results(self):
        self.results = {}

    @staticmethod
    async def retrieve(session, ssl, proxy, job_id, job, retry_limit, results):
        error_message = None
        for attempt in range(retry_limit):
            try:
                # async with sem:
                async with session.get(job, ssl=ssl, proxy=proxy) as response:
                    if not response.status == 200:
                        raise Exception(
                            f"MultiDocument #{job_id}: [Status] {response.status}")

                    res = await response.read()
                    decoded_res = json.loads(res.decode("utf8"))
                    results[job_id] = decoded_res
                    return
            except Exception as e:
                error_message = e
                continue

        print(f'Error: MultiDocument: {job_id} - {job}:\n{error_message}')
