# CosmWasm721 Standard
import asyncio
import aiohttp
import ssl
import time
import json
import requests

from functools import cmp_to_key

from pyshuii.clients import CosmWasmClient
from pyshuii.indexers import SingleDocument, MultiDocument
from pyshuii.utils import traceCast

from pyshuii.retrievers.Main import Main


class cw721(Main):
    def __init__(self, max_retries=500, proxies=''):
        super().__init__()

        self.client = None
        self.chain = None
        self.address = None
        self.proxies = proxies

    async def count(self, token_id, metadata):
        metadata = metadata[token_id]
        token_id = metadata['edition'] or token_id
        attributes = metadata["attributes"]

        await self.prep(token_id, attributes)

    async def execute(self):
        indexer = None
        start_time = time.time()
        collection_metadata = self.client.getCollectionMetadata(self.address)

        token_uri = None
        file_name = None
        suffix = collection_metadata['suffix'] or ''
        if collection_metadata['token_uri']:
            token_uri = collection_metadata.replace(
                "ipfs://", "https://gateway.ipfs.io/ipfs/")

        token_uri = 'https://hopegalaxy.mypinata.cloud/ipfs/QmTxetzZAqvhFrVVf1wQBx8hFrE8AnN85G5WvB489d81wV'

        document_type = 'MULTI'
        if token_uri:
            resp = requests.get(token_uri)
            if f'_metadata{suffix}' in resp.text:
                file_name = '_metadata'
            elif f'metadata{suffix}' in resp.text:
                file_name = 'metadata'

        if file_name:
            document_type = 'SINGLE'

        # if doc type single, get file name
        if document_type == "SINGLE":
            indexer = SingleDocument(f'{token_uri}/{file_name}{suffix}')
            await traceCast(
                desc="Initialize Jobs",
                fn=indexer.create_jobs,
                tasks=[{
                    'job': token_id
                } for token_id in range(collection_metadata['total_supply'])]
            )
            await indexer.execute_jobs(fn=None)
        elif document_type == "MULTI":
            if token_uri:
                indexer = MultiDocument(retry_limit=100, proxies=self.proxies)
                await traceCast(
                    desc="Initialize Jobs",
                    fn=indexer.create_jobs,
                    tasks=[{
                        "job_id": token_id,
                        'job': "%s/%s%s" % (token_uri, token_id, suffix)
                    } for token_id in range(
                        collection_metadata['starting_index'],
                        collection_metadata['starting_index'] +
                        collection_metadata['total_supply']
                    )]
                )
                await indexer.execute_jobs(fn=None)
            else:  # on chain
                indexer = MultiDocument(retry_limit=100, proxies=self.proxies)
                await traceCast(
                    desc="Initialize Jobs",
                    fn=indexer.create_jobs,
                    tasks=[{
                        "job_id": token_id,
                        'job': "%s/%s%s" % (token_uri, token_id, suffix)
                    } for token_id in range(collection_metadata['starting_index'], collection_metadata['starting_index'] + collection_metadata['total_supply'])]
                )
                await indexer.execute_jobs(fn=on_chain)

        # if doc type multi, if token uri query
        # if doc type multi, if not token uri

        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(url=collection_metadata['token_uri'], ssl=SSL_CONTEXT) as response:
                res = await response.read()
                metadata = json.loads(res.decode("utf8"))
                collection_metadata['total_supply'] = len(metadata)
                collection_metadata['name'] = ' '.join(
                    metadata[0]['name'].split(' ')[:-1])
                collection_metadata['symbol'] = ''.join(
                    s[0] for s in collection_metadata['name'].split(' '))

                print("*** COUNTING ***")
                await asyncio.gather(*[self.count(token_id) for token_id in range(collection_metadata['total_supply'])])

                for attributes in self.aggregate.values():
                    for attribute in attributes.values():
                        self.composed.append(attribute)

                print("*** WEIGHING ***")
                await asyncio.gather(*[super().assign_weight(attribute, collection_metadata['total_supply']) for attribute in self.composed])

                print("*** SORTING ***")
                self.weights.sort(key=cmp_to_key(self.compare), reverse=True)

                print("*** RANKING ***")
                self.rank()

        finalized_time = time.time() - start_time

        print("*** DONE ***")
        print("*** %s seconds ***" % (finalized_time))

        return {
            'network': self.chain.upper(),
            'address': collection_metadata['address'],
            'project_name': collection_metadata['name'],
            'project_symbol': collection_metadata['symbol'],
            'token_uri': collection_metadata['token_uri'],
            'total_supply': collection_metadata['total_supply'],
            'suffix': collection_metadata['suffix'],
            'starting_index': collection_metadata['starting_index'],
            'time_to_sync': finalized_time,
            'aggregate': self.aggregate,
            'weights': self.weights,
        }

    def run(self, chain, address):
        super().refresh()
        self.client = CosmWasmClient(chain)
        self.chain = chain
        self.address = address

        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(self.execute())
        loop.close()
        return result


# run('juno1e229el8t4lu4rx7xeekc77zspxa2gz732ld0e6a5q0sr0l3gm78stuvc5g', 'juno-1')
# print("INVALIDS:", invalids)
"""
juno1za0uemnhzwkjrqwguy34w45mqdlzfm9hl4s5gp5jtc0e4xvkrwjs6s2rt4

"""
