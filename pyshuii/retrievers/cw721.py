# CosmWasm721 Standard
import asyncio
import aiohttp
import ssl
import time

from functools import cmp_to_key

from pyshuii.clients import CosmWasmClient
from pyshuii.indexers import SingleDocument, MultiDocument

from pyshuii.retrievers.Main import Main


class cw721(Main):
    def __init__(self):
        super().__init__()

        self.client = None
        self.chain = None
        self.address = None

    async def count(self, token_id, metadata):
        metadata = metadata[token_id]
        token_id = metadata['edition'] or token_id
        attributes = metadata["attributes"]

        super().prep(token_id, attributes, self.weights, self.aggregate)

    # detect project name
    async def execute(self):
        start_time = time.time()
        collection_metadata = self.client.getCollectionMetadata(self.address)

        token_uri = collection_metadata['token_uri'].replace(
            "ipfs://", "https://gateway.ipfs.io/ipfs/")
        suffix = collection_metadata['suffix']

        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(url=collection_metadata['token_uri'], ssl=SSL_CONTEXT) as response:
                res = await response.read()
                metadata = json.loads(res.decode("utf8"))
                collection_metadata['total_supply'] = len(metadata)
                collection_metadata['name'] = ' '.join(
                    metadata[0]['name'].split(' ')[:-1])
                collection_metadata['symbol'] = ''.join(
                    s[0] for s in collection_metadata['name'].split(' '))

                print("--- COUNTING ---")
                await asyncio.gather(*[self.count(token_id) for token_id in range(collection_metadata['total_supply'])])

                for attributes in self.aggregate.values():
                    for attribute in attributes.values():
                        self.composed.append(attribute)

                print("--- WEIGHING ---")
                await asyncio.gather(*[super().assign_weight(attribute, collection_metadata['total_supply']) for attribute in self.composed])

                print("--- SORTING ---")
                self.weights.sort(key=cmp_to_key(self.compare), reverse=True)

                print("--- RANKING ---")
                self.rank()

        finalized_time = time.time() - start_time

        print("--- DONE ---")
        print("--- %s seconds ---" % (finalized_time))

        return {
            'network': chain.upper(),
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
        super().clear()

        self.client = CosmWasmClient(self.chain)
        self.chain = chain
        self.address = address

        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(
            self.execute())
        loop.close()
        return result


#run('juno1e229el8t4lu4rx7xeekc77zspxa2gz732ld0e6a5q0sr0l3gm78stuvc5g', 'juno-1')
#print("INVALIDS:", invalids)
