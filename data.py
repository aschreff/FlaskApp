import string
import math
import csv

def readRecipes():
    recipeList = []
    d = {}
    with open("static/sheet.csv") as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            recipeList = row
            break
    return recipeList

def readRecipeDict():
    recipeList = []
    d = {}
    with open("static/sheet.csv") as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            recipeList = row
            break
    i = 0
    for elem in recipeList:
        d[elem] = i
        i += 1
    return d

def readWashMatrix():
    mat = []
    first = True
    with open("static/sheet.csv") as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            if(not first):
                mat.append(row)
            first = False
    return mat

def createDirections(wash):
    rawDirs = getRawDirs(wash)
    listDirs = thinRawDirs(rawDirs)
    return listDirs

def getRawDirs(wash):
    result = []
    adding = False
    with open("static/sheet.csv") as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            if(adding):
                result.append(row)
            for elem in row:
                if(elem != "" and elem == "$%s"%wash):
                    adding = True
                    break
                elif(elem != "" and elem[0] == "$"):
                    adding = False
                    break         
    return result

def thinRawDirs(rawDirs):
    result = []
    for row in range(len(rawDirs)):
        result.append(rawDirs[row][0])
    result.pop()
    return result

