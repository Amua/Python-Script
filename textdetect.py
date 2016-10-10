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
   
