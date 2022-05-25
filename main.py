import wikipedia
import requests
from requests.exceptions import HTTPError
import typing
import time
import json
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
        for words in wordCollection1:
            try:
                result = wikipedia.search(words)
                for wordOrPharase in result:
                    completeCollection.append(wordOrPharase)
                    # print(wordOrPharase)
            except wikipedia.DisambiguationError as e:
                 availableOptions = e.options
                 print(availableOptions)
                 time.sleep(2.5)
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
                # print(wordsOrPharase)
                # print(str(index))
                if index == 5:
                    break
                result = wikipedia.page(wordsOrPharase, auto_suggest=False)
                # print({f'doc-{str(self.counter)}': str(result.content)})
                # time.sleep(5.0)
                documents[f'doc-{str(self.counter)}'] = str(result.content)
                # documents.update({f'doc-{str(self.counter)}': str(result.content)})
                listOfDocuments.append(documents)
                self.counter += 1
                print(self)
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

        for doc in listOfDocuments:
            print(doc)
            print()
            print(len(doc))
            docId = doc.keys()
            print(docId)
            # docId = docId[0]
            # print(docId)
            time.sleep(10.0)
            content = doc[docId]
            tokens = content.split(" ")
            for token in tokens:
                if token not in invertedIndex.keys():
                    invertedIndex[token] = [docId]
                else:
                    invertedIndex[token].append(docId)

        print(invertedIndex)

if __name__ =='__main__':
    ii = InvertedIndex()
    wordCollection1 = ii.downloadWords("https://www.mit.edu/~ecprice/wordlist.10000")
    wordCollection2 = ii.readWordsFromLocal()
    # completeCollection = ii.searchWikipedia((wordCollection1, wordCollection2))
    listOfDocuments = ii.getWikipediaPage(wordCollection1)
    print(len(listOfDocuments[0]))
    # ii.createInvertedIndex(listOfDocuments)
