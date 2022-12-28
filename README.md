# Rarity Scanner

eth: **_0xbA842b7DA417Ba762D75e8F99e11c2980a8F8051_**
ens: **_prathik.xyz_**

Aggregate metadata info on NFT collections

Accuracy on par w/ legitimate tools afaik (May now have changed with the release of OpenRarity)

#### description

Gathering info on collection, weighing rarities, and spitting into json file
_Currently supports collections on Ethereum and Cosmos_
_Currently supports on-chain metadata, single-file metadata, multi-file metadata_

#### how-to

##### sample

```py
import json
from pyshuii.retrievers import erc721, cw721

creds = {}
creds['ALCHEMY_API_KEY'] = ''

client_mappings = {
    'EVM': erc721,
    'CW': cw721
}

proxies = open('proxies.txt', 'r').read()


def main(event):
    try:
        if (event['network'] == 'EVM'):
            cli = client_mappings[event['network']](
                alchemy_api_key=creds.get('ALCHEMY_API_KEY'),
                max_retries=100,
                proxies=proxies
            )
        elif (event['network'] == 'CW'):
            cli = client_mappings[event['network']](
                max_retries=100,
                proxies=proxies
            )

        results = cli.run(event['chain'], event['address'])

        with open("%s.json" % (results['project_name'].lower().replace(" ", "_")), "w") as dumped:
            dumped.write(json.dumps(results))

        return '{}s'.format(results['time_to_sync'])
    except Exception as e:
        print(e)
        raise e

# main(
#     event={
#         "network": "CW",
#         "chain": "JUNO-1",
#         "address": "juno1za0uemnhzwkjrqwguy34w45mqdlzfm9hl4s5gp5jtc0e4xvkrwjs6s2rt4"
#     })
# main(
#     event={
#         "network": "CW",
#         "chain": "JUNO-1",
#         "address": "juno1e229el8t4lu4rx7xeekc77zspxa2gz732ld0e6a5q0sr0l3gm78stuvc5g"
#     })
# main(
#     event={
#         "network": "CW",
#         "chain": "STARGAZE-1",
#         "address": "stars1rz8jkes33jxqf79t707s68yary3969faqfz59lvwnxjy4j65q7es62j098"
#     })
main(
    event={
        "network": "EVM",
        "chain": "ETH",
        "address": "0x0e32cee0445413e118b14d02e0409303d338487a"
    })
```

### whats left

- _containerize_
  - poetry shell alternative
- improve efficiency
  - work around brute force retry method
  - CW single threaded
- more chains?
- better docs

```sh
python3 setup.py install
```

```sh
python3 -m twine upload --repository pypi dist/*
```

### to do

github workflow for package publishing & layer uploading
