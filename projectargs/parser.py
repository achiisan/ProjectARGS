#!/usr/bin/python


#==========================================================
#FILE PARSER 
# INPUT / OUTPUT FILES

class Parser:

     
    @staticmethod
    def fileread(filename):
        file = open(filename, 'r', 1)
        print(file);
        
        filebuf = file.read();
        
        return filebuf


