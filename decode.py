#!python3
#brought to you by Shin & nanananate



#import google_api_interact  # I think you can remove this
import traceback
import base64
from collections import namedtuple
from collections import defaultdict
import asyncio
import time
import random



class TestError(Exception):
    pass


DEBUG = False

def dp(wot: str):
    '''Debug Print (hence dp) '''
    if DEBUG:
        print(wot)



###### decode that shit #######



morsecode_dict = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----',
                    '(':'-.--.', ')':'-.--.-', ' ': '/',
                    "." : ".-.-.-",
                    "," : "--..--",
                    ":" : "---...",
                    "?" : "..--..",
                    "'" : ".----.",
                    "-" : "-....-",
                    "/" : "-..-.",
                    "@" : ".--.-.",
                    "=" : "-...-"
                    }

INVALID_INPUT = '#INVALID_INPUT#'
alphabet = "abcdefghijklmnopqrstuvwxyz"
atbash = str.maketrans(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
    "ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba")
rot13 = str.maketrans(
    "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz",
    "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")
wordlist =open('wordlist.txt', 'r')
wordlist_str=wordlist.read()
wordlist.close()
valid_word=(wordlist_str.lower()).split()



    ####### applying delimiter ########

def force_delimiter(code, length):
    string = ''.join(code.split())                                              #removes all spaces
    string = string.replace('-', '')                                            #removes all dashes
    string = string.replace('/', '')                                            #removes all slashes
    return ' '.join(string[i:i+length] for i in range(0, len(code), length))    #places a space every length



