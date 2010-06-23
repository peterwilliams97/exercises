"""

Search for strings in files

http://docs.python.org/howto/regex.html#regex-howto

Created on 23/06/2010

@author: peter
"""
import re

string_pattern = '"*?"'
pattern = re.compile(string_pattern)

def findJavaStrings(text):
   return pattern.findall(text)  

    
if __name__ == '__main__':
    text = ' aaa bbbb "c" ddd "ff gg" h '
    strings = findJavaStrings(text)
    print text
    for i,s in enumerate(strings):
        print i, s