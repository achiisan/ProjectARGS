#!/usr/bin/python

class Parser:
    def __init__(self):
        print("Hello World")
     
    @staticmethod
    def fileread(filename):
        file = open(filename, 'r', 1)
        print(file);
        
        filebuf = file.read();
        
        return filebuf

filebuf = Parser.fileread("../schedule-list/classlist-2015-1.csv");

print(filebuf);