#!/usr/bin/env python

import string, sys

class TextDetect(object):
    
    def __init__(self):
        self.text_characters = "".join(map(chr, range(32, 127)) + list("\n\r\t\b"))
        self.null_trans = string.maketrans("", "")      
    
    def istextfile(self, filename, block_size=512): 
        return self.istext(open(filename, 'rb').read(block_size))
    
    def istext(self, s):  
        if '\0' in s: 
            return 0 
        if not s: 
            return 1
        t = s.translate(self.null_trans, self.text_characters)
        if len(t) * 1.00 / len(s) > 0.30:
            return 0
        return 1

"""
这个算法把一个字节的数据放入三个名单：
白名单:
9 (TAB), 10 (LF), 13 (CR), 32..255
灰名单：
7 (BEL), 8 (BS), 11(VT), 12 (FF), 26 (SUB), 27 (ESC)
黑名单：
0..6, 14..31

判断的方法是：
如果一个文件包含至少一个白名单中的字节而且不包含一个黑名单中的字节，那么它就是文本文件，否则它是二进制文件。
算法原理很简单，凡是出现了黑名单中的字节的文件几乎只可能是二进制文件，而普通的文本文件几乎不可能出现这些字节，即使是Unicode等多字节编码也会设置高位的标记字符以实现兼容ASCII。
"""
def isPlainText(filename):    
    white_list_char_count = 0        
    try:        
        fp = open(filename, 'rb')
        while True:
            char = fp.read(1)
            if not char: 
                break               
            byte = ord(char)         
            if  byte in [9, 10, 13] or 255 >= byte >= 32:
                white_list_char_count += 1
            elif byte <= 6 or 14 <= byte <= 31:
                return False                               
    finally:
        fp.close()                 
    return white_list_char_count >= 1   
    

def main(argv):
    import os, getopt
    try:
        args, dirnames = getopt.getopt(argv[1:], "h", ["help"])
    except getopt.error:
        args = "dummy"
    if args:
        print "Usage: %s <directory> [<directory> ...]" % (argv[0],)
        print " Shows which files in a directory are text and which are binary"
        sys.exit(0)
        
    detec = TextDetect()
    table = {0: "binary", 1: "text"}
    if not dirnames:
        dirnames = ["."]
    for dirname in dirnames:
        try:
            filenames = os.listdir(dirname)
        except OSError, err:
            print >>sys.stderr, err
            continue
        for filename in filenames:
            fullname = os.path.join(dirname, filename)
            try:
                print table[detec.istextfile(fullname)], repr(fullname)[1:-1]
            except IOError:  # eg, this is a directory
                pass
    
if __name__ == "__main__":
    main(sys.argv)
   
