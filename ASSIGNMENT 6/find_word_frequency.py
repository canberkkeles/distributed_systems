from map_reduce import MapReduce
import string

def removePunctuation(word):
    punctuations = string.punctuation
    result = ""
    for ch in word:
        if ch not in punctuations and (ch != '\n' and ch != '\t'):
            result += ch
    return result

class FindWordFrequency(MapReduce):
    def __init__(self,numWorker):
        super().__init__(numWorker)
    
    def Map(self,map_input):
        
        fileName = map_input['filename']
        start = map_input['startno']
        end = map_input['endno']
        kw = map_input['keyword']

        result = dict()
        with open(fileName) as f:
            for i,line in enumerate(f):
                if i >= start and i<=end:
                    line.strip()
                    line.rstrip()
                    upperLine = line.upper()
                    words = upperLine.split(" ")
                    for word in words: # ITERATE OVER THE WORDS IN LINE
                        cleanWord = removePunctuation(word)
                        if cleanWord not in result and cleanWord == kw.upper(): # CASE INSENSITIVE
                            result[word] = [1]
                        elif cleanWord in result and cleanWord == kw.upper(): # CASE INSENSITIVE
                            result[word].append(1)
        return result

    def Reduce(self,reduce_input):

        wordCount = 0
        for key in reduce_input:
            wordArray = reduce_input[key]
            for element in wordArray:
                wordCount += element
        return wordCount
