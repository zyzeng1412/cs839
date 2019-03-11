#!/usr/bin/env python3

"""
    This transform the labeled datasets into structured data in dat files with features
    """

import sys
import os
import re

# return 1 if  a sentence is capitalized
def _is_capitalized(sentence):
    return 1 if all(word[0].isupper() for word in sentence.split()) else 0


# return 1 if  a sentence contain certain suffix
def containNameSuffix(sentence):
    suffix = ['Jr', 'II', 'III']
    for su in suffix:
        if su in sentence:
            #print(sentence)
            return 1
    return 0

# return the number of word in the sentence
def _num_word(sentence):
    return len(sentence.split())

# return a substring list of the sentence
def _split_sentence(sentence, word_num=1):
    tokens = sentence.split()
    n = len(tokens)
    return [" ".join(tokens[i:i + word_num])
            for i in range(0, n - word_num + 1)]

# return pos/neg examples from files in a directory
def generate_samples(dir, is_positive, start_tag='<Name>', end_tag='</Name>'):
    start_tag_len, end_tag_len = len(start_tag), len(end_tag)
    sentence_delimiter = r"[,.!?;]\s*"
    samples = []
    word_nums = [1, 2, 3]
    fileList = os.listdir(dir)
    for fname in fileList:
        input_path = os.path.join(dir, fname)
        with open(input_path, 'r') as file:
            content = file.read()
        sentences = re.split(sentence_delimiter, content)
        
        #when sample is marked as a Name
        if is_positive:
            for sentence in sentences:
                sentence_len = _num_word(sentence)
                for match in re.finditer(
                                         r"{}[^<]*{}".format(start_tag, end_tag), sentence):
                    string = sentence[match.start():match.end()]
                    name = string[start_tag_len: -end_tag_len]
                    
                    if sentence[match.start()-4:match.start()-1] =='the':
                        prev_word=1
                    else:
                        prev_word=0
                    sample = (name, containNameSuffix(name), _num_word(name), _is_capitalized(name),
                              _num_word(sentence[:match.start()]), sentence_len, prev_word, 1)
                    samples.append(sample)


        else:
            for sentence in sentences:
                sentence_len = _num_word(sentence)
                for word_num in word_nums:
                    substrings = _split_sentence(sentence, word_num)
                    for index, substring in enumerate(substrings):
                        if not (start_tag in substring or end_tag in substring):
                            
                            if index>1 and sentence.split()[index//word_num-1]=='the':
                                prev_word=1
                            else:
                                prev_word=0
                                sample = (substring, containNameSuffix(substring), _num_word(substring), _is_capitalized(substring),
                                          index, sentence_len, prev_word, 0)
                                sample = (substring,
                                          containNameSuffix(substring),
                                          _num_word(substring),
                                          _is_capitalized(substring),
                                          index, sentence_len,prev_word,
                                          0)
                            samples.append(sample)
    return samples

# output these samples to a dat file
def write_samples_to_file(outfile, samples):
    with open(outfile, 'w') as file:
        for sample in samples:
            file.write("{}\n".format(str(sample)[1:-1]))
    print("writing {:d} samples to {}".format(len(samples), outfile))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
              "Usage: >> python {} <input_folder> <output_file> <pos or neg>".format(
                                                                                     sys.argv[0]))
        sys.exit(1)
    dir_name, output_file_name = sys.argv[1:-1]
    positive = True if sys.argv[-1] == 'pos' else False
    # setting parameters
    start_tag, end_tag = '<Name>', '</Name>'
    samples = generate_samples(dir_name, positive, start_tag, end_tag)
    write_samples_to_file(output_file_name, samples)


