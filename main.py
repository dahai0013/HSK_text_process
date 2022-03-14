import argparse
import HSK_text_process

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='File1_chinese_text.txt', help='input file for checking')
    parser.add_argument('--highlighted', type=str, default='tmp1.csv', help='file to store highlighted words')
    parser.add_argument('--statistic', type=str, default='tmp2.csv', help='file to store words statistics')
    parser.add_argument('--html', type=str, default='File2_hsk_2_by_chapter_a-_vocabulary_20220314050202.csv', help='html file as input')
    parser.add_argument('--output', type=str, default='tmp3.csv', help='html file as input')
    args = parser.parse_args()

    input, highlighted, statistic, html, output = args.input, args.highlighted, args.statistic, args.html, args.output

    HSK_text_process.extract_character(input, highlighted, statistic, statistics_opt = 2)
    words = HSK_text_process.read_highlighted_words(input)
    HSK_text_process.find_from_html('error_text.csv', words, 'tmp3.csv')
    HSK_text_process.find_from_html(html, words, output)
