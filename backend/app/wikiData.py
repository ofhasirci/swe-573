import requests

class WikiData:

    def __init__(self, id):
        wiki = requests.get('https://www.wikidata.org/w/api.php?action=wbgetentities&ids=' + id + '&languages=en&format=json')
        self.wikiData = wiki.json().get('entities').get(id)
    
    def getDescription(self):
        if self.wikiData.get('descriptions'):
            return self.wikiData.get('descriptions').get('en').get('value')
        else:
            return ""
    
    def getLabel(self):
        if self.wikiData.get('labels'):
            return self.wikiData.get('labels').get('en').get('value')
        else:
            return ""
    
    def getSentence(self):
        sentence = " "

        if self.wikiData.get('claims'):
            
            if self.wikiData.get('claims').get('P31'):
                for item in self.wikiData.get('claims').get('P31'):
                    id = item.get('mainsnak').get('datavalue').get('value').get('id')
                    data = WikiData(id)
                    sentence = sentence + " " + data.getDescription() + " " + data.getLabel()
            
            
            if self.wikiData.get('claims').get('P279'):
                for item in self.wikiData.get('claims').get('P279'):
                    id = item.get('mainsnak').get('datavalue').get('value').get('id')
                    data = WikiData(id)
                    sentence = sentence + " " + data.getDescription() + " " + data.getLabel()
            
            
            if self.wikiData.get('claims').get('P2579'):
                for item in self.wikiData.get('claims').get('P2579'):
                    id = item.get('mainsnak').get('datavalue').get('value').get('id')
                    data = WikiData(id)
                    sentence = sentence + " " + data.getDescription() + " " + data.getLabel()

            if self.wikiData.get('claims').get('P361'):
                for item in self.wikiData.get('claims').get('P361'):
                    id = item.get('mainsnak').get('datavalue').get('value').get('id')
                    data = WikiData(id)
                    sentence = sentence + " " + data.getDescription() + " " + data.getLabel()

        return sentence