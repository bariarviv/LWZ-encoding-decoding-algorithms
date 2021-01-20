"""
LWZ encoding & decoding algorithms.
@author: Bari Arviv
"""
import shutil
from tabulate import tabulate # must to: pip install tabulate

# Saving the terminal width value.
SIZE_SCREEN = shutil.get_terminal_size().columns


def encode(sentence):
    """The function performs compression according to the LZW algorithm. 
       In addition, it prints a table that includes all the steps of the
       algorithm. Finally, returns a list of the sentence after compression.
       :param sentence: a sentence we would like to compress.
       :type sentence: string
       :return: compressed list of sentence.
       :rtype: list
    """
    # The dictionary is initialized with symbols from  
    # the source alphabet (ASCII values). char(i): i
    dict_size = 256
    encode_dict = dict((chr(i), i) for i in range(dict_size))
    
    # Initializes required to build the table.
    tbl_list = []
    row_tbl = []
    head_tbl = 'LZW Encoding Table:'
    header_list = ['Prefix w', 'Input', 'Pointer Dict', 'New Phrase Dict',
                   'Phrase Output', 'Pointer Output']
    in_dict = ['nil','nil','nil','nil']
    
    # Initialize the output list.
    compress = []
    prefix = ""

    # The encoder then examines the string of source output symbols  
    # until a phrase occurs that is not in the dictionary. 
    for ch in sentence:
        row_tbl = [prefix, ch]
        phrase = prefix + ch
        
        if phrase in encode_dict:
            prefix = phrase
            prev = ch
            row_tbl.extend(in_dict)
        else:
            # The new phrase is added to the dictionary along with its 
            # associated index, and the encoder outputs the index 
            # corresponding to the prefix of the just-identified new phrase.
            compress.append(encode_dict[prefix])
            encode_dict[phrase] = dict_size
            dict_size += 1
            
            # The new symbol becomes the initial symbol of the
            # next substring to be added to the dictionary.
            prev = prefix
            prefix = ch
            row_tbl.extend([encode_dict[phrase], phrase, prev, encode_dict[prev]])
        
        # Add a row to the table.
        tbl_list.append(row_tbl)
    
    # Add the last prefix to the output list.
    compress.append(encode_dict[prefix])
    # Add the last row to the table and print it.
    tbl_list[0][0] = 'nil'
    tbl_list.append([prefix, 'nil', 'nil', 'nil', prefix, encode_dict[prefix]]) 
    print_table(head_tbl, tbl_list, header_list)
    return compress


def decode(compress):
    """The function performs decompression according to the LZW algorithm. 
       In addition, it prints a table that includes all the steps of the
       algorithm. Finally, returns the sentence after decompression.
       :param compress: the sentence after compression.
       :type compress: list
       :return: the sentence after decompression.
       :rtype: string
    """
    # The dictionary is initialized with symbols from  
    # the source alphabet (ASCII values). i: char(i)
    dict_size = 256
    decode_dict = dict((i, chr(i)) for i in range(dict_size))

    # Initializes required to build the table.
    tbl_list = []
    head_tbl = 'LZW Decoding Table:'
    header_list = ['Prefix w','Pointer Input', 'Phrase Input', 'Pointer Dict',
                   'New Phrase Dict', 'Output Phrase']
    
    # Initialize the output stirng.
    decompress = ""
    
    # The first received pointer (codeword) always represents a character in 
    # the source alphabet. So the decoder outputs the character corresponding 
    # to the received pointer and also initialized the prefix with it.
    save_first_element = compress.pop(0)
    prefix = chr(save_first_element)
    decompress += prefix
    # Initialize the first row of the table.
    row_tbl = ['nil', save_first_element, prefix, 'nil', 'nil', prefix]
    tbl_list.append(row_tbl)

    for pointer in compress:
        row_tbl = [prefix, pointer]
        
        # Decide what the new phrase is.
        if pointer in decode_dict:
            phrase = decode_dict[pointer]
        elif pointer == dict_size:
            phrase = prefix + prefix[0]
        
        # The decoder outputs and inserts the result in the dictionary.
        decompress += phrase
        decode_dict[dict_size] = prefix + phrase[0]
        dict_size += 1 
        prefix = phrase
        
        row_tbl.extend([phrase, dict_size - 1, decode_dict[dict_size - 1], phrase])
        # Add a row to the table.
        tbl_list.append(row_tbl)
    
    # Printing the table.
    print_table(head_tbl, tbl_list, header_list)
    # Insert the first codeword removed from the received code list.
    compress.insert(0, save_first_element)
    return decompress


def print_table(head, tbl, header_list):
    """The function prints a table using tabulate.
       :param head: table title.
       :type head: string
       :param tbl: A list that contains all the table rows. 
                   Each row is represented by a list.
       :type tbl: list
       :param header_list: list of table column headings.
       :type header_list: list
       :return: None
    """
    # Printing the table title in the middle of the screen.
    print(head.center(SIZE_SCREEN + int(len(head) / 2)))
    print('')
    print(tabulate(tbl, headers=header_list, stralign="center", numalign="center"))
    print('\n')


def print_part1(sentence, compress, decompress):
    """The function prints the results of part A of the task 
       which performs compression and then decompression.
       :param sentence: table title.
       :type sentence: string
       :param compress: the sentence after compression.
       :type compress: list
       :param decompress: the sentence after decompression.
       :type decompress: string
       :return: None
    """
    print('Explanation:\nThe sentence we want to compress:')
    print(sentence)
    print('\nThe sentence after compression:')
    print(compress)
    print('\nThe sentence after decompression:')
    print(decompress)
    print('\n')
   
    
def print_part2(code, decompress, compress):
    """The function prints the results of part B of the task 
       that performs decompression and then compression.
       :param code: table title.
       :type code: string
       :param decompress: the code after decompression.
       :type decompress: string
       :param compress: the code after compression.
       :type compress: list
       :return: None
    """
    print('Explanation:\nThe code we want to decompression:')
    print(code)
    print('\nThe code after decompression:')
    print(decompress)
    print('\nThe code after compression:')
    print(compress)
    print('\n')

    
def main():
    # Part A: sentence -> encode -> decode
    print("\nPart A: sentence -> encode -> decode\n- Sentence number 1:")
    # Sentence number 1
    sentence = 'It is better to have loved and lost than neverto have loved at all.'
    compress = encode(sentence)
    decompress = decode(compress)
    print_part1(sentence, compress, decompress)
    
    # Sentence number 2
    print("- Sentence number 2:")
    sentence2 = 'TO_BE_OR_NOT_TO_BE_THAT_IS_TO_BE'
    compress2 = encode(sentence2)
    decompress2 = decode(compress2)
    print_part1(sentence2, compress2, decompress2)
    
    # Part B: code -> decode -> encode
    print("Part B: code -> decode -> encode")
    code = [69, 97, 114, 108, 121, 32, 116, 111, 32, 98, 101, 100, 32, 97,
            110, 267, 101, 257, 259, 261, 263, 114, 105, 115, 101, 32, 109,
            97, 107, 101, 115, 268, 281, 269, 32, 104, 272, 108, 116, 104,
            121, 44, 32, 119, 292, 294, 260, 269, 267, 119, 278, 101, 46]
    decompress3 = decode(code)
    compress3 = encode(decompress3)
    print_part2(code, decompress3, compress3)

if __name__ == "__main__":
    main()