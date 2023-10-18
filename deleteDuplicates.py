# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 19:12:32 2023

@author: MarcA
"""

folderFrom = r"C:\Users\MarcA\OneDrive - afacademy.af.edu\Pictures"
folderFrom = r"C:\Users\MarcA\OneDrive - afacademy.af.edu\Music"
folderFrom = r"C:\Users\MarcA\OneDrive - afacademy.af.edu\Videos"
folderFrom = r"C:\Users\MarcA\OneDrive - afacademy.af.edu\Documents"
folderFrom = r"C:\Users\MarcA\OneDrive - afacademy.af.edu\[X] Personal"
folderTo = "D:\Pictures"
folderTo = "D:\Music"
folderTo = r"D:\Videos"
folderTo = r"D:\Documents"
folderTo = "D:\OneDrive backup\Personal"
folderFrom, folderTo = r"C:\Users\MarcA\OneDrive - afacademy.af.edu\[X] Done with",r"D:\OneDrive backup\[X] Done with"
folderFrom, folderTo = r"C:\Users\MarcA\OneDrive - afacademy.af.edu\[X] MuseScore projects","D:\OneDrive backup\[X] MuseScore projects"
folderFrom, folderTo = r"C:\Users\MarcA\OneDrive - afacademy.af.edu\Desktop",r"D:\OneDrive backup\Desktop"
folderFrom, folderTo = r"C:\Users\MarcA\OneDrive - afacademy.af.edu\[] Jupyter Notebook",r"D:\OneDrive backup\Jupyter Notebook"
folderFrom, folderTo = r"C:\Users\MarcA\OneDrive - afacademy.af.edu", "D:/"

foldersToIgnore = ['D:/DeliveryOptimization']

import os
from filecmp import cmp
from tqdm import tqdm

def filePathsIn(folderPath):
    for folder in foldersToIgnore:
        if folder in folderPath:
            return []
    folderPath = folderPath.replace('\\','/')
    if os.path.isfile(folderPath) or '.' in folderPath.split('/')[-1]:
        return [folderPath]
    filePathsHere = list()
    names = os.listdir(folderPath)
    for name in names:
        subPath = folderPath+'/'+name
        subPath = subPath.replace('//','/')
        filePathsHere.extend(filePathsIn(subPath))
    return filePathsHere

print("Finding files to delete...")
filesFromList = filePathsIn(folderFrom)
print("Finding files to compare against")
filesToList   = filePathsIn(folderTo)

def check_pairs(pairs):
    for pair in tqdm(pairs):
        fileFrom, fileTo = pair
        assert os.path.exists(fileTo)
        if os.path.exists(fileFrom):
            try:
                same = cmp(fileFrom, fileTo)
            except:
                print("Could not compare following 2 files:",fileFrom,fileTo)
            else:
                if same:
                    try:
                        os.remove(fileFrom)
                    except:
                        print("failed to delete",fileFrom)
pairs = list()
print("Checking which files are in equivalent locations in both folders...")
len_folderFrom = len(folderFrom)
filesToSet = set(filesToList)
folderTo = folderTo.replace('\\','/').replace('//','/')
for fileFrom in tqdm(filesFromList):
    fileFromPart = fileFrom[len_folderFrom:]
    equivalentFileTo = folderTo + fileFromPart
    if equivalentFileTo in filesToSet:
        pairs.append((fileFrom,equivalentFileTo))

print("Deleting duplicate files in equivalent locations in both folders...")
check_pairs(pairs)

filesFromDict = dict()
filesToDict   = dict()
print("Sizing files from input...")
for file in filesFromList:
    try:
        size = os.path.getsize(file)
    except:
        print("Could not size",file)
    else:
        filesFromDict[file] = size
print("Sizing files from output...")
for file in filesToList:
    try:
        size = os.path.getsize(file)
    except:
        print("Could not size",file)
    else:
        filesToDict[file]   = size

filesFromList = filesFromDict.keys()
filesToList = filesToDict.keys()

fileSizes = list(filesFromDict.values()) + list(filesToDict.values())
fileSizes = set(fileSizes)
#fileSizes = list(fileSizes)
#fileSizes = sorted(fileSizes)

print("Grouping files by size from both input and output...")
pairs = list()
for fileSize in tqdm(fileSizes):
    filesFrom = [x for x in filesFromList if filesFromDict[x] == fileSize]
    filesTo   = [x for x in  filesToList  if filesToDict[x] == fileSize]
    for fileFrom in filesFrom:
        for fileTo in filesTo:
            pairs.append((fileFrom, fileTo))



print("Comparing files of same size and deleting old files...")
check_pairs(pairs)
pairs = list()

def deleteEmptyFolders(folderPath):
    folderPath = folderPath.replace('\\','/')
    # if this is a file, do nothing
    if os.path.isfile(folderPath) or '.' in folderPath.split('/')[-1]:
        try:
            os.path.getsize(folderPath)
        except:
            try:
                os.remove(folderPath)
            except:
                print("failed to delete",folderPath)
        return
    names = os.listdir(folderPath)
    # if not empty, recurse on all contents
    for name in names:
        subPath = folderPath + '/' + name
        deleteEmptyFolders(subPath)
    # if empty folder, delete empty folder
    if len(names) == 0:
        try:
            os.removedirs(folderPath)
        except:
            print("failed to delete",folderPath)
        return

print("Deleting empty folders")
deleteEmptyFolders(folderFrom)

if True:
    for fileFrom in filesFromList:
        for fileTo in filesToList:
            pairs.append((fileFrom, fileTo))
            
print("Comparing all files and deleting old copies")
check_pairs(pairs)

deleteEmptyFolders(folderFrom)