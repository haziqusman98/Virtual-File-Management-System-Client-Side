import sys
import math
import os.path
from .datStream import datStream
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 17:16:37 2019

@author: Haziq Usman
        Moeed Ahmad
"""


def max_level(n):
    max = -1
    while(n > max):
        max = n
    return max


def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))


class Metadata:
    def __init__(self):
        self.parentToChild = dict()
        self.parentToFile = dict()

    def printself(self):
        print(self.parentToChild, self.parentToFile)


class Directory:
    level = 0

    def __init__(self, prevLevel=0):
        self.fileNames = {}
        self.files = {}
        self.fid = 0
        self.pid = 0
        self.parent = "."
        self.pdir = []
        self.pcontent = ""
        self.dirName = "root"
        self.subDirCount = 0
        self.level = prevLevel + 1
        self.children = []

    def add_child(self):
        self.children.append(Directory(self.level))
        self.subDirCount = self.subDirCount + 1

    def create_file(self, fname):
        self.fid = self.fid + 1
        self.fileNames[self.fid] = fname
        self.files[self.fid, 0] = self.pcontent

    def showMemoryMap(self):
        print("Current Directory: " + self.dirName)
        for key, value in list(self.fileNames.items()):
            for [key1, key2] in list(self.files.keys()):
                if(key1 == key):
                    print(self.dirName + "   |   " +
                          str(key2) + "   |   " + value)
        for child in self.children:
            print("Current Directory: " + child.dirName)
            for key, value in list(child.fileNames.items()):
                for [key1, key2] in list(child.files.keys()):
                    if(key1 == key):
                        print(child.dirName + "   |   " +
                              str(key2) + "   |   " + value)


class FileSystem:
    root = Directory()
    currDir = root

    def create(self, fname):
        self.currDir.create_file(fname)

    def delete(self, fname):
      for key, value in list(self.currDir.fileNames.items()):
          if value == fname:
            del self.currDir.fileNames[key]
            for [key1, key2] in list(self.currDir.files.keys()):
                if key1 == key:
                    del self.currDir.files[key1, key2]

    def mkdir(self, dirName):
        self.currDir.add_child()
        child = self.currDir.children[self.currDir.subDirCount-1]
        child.pdir.append(self.currDir)
        child.parent = self.currDir.dirName
        child.dirName = dirName

    def chdir(self, dirName):
        if (dirName == "."):
            for parent in self.currDir.pdir:
                self.currDir = parent
                return
        else:
            for child in self.currDir.children:
                if child.dirName == dirName:
                    self.currDir = child
                    return
        print(dirName + " does not exist")

    def write_to_file(self, fname, text, write_at=None):
        if write_at == None:
            chunks = list(chunkstring(text, 25))
            for key, value in list(self.currDir.fileNames.items()):
                if value == fname:
                    for chunk in chunks:
                        self.currDir.files[key, self.currDir.pid] = chunk
                        self.currDir.pid = self.currDir.pid + 1
        else:
            pg = math.floor(int(write_at)/25)
            for key, value in list(self.currDir.fileNames.items()):
                if value == fname:
                    for [key1, key2], value in list(self.currDir.files.items()):
                        if key1 == key and key2 == pg:
                            rest1 = value[:int(write_at)]
                            rest2 = value[int(write_at):]
                            self.currDir.files[key1,
                                key2] = rest1 + text + rest2

    def move(self, source_fname, target_dirName):
        temp = ""
        curr_fol = self.currDir
        for key, value in list(self.currDir.fileNames.items()):
            if value == source_fname:
                for [key1, key2], value1 in list(self.currDir.files.items()):
                    if key1 == key:
                        temp += value1
        self.delete(source_fname)
        for child in self.currDir.children:
               if child.dirName == target_dirName:
                   self.currDir = child
        self.create(source_fname)
        self.write_to_file(source_fname, temp)
        self.currDir = curr_fol

    def read_from_file(self, fname, start=None, size=None):
        temp = ""
        if start == None and size == None:
            for key, value in list(self.currDir.fileNames.items()):
                if value == fname:
                    for [key1, key2], value in list(self.currDir.files.items()):
                        if key1 == key:
                             temp += value
            return temp
        else:
            for key, value in list(self.currDir.fileNames.items()):
                if value == fname:
                    for [key1, key2], value in list(self.currDir.files.items()):
                        if key1 == key:
                            temp += value
            return temp[start:(start+size-1)]

    def move_within_file(self, fname, start, size, target):
        temp = ""
        pg1 = math.floor(start/25)
        pg2 = math.floor(target/25)
        for key, value in list(self.currDir.fileNames.items()):
                if value == fname:
                    for [key1, key2], value in list(self.currDir.files.items()):
                        if key1 == key and key2 == pg1:
                            temp = value[start:(start+size-1)]
                            rest1 = value[:start]
                            rest2 = value[(start+size):]
                            self.currDir.files[key1, key2] = rest1 + rest2
                    for [key1, key2], value in list(self.currDir.files.items()):
                        if key2 == pg2:
                            rest1 = value[:target]
                            rest2 = value[target:]
                            self.currDir.files[key1,
                                key2] = rest1 + temp + rest2

    def truncate_file(self, fname, maxSize):
        temp = ""
        for key, value in list(self.currDir.fileNames.items()):
                if value == fname:
                    for [key1, key2], value in list(self.currDir.files.items()):
                        if key1 == key:
                            temp += value
                            del self.currDir.files[key1, key2]
                    del self.currDir.fileNames[key]
        self.create(fname)
        self.write_to_file(fname, temp[:maxSize])

    def get_last_dir(self):
         for child in self.currDir.children:
                    self.currDir = child
         return self.currDir.level

    def recurse(self):
        for key, value in list(self.currDir.fileNames.items()):
                y = "-"
                y = y + "-" + value
                print(y)
        for child in self.currDir.children:
                x = "-"
                x = x + "-" + child.dirName
                print(x)
                self.currDir = child


def main(dire, ip, port):
    ds = datStream()
    fileSystem = FileSystem()
    fileSystem.root = dire
    fileSystem.currDir = dire
    loop = True

    while (loop):  # While loop which will keep going until loop = False
        print_menu()  # Displays menu
        choice = input("Enter your choice [1-13]: ")

        if choice == '1':
            fname = input("Enter File Name: ")
            fileSystem.create(fname)
            print(fname + " created")
            ds.dump(fileSystem.root, ip, port)
        elif choice=='2':
            fname= input("Enter File Name: ")
            fileSystem.delete(fname)
            print (fname + " deleted")
            ds.dump(fileSystem.root, ip, port)
        elif choice=='3':
            print ("Make Directory")
            dirName = input("Enter the name of directory: ")
            fileSystem.mkdir(dirName)
            print(dirName + " created")
            ds.dump(fileSystem.root, ip, port)
        elif choice=='4':
            print ("Change Directory")
            dirName = input("Directory name: ")
            fileSystem.chdir(dirName)
            if fileSystem.currDir.dirName == dirName:
                print("Directory changed to: " + dirName)
            else:
                print("Directory not changed!")
            ds.dump(fileSystem.root, ip, port)
        elif choice=='5':
            print ("Move File")
            fname = input("Enter file name to move: ")
            dirName = input("Enter target folder: ")
            fileSystem.move(fname,dirName)
            print(fname + " moved to directory " + dirName)
            ds.dump(fileSystem.root, ip, port)
        elif choice=='6':
            print ("Write to File")
            fname = input("Enter file name to write into: ")
            content = input("Enter text to write into file: ")
            fileSystem.write_to_file(fname, content)
            ds.dump(fileSystem.root, ip, port)
        elif choice=='7':
            print ("Write to file at certain position")
            fname = input("Enter file name to write into: ")
            content = input("Enter text to write into file: ")
            pos = input("Enter position at which you want to write in the file: ")
            fileSystem.write_to_file(fname, content, pos)
            ds.dump(fileSystem.root, ip, port) 
        elif choice=='8':
            print ("Read File")
            fname = input("Enter file name to read from: ")
            print(fileSystem.read_from_file(fname))
            ds.dump(fileSystem.root, ip, port)
        elif choice=='9':
            print ("Read part of the file")
            fname = input("Enter file name to read from: ")
            pos = int(input("Enter position to start reading from: "))
            end = int(input("Enter number of characters you want to read: "))
            print(fileSystem.read_from_file(fname, pos, end))
            ds.dump(fileSystem.root, ip, port)
        elif choice=='10':
            print ("Move within file")
            fname = input("Enter file name to be manipulated: ")
            start = int(input("Enter the position from where you want to cut the text: "))
            size = int(input("Enter the number of characters to cut: "))
            target = int(input("Enter the position where you want to place the text that was cut: "))
            fileSystem.move_within_file(fname, start, size, target)
            ds.dump(fileSystem.root, ip, port)
        elif choice=='11':
            print ("Truncate File")
            fname = input("Enter file name to be truncated: ") 
            size = int(input("Enter the size of file you want to sustain: "))
            fileSystem.truncate_file(fname, size)
            ds.dump(fileSystem.root, ip, port) 
        elif choice=='12':
            print ("Memory map: ")
            dire.showMemoryMap() 
        elif choice=='13':
            print ("Exit")
            # You can add your code or functions here
            loop=False # This will make the while loop to end as now value of loop is set to False
        else:
            # Any integer inputs other than values 1-5 we print an error message
            print("Wrong option selection. Enter any key to try again..")
        
    return 0

def print_menu():       ## Your menu design here
    print (30 * "-" , "MENU" , 30 * "-")
    print ("1. Create file")
    print ("2. Delete File")
    print ("3. Make Directory")
    print ("4. Change Directory")
    print ("5. Move")
    print ("6. Write to File")
    print ("7. Write to File at")
    print ("8. Read From File")
    print ("9. Read from File at")
    print ("10. Move within file")
    print ("11. Truncate file")
    print ("12. Show memory map")
    print ("13. Exit")
    print (67 * "-")
 
