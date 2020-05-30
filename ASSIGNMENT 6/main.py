import sys
from find_word_count import FindWordCount
from find_word_frequency import FindWordFrequency

def help():
    print("Proper usage of the program is:")
    print("python main.py <operation> <workercount> <filename> <word (for frequency operation)>")

if __name__ == '__main__':
    try:
        operation = sys.argv[1]
        if operation == 'COUNT':
            workerCount = sys.argv[2]
            try:
                workerCount = int(workerCount)
            except ValueError:
                print("Please enter an integer for worker count!")
                sys.exit()
            file = sys.argv[3]

            try:
                with open(file) as f:
                    pass
            except FileNotFoundError:
                print("Please enter a proper file!")
                sys.exit()

            fwc = FindWordCount(workerCount)
            fwc.start(file)


        elif operation == 'FREQ':
            workerCount = sys.argv[2]
            try:
                workerCount = int(workerCount)
            except ValueError:
                print("Please enter an integer for worker count!")
                sys.exit()

            fileName = sys.argv[3]
            try:
                with open(fileName) as f:
                    pass
            except:
                print("Please enter a proper file!")
                sys.exit()

            word = sys.argv[4]

            fwf = FindWordFrequency(workerCount)
            fwf.start(fileName,word)
            
        else:
            help()
            sys.exit()

    except IndexError:
        help()
        sys.exit()

