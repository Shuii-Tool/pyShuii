import json
import argparse

parser = argparse.ArgumentParser(description='Rarity retriever')
parser.add_argument('--name', action="store",
                    dest='collection_name', default='')
parser.add_argument('--tokenid', action="store",
                    dest='token_id', default=0)
args = parser.parse_args()


def main(project_name, tokenId):
    f = json.load(open('%s.json' % (project_name)))
    for rank in range(len(f['weights'])):
        if f["weights"][rank]["tokenId"] == tokenId:
            return rank, f["weights"][rank]


print(main(args.collection_name, int(args.token_id)))
#print(main("blankface", 3535))
