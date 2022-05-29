import wikipedia
import requests
from requests.exceptions import HTTPError
import typing
import time
import json
# import ipdb # this is used for debugging in atom editor, ipdb=IPython-enabled Python Debugger


# from random_word import RandomWords
# str = '{"name": "Farid", "lastname":"Zaredar"}'
# python_object  = json.loads(str)

class InvertedIndex:

    counter:int = 1

    def downloadWords(self, url:str):
        listOfWordsByte:list = []
        listOfWordsString:list = []
        try:
            pass
            response = requests.get(url)
            response.encoding = 'utf-8'
            listOfWordsString = response.text.split('\n') #gives you in str format
            listOfWordsByte = response.content.splitlines() #gives you in byte format
            return listOfWordsString

        except HTTPError as http_error:
            print(f'[-] HTTP ERROR: {http_error}')
        except Exception as exception:
            print(f'[-] Exception: {exception}')
        else:
            print('successful')

    # didn't work, problem: module random_word not found, despite of using command: pip install random-word
    def randomWordGenerator(self):
        randomWords:list = []
        randomWord = RandomWords()
        randomWords = randomWord.get_random_word()
        # print(randomWords)

    def readWordsFromLocal(self):
        path = '/usr/share/dict/words'
        # method1
        # readWords = open(path, 'r')
        # for words in readWords:
        #     print(str(words))
        # method
        words = open(path).read().splitlines()
        return words

    def searchWikipedia(self, wordCollection:tuple):
        wordCollection1 = wordCollection[0]
        wordCollection2 = wordCollection[1]
        completeCollection:list = []
        completeCollection = wordCollection1.copy()
        # print(completeCollection)
        for index, words in enumerate(wordCollection1):
            # if index == 5:
            #     break
            try:
                result = wikipedia.search(words)
                for wordOrPharase in result:
                    completeCollection.append(wordOrPharase)
                    # print(wordOrPharase)
            except wikipedia.DisambiguationError as e:
                 availableOptions = e.options
                 print(availableOptions)
                 # time.sleep(2.5)
                 for eachOption in availableOptions:
                     completeCollection.append(eachOption)
            except Exception as e:
                print(f"[-] Exception is: {e}")

        print(completeCollection)
        return completeCollection

    def getWikipediaPage(self, wordCollection:list):
        documents:dict = {}
        listOfDocuments:list = []
        for index, wordsOrPharase in enumerate(wordCollection):
            try:
                documents:dict = {}
                # ipdb.set_trace() # breakPoint
                print(wordsOrPharase)

                # print(str(index))
                if index == 5: # it takes some hours, in order to reduce execution time decrese it to 10 or 5
                    break
                result = wikipedia.page(wordsOrPharase, auto_suggest=False)
                # print({f'doc-{str(self.counter)}': str(result.content)})
                # time.sleep(5.0)
                documents[f'doc-{str(self.counter)}'] = str(result.content)
                # documents.update({f'doc-{str(self.counter)}': str(result.content)})
                listOfDocuments.append(documents)
                self.counter += 1
                # print('here and counter :' + str(self.counter))
                # print(documents["doc" + str(self.counter)])

            except wikipedia.DisambiguationError as disambiguationError:
                availableOptions = disambiguationError.options
                for eachAvailable in availableOptions:
                    wordCollection.append(eachAvailable)
            except Exception as e:
                print(f'[-] Exception: {e}')
        return listOfDocuments

    def createInvertedIndex(self, listOfDocuments:list):
        invertedIndex:dict = {}
        counter:int = 1
        keyList:list = []

        for doc in listOfDocuments:

            docId = doc.keys()
            keyList = [key for key in docId]
            docId = keyList[0]
            content = doc[docId]
            tokens = content.split(" ")

            for token in tokens:
                if token not in invertedIndex.keys():
                    invertedIndex[token] = [docId]
                else:
                    invertedIndex[token].append(docId)


        for keys in invertedIndex:
            invertedIndex[keys] = list(set(invertedIndex[keys]))

        # print(invertedIndex)
        return invertedIndex

    def findDocs(self, invertedIndex:dict, query:list):
        foundDocs:dict = {}
        for eachQuery in query:
            try:
                if invertedIndex[eachQuery]:
                    # print('here')
                    foundDocs.update({eachQuery: invertedIndex[eachQuery]})
                    
            except Exception as e:
                print('[-] This element does not exist in inverted index\nMore Details: ' + str(e))
        return foundDocs

if __name__ =='__main__':
    ii = InvertedIndex()
    wordCollection1 = ii.downloadWords("https://www.mit.edu/~ecprice/wordlist.10000")
    print('here')
    wordCollection2 = ii.readWordsFromLocal()
    # the below function takes too much time to be processed if you want to skip it, you can comment it
    # completeCollection = ii.searchWikipedia((wordCollection1, wordCollection2))
    # if you need a complete collection you need to replace completeCollection instead of wordCollection1
    listOfDocuments = ii.getWikipediaPage(wordCollection1)
    invertedIndex = ii.createInvertedIndex(listOfDocuments)
    found  = ii.findDocs(invertedIndex, ['A', 'google'])
    print(found)
