import csv
import re
from collections import OrderedDict



def output_wordlist_to_csv_file(characters, output_highlighted_file):
    """ push the recorded characters with frequency to a csv file
    characters is the list of characters to output, output_highlighted_file is the target file to output
    :param characters: list of characters to output
    :param output_highlighted_file: target file to output
    :return: NA
    """

    try:
        with open(output_highlighted_file, 'w') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in characters.items():
                writer.writerow([key, value])
    except IOError:
        print("I/O error")


def getChinese(context):
    #context = context.decode("utf-8") # convert context from str to unicode
    filtrate = re.compile(u'[^\u4E00-\u9FA5·]') # non-Chinese unicode range
    context = filtrate.sub(r'', context) # remove all non-Chinese characters
    #context = context.encode("utf-8") # convert unicode back to str
    return context

def extract_character(input_file, output_highlighted_file, output_statistics_file = None, statistics_opt = 0):
    """ extract characters from a .txt and put the extract characters into a .csv file
        this function extract all chinese character with prefix dot(.) from the input_file and put it into a .csv file.
        the statistics will be generated if needed: --statistics_opt
        1: order by appearance
        2: order by optional number of strocks
        3: order by alphabetic
        others: as default 1
    :param input_file: a .txt to extract characters
    :param output_highlighted_file: a .csv file to store the output result for highlighted characters
    :param output_statistics_file: the file to store statistic result; default as None, then statistic will be output
    :param statistics_opt: 1: order by appearance; 2: order by optional number of strocks; 3: order by alphabetic; others: as default 1
    :return: the highlighted words, and all words with statistics as dictionary
    """

    #read text from input file
    with open(input_file) as f:
        contents = f.readlines()

    # highlighted_words - all characters with dot as prefix: it stores the {character: frequency}
    highlighted_words = {}

    # highlighted_words - all characters appear in the text: it stores the {character: frequency}
    all_words = {}

    total_number_characters = 0
    # iterate with each line
    for line in contents:
        line = line.replace('\n', '')

        # if valid line starting with A-,B-,C-,D-, then start to scan this line
        if len(line) > 0:# and line[0] in ['A', 'B', 'C', 'D']:

            # remove invalid characters
            #line = re.sub('[\u4e00-\u9fff]+', '', line[2:])
            line = getChinese(line)
            #line = re.sub(r'[a-zA-Z0-9，=【】áā ！!f)：(:.？。",éàīí?!]（ěíī）', '', line[2:])
            #line = line.replace("-",'')

            # find all position for dot ·
            dot_pos = [_.start() for _ in re.finditer('·', line)]

            # for each position of dot, record the character after that dot, and record the frequency of corresponding character
            for pos in dot_pos:
                if line[pos + 1] in highlighted_words.keys():
                    count = highlighted_words[line[pos + 1]]
                    highlighted_words[line[pos + 1]] = count + 1
                else:
                    highlighted_words[line[pos + 1]] = 1

            # for all characters appeared, record the character and record the frequency of corresponding character
            for pos in range(len(line)):
                if line[pos] != '·':
                    total_number_characters += 1
                    if line[pos] in all_words.keys():
                        count = all_words[line[pos]]
                        all_words[line[pos]] = count + 1
                    else:
                        all_words[line[pos]] = 1

    unique_number_characters = len(all_words)

    # id statistics option is 1: then sort the list by character
    if statistics_opt == 2:
        all_words = OrderedDict(sorted(all_words.items(),key=lambda kv: kv[1], reverse=True))

    # id statistics option is 2: then sort the list by character
    if statistics_opt == 3:
        all_words =  OrderedDict(sorted(all_words.items()))

    # output the highlighted characters as csv files
    output_wordlist_to_csv_file(highlighted_words, output_highlighted_file)

    # output statistics if needed
    if output_statistics_file is not None:
        output_wordlist_to_csv_file(all_words, output_statistics_file)

    # print out the statistic of total number of characters and unique number of characters
    print('---total number of characters =', total_number_characters)
    print('---unique number of characters =', unique_number_characters)

    # return highlighted_words and all_words in case needed
    return highlighted_words, all_words


def read_highlighted_words(input_file):
    """ read from the highlight words file and return the highlihgted word list file and return the highlighted words as set
    :param input_file: the file which stores the highlihgted characters
    :return: a set of highlighted characters read from the input_file
    """

    words = set()

    # read from the highlight words file, and put the words into words
    with open(input_file) as f:
        lines = f.readlines()
    for line in lines:
        words.add(line.split(',')[0])

    # return the highlighted words as set
    return words



def log_imvalid_html(line):
    """ append one line to the log file; here the appended line is the line not in correct html format
    :param line: bad formatted html file
    :return: NA
    """

    try:
        file_object = open("logfile.log", "a")
        file_object.write(line + '\n')
    except IOError:
        print("I/O error")


def find_from_html(file_name, words, output_file):
    """ serach from the html format csv file for the words (defined in words) and output the search result to output csv file (html format)
    :param file_name: html format csv file to search (word dictionary)
    :param words: a list of words need to be searched
    :param output_file: the file name to store the searching result
    :return: NA
    """

    #define the pattern as clean to remove the markers in html file
    clean = re.compile('<.*?>')

    # read from the html file (dictionary)
    with open(file_name) as f:
        lines = f.readlines()

    result_lines = []

    # iterate each line in the html file/dictionary
    for one_line in lines:
        line = one_line.split(',')[0]
        # remove html markers to obtain the clean text
        cleaned_line = re.sub(clean, '', line.replace('\n', ''))
        if cleaned_line.find('<') >= 0 or cleaned_line.find('>') >= 0:

            # if the line if not proper html format print warning and log it into the logfile.log
            print('wrong format! ---', line)
            log_imvalid_html(line)

        else:
            # if the line is in correct format, search whether this line include the word we want to search for
            for word in words:
                if word in line:
                    #print(one_line)
                    # if this line includes the word we are searching for, then append it to result_lines as one result clause which will be dump to the result file
                    result_lines.append(one_line)
                    break
    try:

        # output the searching result to output_file
        file_object = open(output_file, 'w')
        for result_line in result_lines:
            file_object.write(result_line)

    except IOError:
        print("I/O error")


