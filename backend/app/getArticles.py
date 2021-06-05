import collections
from Bio import Entrez
import xmltodict
from app.models import Article
from django.db.utils import IntegrityError
from background_task import background

@background(schedule=5)
def getArticle(term):
    Entrez.api_key = "8b156363bf8c0f48cb00a46181f25de5d508"
    Entrez.email = "ofhasirci@gmail.com"

    search_handle = Entrez.esearch(db="pubmed", term=term, retmax=100000)
    record = Entrez.read(search_handle)
    search_handle.close()
    idList = record['IdList']

    saved_ids = list(Article.objects.values_list('PMID', flat=True).distinct())
    new_ids = list(set(idList) - set(saved_ids))

    article_counter = 0

    for i in range(0, len(new_ids)):
        article_handle = Entrez.efetch(db="pubmed", id=new_ids[i], retmode='xml', rettype='abstract', retmax=100)
        articles_xml = article_handle.read()
        articles = xmltodict.parse(articles_xml)
        article = articles.get('PubmedArticleSet').get('PubmedArticle')
        article_handle.close()

        try:
            pmid = article.get('MedlineCitation').get('PMID').get('#text')
        except AttributeError:
            pass

        try:
            title = article.get('MedlineCitation').get('Article').get('ArticleTitle')
        except AttributeError:
            pass
        
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
                    if item.get('Initials') and item.get('LastName'):
                        author = item.get('LastName') + " " + item.get('ForeName')
                        author_list.append(author)
                except AttributeError:
                    pass
        
        keyword_list = []
        keywords = article.get('MedlineCitation').get('KeywordList')
        if keywords:
            for item in keywords.get('Keyword'):
                try:
                    if item.get('#text'):
                        keyword_list.append(item.get('#text'))
                    elif type(item) is str:
                        keyword_list.append(item)
                    else:
                        pass
                except AttributeError:
                    pass

        article = Article(
            PMID=pmid,
            Title=title,
            Abstract=abstract,
            Authors=author_list,
            Keywords=keyword_list
        )

        try:
            article.save()
            article_counter += 1
            print("article count: " + str(article_counter))
        except IntegrityError:
            print('Inconsistent elements')
            pass
        # print("---------------")
        # print(pmid)
        # print(title)
        # print(abstract)
        # print(author_list)
        # print(keyword_list)
        # print("---------------\n")