import collections
from Bio import Entrez
import xmltodict

def getArticle():
    Entrez.api_key = "8b156363bf8c0f48cb00a46181f25de5d508"
    Entrez.email = "ofhasirci@gmail.com"

    search_handle = Entrez.esearch(db="pubmed", term="amygdala", retmax=10)
    record = Entrez.read(search_handle)
    search_handle.close()
    # print(record)
    idList = record['IdList']

    for i in range(0, len(idList)):
        article_handle = Entrez.efetch(db="pubmed", id=idList[i], retmode='xml', rettype='abstract', retmax=100)
        articles_xml = article_handle.read()
        articles = xmltodict.parse(articles_xml)
        article = articles.get('PubmedArticleSet').get('PubmedArticle')
        article_handle.close()

        pmid = article.get('MedlineCitation').get('PMID').get('#text')
        title = article.get('MedlineCitation').get('Article').get('ArticleTitle')
        abs_dict = article.get('MedlineCitation').get('Article').get('Abstract')
        abstract = ''
        if abs_dict:
            abstract_text = abs_dict.get('AbstractText')
            if abstract_text:
                if type(abstract_text) is str:
                    abstract = abstract_text
                elif type(abstract_text) is list:
                    for item in abstract_text:
                        if type(item) is str:
                            abstract += item + '\n'
                        elif item.get('@Label') and item.get('#text'):
                            abstract += item.get('@Label') + ': ' + item.get('#text') + '\n'
                        elif item.get('#text'):
                            abstract += item.get('#text') + '\n'
                        else:
                            pass
                elif type(abstract_text) is collections.OrderedDict:
                    abstract += abstract_text.get('#text')
        
        author_list = []
        authors = article.get('MedlineCitation').get('Article').get('AuthorList')
        if authors:
            for item in authors.get('Author'):
                try:  
                    author = item.get('LastName') + " " + item.get('ForeName')
                    author_list.append(author)
                except AttributeError:
                    pass
        
        keyword_list = []
        keywords = article.get('MedlineCitation').get('KeywordList')
        if keywords:
            for item in keywords.get('Keyword'):
                if item.get('#text'):
                    keyword_list.append(item.get('#text'))
                elif type(item) is str:
                    keyword_list.append(item)
                else:
                    pass
        
        print("---------------")
        print(pmid)
        print(title)
        print(abstract)
        print(author_list)
        print(keyword_list)
        print("---------------\n")


getArticle()