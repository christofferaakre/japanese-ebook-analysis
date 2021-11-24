import MeCab

class MecabNode:
    def __init__(self, string):
        surface = string.split("\t")[0]
        features = string.split("\t")[1].split(",")

        self.surface = surface
        self.pos = ".".join(features[:4]).replace(".*","")
        self.inflection_group = features[4].replace("*","")
        self.inflection_type = features[5].replace("*","")
        self.base_form = features[6].replace("*","")
        self.reading = features[7].replace("*","")
        self.pronunciation = features[8].replace("*","")

    def __repr__(self):
        return f'{self.surface},{self.pos},{self.inflection_group},{self.inflection_type},{self.base_form},{self.reading},{self.pronunciation}'