class Decode:
    def __init__(self, content: str):
        self.content = content #for interpretation as a whole
        self.codes = content.split() #for interpretation as parts
        check_code = namedtuple('Code', 'code likely analysis')
        self.valid_english = False
        self.codes_used = []
        self.layers = []
        self.layers_info = [] #more detailed info compared to layers
        dp('AAAAHHH')


    def get_path(self, code, layers_info = None):
        path = []
        if layers_info == None:
            layers_info = self.layers_info
        if layers_info == []:
            return []

        layer = layers_info[-1]

        for key in layer.keys():

            if code in key:

                path.append(layer[key])
                
                path.extend(self.get_path(layer[key][1], layers_info[:-1]))
                return path


    def str_fx_path(self, path: 'List of tuple'):
        result = 'Enciphered Text > '
        for item in path[::-1]:
            result += item[0] + ' > '

        return result + 'result'

    def str_path(self, path: 'List of tuple'):
        result = 'From Robot-Nate :D | Check me out~ https://discordbots.org/bot/428591194185138178\n\n'
        for number, item in enumerate(path[::-1]):
            number += 1
            result += item[1] + '\n\n'
            result += '> {}\n'.format(item[0])

        return result + self.confirmed_code




    def str_layers_info(self):
        result = "Decodes from Robot-Nate :D | Check me out~ https://discordbots.org/bot/428591194185138178\n"
        count = 0
        for layer in self.layers_info:
            count += 1
            result += '{:-^120}\n'.format(' Layer {} '.format(count))
            result += "{:50s} | {:20s} | {:50s}\n".format('Previous Code', 'Decoded through', 'Result')
            for key in layer.keys():
                try:
                    result += "{:50s} | {:20s} | {:50s}\n".format(layer[key][1], layer[key][0], str(key))
                except:
                    traceback.print_exc()
                    result += "internal error \n"

        return result

    ######### rotation codes ######

    def Caesar_decrypt(self, x:str, y: int)->str:
        'Returns plain text that is ran backwards through a caesar cypher'
        z=y%26
        x = x.lower()
        # invalid_char = dict()
        # invalid_char_count = 0
        # for char in x:
        #     if char not in alphabet:
        #         invalid_char.update({invalid_char_count: char})
        #         invalid_char_count += 1

        a=alphabet[-z+26:26]+alphabet[0:26-z]
        table=str.maketrans(alphabet,a)
        result = x.translate(table)

        # char_count = 0
        # final = ''
        # if invalid_char_count > 0:
        #     for letter in x:
        #         try:
        #             final += invalid_char[invalid_char_count]
        #             char_count += 1
        #         except KeyError:
        #             pass
        #         final += letter
        #         char_count += 1

        return result

    def decrypt_word_list(self, a: str, x: int) -> 'list of str':
        'Returns a list of Caesar_decrypted words'
        result = []
        words = a.split()
        for i in words:
            result.append(self.Caesar_decrypt(i, x))
        return result

    def english_match(self, a: str, x: int) -> 'list of strings':
        '''Looks for english words in decrypt_word_list, adds those english words to list
        Used for caesar '''
        wordlist =open(r'C:\Users\Aska\Downloads\wordlist.txt', 'r')
        wordlist_str=wordlist.read()
        wordlist.close()
        I=(wordlist_str.lower()).split()
        words = (a.lower()).split()
        english = []
        for n in self.decrypt_word_list(a, x):
            if n in I:
                english.append(n)
        return english



    def encode_caesar(self, code = None, rot = 13):
    	if code == None:
    		code = self.content
    	return self.Caesar_decrypt(code, rot)


    async def caesar_break(self, code = None, single = False)->str:
        '''Does english_match for every possible decryption,
        returns the decryption with adequate english words'''
        try:
            if code == None:
                code = self.conent
            elif code == INVALID_INPUT:
                return [INVALID_INPUT]
            cool_word = code.strip()
            length = len(cool_word.split())
            a =cool_word.lower()
            for n in range(26):
                dp(self.Caesar_decrypt(a, n))
                if len(self.english_match(a, n)) > length/3:
                    result = self.Caesar_decrypt(a, n)
                    self.is_english(result)
                    return [result]

            return [INVALID_INPUT]

        except:
            return [INVALID_INPUT]


    ########## binary codes #######



    def encode_hex(self, code = None, single = False):
        if code == None:
            code = self.content

        return (base64.b16encode(bytes(code, encoding = 'utf-8'))).decode('utf-8')



    async def decode_hex(self, code = None, single = False):
        '''Takes in content, return decoded hex'''
        result = []

        if code == None:
            code = self.content

        # if code.startswith('0x'):
        #     print('yeet')
        #     code = code[2:]


        try:

            decoded = bytearray.fromhex(code).decode()
            self.is_english(decoded)
            result.append(decoded)

        except:
            result.append(INVALID_INPUT)

        try:
            decoded_byte = hex(int(code))
            result.append(bytearray.fromhex(decoded_byte).decode())
        except:
            result.append(INVALID_INPUT)

        remove_duplicates = set(result)
        return list(remove_duplicates)



    def encode_base64(self, code = None, single = False):
        if code == None:
            code = self.content

        return (base64.b64encode(bytes(code, encoding = 'utf-8'), altchars=None)).decode('utf-8')




    async def decode_base64(self, code = None, single = False):
        result = []
        try:
            if code == None:
                code = self.content

            decoded = (base64.b64decode(code, altchars=None, validate=False)).decode('utf-8')
            self.is_english(decoded)
            result.append(decoded)
        except:
            result.append(INVALID_INPUT)
        finally:
            remove_duplicates = set(result)
            return list(remove_duplicates)



    def encode_ascii(self, code = None, single = False):
        if code == None:
            code = self.content

        code = str(code)

        return ' '.join(str(ord(str(s))) for s in code)



    async def decode_ascii(self, code = None, single = False):
        try:
            if code == None:
                code = self.content

            if type(code) is not list:
                code = code.split()

            result = ''.join(chr(int(i)) for i in code) # maybe consider breaking this down for try/except block for poorly written code

            self.is_english(result)

            return [result]

        except:
            return [INVALID_INPUT]




    def encode_morse(self, code = None):
    	if code == None:
    		code = self.content
    	result = ''
    	for char in code:
    		try:
    			result += morsecode_dict[char.upper()] + ' '
    		except KeyError:
    			result += char
    	return result.strip()



    async def decode_morse(self, code = None, single = False):
        '''needs to be split by spaces '''
        decoded = ''
        morsecode_dict_reversed = {value:key for key,value in morsecode_dict.items()}
        result = []
        if code == None:
            code = self.codes


        if type(code) is not list or type(code) is str:
            formatted_code = (code).split()


        else:
            formatted_code = code
        try:
            for letter in formatted_code:

                try:
                    dp(str(letter) + str(morsecode_dict_reversed[letter]))
                    decoded += morsecode_dict_reversed[letter]
                except:
                    return [INVALID_INPUT]
            self.is_english(decoded)
            result.append(decoded)
            self.valid_english = True
            self.confirmed_code = decoded
            return [decoded]
        except:
            return [INVALID_INPUT]



    def encode_binary(self, code = None, single = False):
        if code == None:
            code = self.content

        binary = code.encode()
        return binary


    async def decode_binary(self, code = None, single = False):
            result = []
            decoded = []

            if code == None:
                code = self.content
            try:
                dp('binary')
                temp = force_delimiter(code, 8)
                temp = temp.split()
                for i in temp:
                    decoded.append(chr(int(i, 2)))
                decoded = ''.join(decoded)
                self.is_english(decoded)
                result.append(decoded)
                #print(decoded)
            except:
                result.append(INVALID_INPUT)

    #        try:
    #            decoded_b64 = base64.decodebytes(bytes(code, 'utf-8'))
    #            result.append(decoded_b64.decode("utf-8"))
    #        except:
    #            result.append(INVALID_INPUT)



    #        finally:
    #            remove_duplicates = set(result)
            #print(result)

            return result




    async def decode_binary_bases(self, code = None):
        result = []
        start = time.time()
        if code == None:
            code = self.content
        for x in range(2, 6):                                              #cycles through the delimiter function creating groups of 2-5 characters and the saving them in an array
            temp = force_delimiter(code, x)
            temp = temp.split()
            for base in [3,4,5,6,7,8,9,10]:                                #cycles through the bases
                num_decoded = []                                           #variables reset each cycle to prevent duplicates
                ascii_decoded = ''
                for i in temp:
                    try:
                        num_decoded.append(int(i, base))                   #appends the corresponding base10 value
                        if int(i, base) >= 32 and int(i, base) <= 126:     #checks if the corresponding base10 value is in range
                            ascii_decoded += chr(int(i, base))             #appends the corresponding ascii character
                    except:
                        num_decoded = []                                   #resets the variable if something can not be decoded with current base
                        ascii_decoded = ''
                        break
                    finally:
                        #print(str(time.time() - start))
                        if (time.time() - start) > 10:
                            return [INVALID_INPUT]
                        elif (time.time() - start) > 5:
                            await asyncio.sleep(6)
                            start = time.time()


                if num_decoded:                                            #checks if the variable is empty
                    num_decoded_string = ''.join(map(str, num_decoded))    #from list with lists to list with strings because nate-bot can't read list of lists
                    result.append(num_decoded_string)                      #appends the variable
                    if len(ascii_decoded) == len(num_decoded):             #checks if the ascii character string has the same length as the number array
                        self.is_english(ascii_decoded)
                        result.append(ascii_decoded)                       #appends the string


        if not result:
            return [INVALID_INPUT]

        return result




    async def atbash(self, code = None):
        try:
            if code == None:
                code = self.content
            result = str.translate(code, atbash)                #translate the original using the alphabet set in line 49-51
            self.is_english(result)
            if result != code:
                return [result]
            else:
                return [INVALID_INPUT]
            return [result]
        except:
            return [INVALID_INPUT]




    async def rot13(self, code = None, single = False):
        try:
            if code == None:
                code = self.content
            result = str.translate(code, rot13)             #translate the original using the alphabet set in line 52-54
            
            if single:
                return result

            self.is_english(result)
            if result != code:
                return [result]
            else:
                return [INVALID_INPUT]
            return [result]
        except:
            return [INVALID_INPUT]



    async def rot47(self, code = None, single = False):
        try:
            if code == None:
                code = self.content
            temp = []
            for i in range(len(code)):
                n = ord(code[i])                            #ord() gives either a unicode code point (if argument is unicode object) or an int (if argument is 8-bit string)
                if n >= 33 and n <= 126:                    #rot47 is limited to ascii-characters in the range of 33-126, if it's outside the range it won't get rot'ed
                    temp.append(chr(33 + ((n + 14) % 94)))  #calculating the new int. chr() returns the ascii character sorresponding to the given int
                else:
                    temp.append(code[i])                    #if n is out of range, original value gets appended

            result = ''.join(temp)                          #joins the result back together into one string
            
            if single:
                return result

            self.is_english(result)
            if result != code:
                return [result]
            else:
                return [INVALID_INPUT]
            return [result]
        except:
            return [INVALID_INPUT]



    def is_english(self, a: str):
        'some crappy function i made a very long time ago'
        words = (a.lower()).split()
        english = []
        for word in words:
            if word in valid_word and len(word) > 2:
                english.append(word)

        if (len(english) / len(words)) > 0.3:
            self.valid_english = True
            self.confirmed_code = a





    def auto_decode(self):
        '''outdated function, used mostly for debugging a single layer '''
        decode_fx = [self.decode_hex, self.decode_morse, self.decode_morse,
                    self.decode_base64, self.decode_binary, self.caesar_break,
                    self.decode_binary_bases, self.atbash, self.rot13, self.rot47]
        for function in decode_fx:
            decoded = function()
