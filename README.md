# HSK_text_process

python 3.8

pip install python-csv

pip install regex

all functions are in HSK_text_process.py and can be called/re-used by other .py files (the following .py files call this file)

find_highlighted_words.py read from .txt file and find characters after ./dot, and output the highlighted characters and statistic into resulting file, which are currently set as tmp1.csv and tmp2.csv which you can change it or input as parameters

search_from_html.py read the highlighted characters from the output file above (tmp1.csv) and search for the relevant information from html format csv file and the output will be dumpde into another file (currently as tmp3.csv),  you can change it or input as parameters

main.py just combine find_highlighted_words.py and search_from_html.py together and complete the task in one go! 


