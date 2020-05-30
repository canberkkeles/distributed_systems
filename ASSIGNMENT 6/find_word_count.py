from map_reduce import MapReduce

class FindWordCount(MapReduce):
    def __init__(self,numWorker):
        super().__init__(numWorker)
    
    def Map(self,map_input):

        fileName = map_input['filename']
        start = map_input['startno']
        end = map_input['endno']

        result = dict()
        with open(fileName) as f:
            for i,line in enumerate(f):
                if i >= start and i<=end:
                    line.strip()
                    words = line.split(" ")
                    for word in words: # ITERATE OVER THE WORDS IN LINE
                        if word not in result:
                            result[word] = [1]
                        elif word in result:
                            result[word].append(1)
        return result


    def Reduce(self,reduce_input):
        wordCount = 0
        for key in reduce_input:
            wordArray = reduce_input[key]
            for element in wordArray:
                wordCount += element
        return wordCount


        
