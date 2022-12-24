# EthereumRC721 Standard
import asyncio
import time

from functools import cmp_to_key

from pyshuii.clients import EthereumClient
from pyshuii.indexers import MultiDocument

from pyshuii.retrievers.Main import Main


class erc721(Main):
    def __init__(self, alchemy_api_key, max_retries=500, proxies=[]):
        super().__init__()

        self.client = EthereumClient(alchemy_api_key)
        self.indexer = MultiDocument(max_retries, proxies)
        self.address = None

    async def count(self, token_id, metadata):
        attributes = metadata["attributes"]

        super().count(token_id, attributes, self.weights, self.aggregate)

    async def execute(self):
        start_time = time.time()
        collection_metadata = self.client.getCollectionMetadata(self.address)

        token_uri = collection_metadata['token_uri'].replace(
            "ipfs://", "https://gateway.ipfs.io/ipfs/")
        suffix = collection_metadata['suffix']

        print("*** GATHER ***")
        await asyncio.gather(*[self.indexer.create_job(token_id, "%s/%s%s" % (token_uri, token_id, suffix)) for token_id in range(collection_metadata['starting_index'], collection_metadata['starting_index'] + collection_metadata['total_supply'])])
        await self.indexer.execute_jobs()

        print("*** COUNTING ***")
        await asyncio.gather(*[self.count(token_id, self.indexer.results[token_id]) for token_id in self.indexer.results])

        for attributes in self.aggregate.values():
            for attribute in attributes.values():
                self.composed.append(attribute)

        print("*** WEIGHING ***")
        await asyncio.gather(*[super().assign(attribute, collection_metadata['total_supply']) for attribute in self.composed])

        print("*** SORTING ***")
        self.weights.sort(key=cmp_to_key(self.compare), reverse=True)

        print("*** RANKING ***")
        self.rank()

        finish_time = time.time()
        finalized_time = finish_time - start_time

        print("*** DONE ***")
        print("*** %s seconds ***" % (finalized_time))

        return {
            'network': "ETH",
            'address': collection_metadata['address'],
            'project_name': collection_metadata['name'],
            'project_symbol': collection_metadata['symbol'],
            'token_uri': token_uri,
            'total_supply': collection_metadata['total_supply'],
            'suffix': collection_metadata['suffix'],
            'starting_index': collection_metadata['starting_index'],
            'time_started': start_time,
            'time_finalized': finish_time,
            'time_to_sync': finalized_time,
            'aggregate': self.aggregate,
            'weights': self.weights,
        }

    def run(self, chain, address):
        super().refresh()

        self.indexer.clear_results()
        self.address = address

        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(self.execute())
        loop.close()

        return result
