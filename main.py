import os
import docx

# this is the list of indicators to look for in files
# the order matters, the first in the list is the highest priority
indicators = ["shall", "should", "will", "could"]

# this checks if the inputted sentence has one of the indicators declared above
# returns true if it does, and false if it does not
def check (sentence):
    for indicator in indicators:
        if sentence.lower().count(indicator.lower()) != 0:
            return True

    return False

# splits a sentence at a period, inputs are a sentence and it has no outputs
def Split_at_period (line):
    # some declarations
    lines = []
    sentence = ""
    prev_sentence = ""
    nums = "0123456789"
    out = False

    # iterating through the sentence
    for i in range(len(line)):
        # if the charcter in the sentence is a period
        if line[i] == '.':
            # if it is not the end of the sentence
            if i + 1 < len(line):
                # if the period is followed by a number
                if nums.count(line[i+1]) == 0:
                    # checks if sentence current sentence made from components
                    # of the inputted sentence has an indicator
                    out = check(sentence)

                    # house keeping
                    prev_sentence = sentence
                    sentence = ""

            else:
                # if it is the end of the sentence
                # checks if sentence current sentence made from components
                # of the inputted sentence has an indicator
                out = check(sentence)

                # house keeping
                prev_sentence = sentence
                sentence = ""

            # if an idicator was present in the sub sentence
            if out:
                # adding the sub sentence that was previous assigned to prev_sentence
                # to the list
                lines.append(prev_sentence.strip())
                
                # house keeping
                out = False
                sentence = ""
                continue

            continue
        
        # adding a character from the main sentence to the sub sentence
        sentence+=line[i]
        #print("- sentence after iteration: ", sentence)

    return lines


# makes a text file withe the same core name as the source word doc but changes .docx to .txt
def write_action_verd_sent_to_file(filename):
    # informin the user
    print("opening this file: ", filename)
    
    # turning the word doc into an object
    doc = docx.Document(filename)

    # creating a name for the new text file by replacing the extension
    filename = filename.replace(".docx", ".txt")
    # and replacing spaces in the name with underscores
    filename = filename.replace(" ", "_")

    # opening the text file
    f = open(filename, 'w')

    # iterating through the paragraphs in the word doc
    for para in doc.paragraphs:
        # splitting the paragraph into sentences that contain the indicators
        # then writing them to the text file
        for i in Split_at_period(para.text):
            f.write(i + "\n")

    f.close()

    # sorting the lines in the file by what indicator they contain, highest priority is
    # put towards the beginning of the file and vice versa
    sort_file_with_indicators(filename)

# sorts a file based on the priority of the indicators present within each line
# the highest priority indicator is sorted towards the top of the file
def sort_file_with_indicators(file_name):
    # list that will hold the lines that will be written back to the text file adter sorting
    new_lines = []

    # reading the lines from the file
    f = open(file_name, 'r')
    lines = f.readlines()
    f.close()

    # iterating through the indicators declared at the top of the file, making a section for each
    # in the text file
    for indicator in indicators:
        # creating an element in the list that represents the section header formatted like
        # INDICATOR:
        new_lines.append(indicator + ":\n")

        # iterating through the lines read from the text file
        for line in lines:
            # if the line contains an idicator then it is added to the list of the sorted lines
            if line.lower().count(indicator.lower()) != 0:
                # writing the line that contains the idicator back to the file in the following
                # format
                #   - LINE
                new_lines.append("\t- " + line)
        
        # this adds a break between each indicator's section
        new_lines.append("\n")

    # writing the sorted lines back to the text file
    f = open(file_name, 'w')
    for line in new_lines:
        f.write(line)
    f.close()


def group_into_master_file(directory_contents):
    # name of the file that all information from all files will be sent to
    master_file_name = "MASTER.txt"

    # creates a 2-d list and adds the indicator string to the beginning of each row,
    # adding the string in this manner is purely my choice of formating
    master_file_lines = []
    for indicator in indicators:
        master_file_line = [indicator + ":\n"]
        master_file_lines.append(master_file_line)

    # writing the header of the file to the master file, this is my choice of a header
    f = open(master_file_name, 'w')
    f.write("All sentences from this directory with the specified indicators:\n\n")
    f.close()

    # to be used later to know what row to add strings to
    pos = 0

    # loops through the files in the directory
    for file in directory_contents:
        # the for loop and the if coupled together filter out the text files
        if file.count('.txt') != 0:
            # opening the text file for reading then reading all of the lines into
            # a list then closing the file
            sub_f = open(file, 'r')
            sub_f_lines = sub_f.readlines()
            sub_f.close()

            # iterating through the contents of the previously opened text file
            for line in sub_f_lines:
                # checking if the line is a section header
                if line[0] != "\t" and len(line.strip()) != 0:
                    # this for loop looks for a the section header in the 2-d list
                    # that is the contents of the master file
                    for i in range(len(master_file_lines)):
                        # if the section header from the file opened in this loop is
                        # the same section header as in the master file contents list
                        if line.lower() == master_file_lines[i][0].lower():
                            # providing the index so that later code knows where to add strings
                            pos = i

                elif len(line.strip()) != 0:
                    # if not section header then it is section contents
                    # adding the contents to appropriate position in the master file's contents
                    master_file_lines[pos].append("\t-"+file.replace(".txt", ".docx")+": "+line[3:])

    # writing the contents to the master file
    f = open(master_file_name, 'a')
    for line in master_file_lines:
        for item in line:
            # if the line is not blank
            if len(item.strip()) != 0:
                f.write(item)
        # adding a break between the sections
        f.write('\n')

    f.close()

# lists the contents of the current directory
contents = os.listdir()

# iterating through all of the files in the current directory
for file in contents:
    # if the file is a Word Doc
    if file.count('.docx') != 0:
        # writing all of the sentences in the word doc that contain one of the indicators
        # declared at the beginnging of file to text file then sorting it and some other 
        # things
        write_action_verd_sent_to_file(file)

# listing the contents in the current directory, updated after the text file were made
contents = os.listdir()

# takes all of the sentences that were written to all of the text files in the directory
# and puts them into a sorted main text file
group_into_master_file(contents)