#            print(function)
#            print(decoded)
            if self.valid_english:
                return decoded

        return('None')


    def multi_layer_encode(self, code = None, encoding = None, layers = 1):
        code_fx = {'hex': self.encode_hex, 'morse': self.encode_morse, 'base64': self.encode_base64,
                    'binary': self.encode_binary, 'rot13': self.rot13, 'rot47': self.rot47,
                    'caesar': self.encode_caesar, 'ascii': self.encode_ascii}
        if code == None:
            code = self.content            
        new_code = code



        if encoding != None:
            print(encoding, code)
            encoding = code_fx[encoding]
            result = encoding(code, single = True)
            return result


        for layer in range(layers):

            encoding_name = random.choice(list(code_fx.keys()))
            encoding = code_fx[encoding_name]

            new_code = encoding(new_code)
            self.codes_used.append(encoding_name)

        print(self.codes_used)

        return new_code








        




    async def multi_layer_decode(self):
        decode_fx = {'decode_hex': self.decode_hex, 'decode_morse': self.decode_morse,
                    'decode_base64': self.decode_base64, 'decode_binary': self.decode_binary,
                     'decode_caesar': self.caesar_break, 'decode_binary_bases': self.decode_binary_bases,
                     'atbash': self.atbash, 'rot13': self.rot13, 'rot47': self.rot47,
                     'decode_ascii': self.decode_ascii}


        global INVALID_INPUT

        Flag = True
        layer = 0
        single_layer_decodes = {'orginal': [self.content]}
        decode_num = 0

        start = time.time()

        time_out = 70
        decodes_used = dict()

        while Flag:
            temp_decodes = dict() # i don't think I use this anymore

            layer_dict = dict() # info about decodes used and their results, used as a traceback


            for result in single_layer_decodes.values(): # dictionary of coding: code
                #print(single_layer_decodes)
                for decode, fx, in decode_fx.items(): # list of function objects

                    another_start = time.time()
                    for code in result:
                        decoded = await fx(code)
                        #print(code)
                        #print(decoded)
                        decoded_str = ''.join(decoded)
                        #print(str((time.time() - start)))

                        if decoded_str != INVALID_INPUT:
                            dp(decode)
                            temp_decodes.update({decode_num: decoded})
                            decode_num += 1
                            layer_dict.update({tuple(decoded): (decode, code)})


                            if self.valid_english:
                                print('we got something')
                                layer_dict.update({self.confirmed_code: (decode, code)}) # just in case decoded differs from confirmed_code
                                self.layers_info.append(layer_dict)
                                print('confirmed', self.confirmed_code)
                                return str(self.confirmed_code)

                        elif (time.time() - start) > time_out:
                            return ("Timed out - Bot")

                        elif (time.time() - another_start) > 2:
                            await asyncio.sleep(6)
            #print(temp_decodes)
            #print(str((time.time() - start)))


            await asyncio.sleep(6)
            if (time.time() - start) > time_out:
                return ("Timed out - Bot")


            single_layer_decodes = dict() # resets to be ready for next layer

            for decode, processed_code in temp_decodes.items():
                '''To prevent mutated references when I clear
                temp_decodes after this '''
                single_layer_decodes.update({decode: processed_code})

            self.layers.append(single_layer_decodes)
            self.layers_info.append(layer_dict)

            #asyncio.sleep(1)

            if layer > 6:
                print('nothing to see here')
                return ("Couldn't be decoded - Bot")



            layer += 1





