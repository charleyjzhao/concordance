from collections import defaultdict
import string
import re


def joinLines(inputLines):
    # join lines into one string
    joined = ""
    for line in inputLines:
        if line[0] == ' ':
            line = line.lstrip()
        if line[-1] in ['.', '!', '?']:
            tmp = line + ' '
        elif line[-1] != ' ':
            tmp = line + ' '
        else:
            tmp = line
        joined += tmp
    return joined


def getSentences(inputLines):
    # from http://en.wikipedia.org/wiki/Sentence_boundary_disambiguation
    regex = "((?<=[a-z0-9][.?!])|(?<=[a-z0-9][.?!]\"))(\s|\r\n)(?=\"?[A-Z])"
    text = joinLines(inputLines)
    # split string on sentence boundary disambiguation
    regexTmp = re.split(regex, text)

    # remove sentences that are too short
    tmpSentences = [sent for sent in regexTmp if len(sent) >= 2]

    # correct improper splits done on title abbreviations (e.g. Mr. Smith)
    sentences = []
    curr = ""
    for i in range(len(tmpSentences)):
        if tmpSentences[i][-4:].lower() in [' mr.', ' ms.', 'mrs.', ' jr.', ' sr.']:
            curr += (tmpSentences[i].strip().rstrip("!.?") + ' ')
        else:
            curr += tmpSentences[i]
            sentences.append(curr.strip().rstrip("!.?"))
            curr = ""
    if curr != "":
        sentences.append(curr)
    return sentences


def generateAndPrintConcordance(inputLines):
    sentences = getSentences(inputLines)
    counts = defaultdict(int)  # word count
    sent_nos = defaultdict(list)  # sentence numbers per word

    # loop over each enumerated sentence
    for sent_no, sentence in enumerate(sentences):
        for word in sentence.split(' '):
            lower_word = word.strip(",:;?").lower()
            counts[lower_word] += 1
            sent_nos[lower_word].append(sent_no + 1)

    for key in sorted(counts.keys()):
        if key == '':
            continue
        print("%s: {%d:%s}" %
              (key, counts[key], ','.join(map(str, sent_nos[key]))))
