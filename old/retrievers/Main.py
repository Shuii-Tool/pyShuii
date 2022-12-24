class Main:
    def __init__(self):
        self.weights = []
        self.aggregate = {}
        self.invalids = []
        self.composed = []

    def refresh(self):
        self.weights = []
        self.aggregate = {}
        self.invalids = []
        self.composed = []

    def weigh(self, metadata):
        if "weight" in metadata.keys():
            return metadata["weight"]

        weight = 0
        for attribute in metadata["attributes"]:
            weight += self.aggregate[
                attribute["trait_type"]
            ][attribute["value"]]["weight"]

        metadata["weight"] = weight
        return weight

    def compare(self, a, b):
        return self.weigh(a) - self.weigh(b)

    def rank(self):
        unique_rank = current_rank = 1
        prev_weight = 1, self.weights[0]['weight']
        for weightIndex in range(len(self.weights)):
            if self.weights[weightIndex]['weight'] != prev_weight:
                prev_weight = self.weights[weightIndex]['weight']
                current_rank += 1

            self.weights[weightIndex]['rank'] = current_rank
            self.weights[weightIndex]['unique_rank'] = unique_rank

            unique_rank += 1

    @staticmethod
    async def assign(attribute, limit):
        attribute["weight"] = round(1 / (attribute["count"] / limit), 3)

    @staticmethod
    async def count(token_id, attributes, weights, aggregate):
        attributes.append({
            'trait_type': 'num_traits',
            'value': len([attrib for attrib in attributes if attrib['value']])
        })

        weights.append({
            "token_id": token_id,
            "attributes": attributes
        })

        for i in attributes:
            if not i["trait_type"] in aggregate:
                aggregate[i["trait_type"]] = {}

            if not i["value"] in aggregate[i["trait_type"]]:
                aggregate[i["trait_type"]][i["value"]] = {
                    "count": 0,
                    "weight": 0
                }

            aggregate[i["trait_type"]][i["value"]]["count"] += 1