#Google translate API

#### debugging ####



ex_b64 = "MzMxNjAyMzM5MzAyMjMyMzAyMzM5MzAyMzM4MzAyMjMyMzAyMzMyNjAyMzM4MzAyMjMyMzAyMzMxNjAyMzMyNjAyMjMyMzAyMzM5MzAyMzMxNjAyMjMyMzAyMzMxNjAyMzM1MzAyMjMyMzAyMzMyNjAyMzM2MzAyMjMyMzAyMzMxNjAyMzMzNjAyMjMyMzAyMzMxNjAyMzMzNjAyMjMyMzAyMzMxNjAyMzMyNjAyMjMyMw=="

async def test_cases():
    if True:

        dp('hex')
        dp(Decode('7061756c').decode_hex())
        dp('')
        dp('Base64')
        dp(Decode('aGVsbG8gdGhlcmU=').decode_base64())
        dp('')
        dp('Morse')
        dp(Decode('- .... .. ... / .. ... / . -. --. .-.. .. ... ....').decode_morse())
        dp("")
        dp('bi')
        big_bi = Decode('010010010111001100100000011101000110100001101001011100110010000001110100011010000110010100100000011001010110111001100100001000000110111101100110001000000110110101100101')
        dp(big_bi.decode_binary())
        dp(big_bi.valid_english)
        dp('')
        dp('base-n')
        dp(Decode('102 141 163 145 055 156 040 157 143 164 141 154 040 164 145 163 164').decode_binary_bases())
        dp('Atbash')
        dp(Decode('Zgyzhs Gvhg').atbash())
        dp('')
        dp('Rot13')
        dp(Decode('Ebg13 grfg').rot13())
        dp('')
        dp('Rot47')
        dp(Decode('#@Ecf E6DE').rot47())
        dp('auto_test')
        dp(Decode('7061756c').auto_decode())
        dp(Decode('010010010111001100100000011101000110100001101001011100110010000001110100011010000110010100100000011001010110111001100100001000000110111101100110001000000110110101100101').auto_decode())

        Flag = True
        while Flag:
            lit = input('Gimme something: ')
            if lit == 'q':
                break
            a = Decode(lit)
            b = await a.multi_layer_decode()
            print(b)

#        test = '102 141 163 145 055 156 040 157 143 164 141 154 040 164 145 163 164'
#        Decode(test).auto_decode()
#        print(Decode(test).multi_layer_decode())

async def test_cases2():
    code = Decode('hey there stranger.')
    print(code.code_morse())
    print(code.code_caesar())
    print(code.multi_layer_code())

async def test_cases3():

    code = Decode(''';:#2+@#:#-$!":+@!#;#+#!$;#3-#!$+$!$$-$!$!-#;1($+!3+#$. * ;#+;$#+. @;#+;$!$;$+2#;$+#!;$;%$-'+#;;;#.''')
    result = await code.multi_layer_decode()
    print(result)
    print(code.str_layers_info())
    path = code.get_path(result)
    print('path:', path)
    print(code.str_fx_path(path))
    print(code.str_path(path))

async def test_cases4():
    code = Decode('this is a test')
    result = code.encode_ascii()
    print(result)



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_cases4())
    loop.close() 


#### delete later #####
