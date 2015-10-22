#coding=utf-8
#!/usr/bin/python
'''
a module in SPARROW
copyright Hong-Bo Zhang
postprocess such as modification of symmetry number
'''

import os
import re
from xml.dom import minidom

class PostProcessClass:
    'post process'

    def __init__(self,Path):
        'set path'
        self.Path = os.path.normpath(Path)
        self.symNumSpecies = []
        self.symNumArray = []
        self.symNumDic = {}
        

    def ReadSymmetryNumber(self):
        'read symmetry number from symmetryNumber.dat'

        self.symNumFile = os.path.normpath(self.Path + '/symmetryNumber.dat')
        self.symNumFileIO = open(self.symNumFile,'r')
        self.symNumFileLength = len(self.symNumFileIO.readlines())
        self.symNumFileIO.close()

        self.symNumFileIO = open(self.symNumFile,'r')
        self.symNumString = self.symNumFileIO.read()
        #re.search('( *)Name( +)sym( *)\n(((\w+)( +)(\d+)\n)+)',self.symNumString,re.I).group()
        self.symNumTemp = re.search('(((\w+)( +)(\d+)\n)+)',self.symNumString,re.I).group()
        self.symNumTemp2 = re.sub(' +',',',re.sub('\n',' ',self.symNumTemp).strip()).split(',')
        for i in range((len(self.symNumTemp2)+1)/2):
            self.symNumSpecies.append(self.symNumTemp2[2*i])
            self.symNumArray.append(self.symNumTemp2[2*i+1])
        self.symNumFileIO.close()

        for i in range(len(self.symNumSpecies)):
            self.symNumDic[self.symNumSpecies[i]] = self.symNumArray[i]
        print self.symNumDic
        #print range(len(self.symNumTemp2))
        #print self.symNumTemp
        #print self.symNumTemp2
        #print self.symNumSpecies
        #print self.symNumArray


    def SymmetryNumberMESMER(self,MESMERxml):
        'modify symmetry numbers in *.xml. Bath gas (Ar,He...) must be the last on in <moleculeList>'

        self.symNumFileIO = open(MESMERxml,'r')
        self.symNumString = self.symNumFileIO.read()
        self.symNumFileIO.close()

        self.symNumSpeciesTemp = re.findall('<molecule id="(\w+)">',self.symNumString)
        for i in range(len(self.symNumDic)):
            self.symNumString = re.sub('1\?\?\?',self.symNumDic[self.symNumSpeciesTemp[i]],self.symNumString,count=1)
         
        self.symNumFileIO = open(MESMERxml,'w')
        self.symNumFileIO.write(self.symNumString)
        self.symNumFileIO.close()


    def SymmetryNumberMESMERFiles(self):
        'modify symmetry numbers in Path/MESMER/*.xml.'

        # directory issue
        self.symNumPath = os.path.normpath(self.Path + '/MESMER/')
        self.symNumMESMERxmlFiles = os.listdir(self.symNumPath)
        for i in self.symNumMESMERxmlFiles:
            if not re.search('\.xml',i,re.I) : self.symNumMESMERxmlFiles.remove(i)

        for i in self.symNumMESMERxmlFiles:
            self.SymmetryNumberMESMER(os.path.normpath(self.symNumPath + '/' + i))


    def SymmetryNumberThermo(self,Thermodat):
        'modify symmetry numbers in Thermo input files *.dat, including /Keq and /ctst'

        self.symNumFileIO = open(Thermodat,'r')
        self.symNumString = self.symNumFileIO.read()
        self.symNumFileIO.close()

        self.symNumSpeciesTemp = re.findall('(?:reac|ctst|prod)(?: +)(\w+)(?: +)-{0,1}(?:\d+)(?:\.*)(?:\d*)',self.symNumString)
        for i in range(len(self.symNumSpeciesTemp)):
            self.symNumString = re.sub('1\?\?\?',self.symNumDic[self.symNumSpeciesTemp[i]],self.symNumString,count=1)
         
        self.symNumFileIO = open(Thermodat,'w')
        self.symNumFileIO.write(self.symNumString)
        self.symNumFileIO.close()

    
    def SymmetryNumberThermoFiles(self):
        'modify symmetry numbers in Path/Thermo/Keq/*.dat and Path/Thermo/ctst/*.dat.'

        # Keq
        self.symNumPath = os.path.normpath(self.Path + '/Thermo/Keq/')
        self.symNumThermodatFiles = os.listdir(self.symNumPath)
        for i in self.symNumThermodatFiles:
            if not re.search('\.dat',i,re.I) : self.symNumThermodatFiles.remove(i)
        for i in self.symNumThermodatFiles:
            self.SymmetryNumberThermo(os.path.normpath(self.symNumPath + '/' + i))

        # ctst
        self.symNumPath = os.path.normpath(self.Path + '/Thermo/ctst/')
        self.symNumThermodatFiles = os.listdir(self.symNumPath)
        for i in self.symNumThermodatFiles:
            if not re.search('\.dat',i,re.I) : self.symNumThermodatFiles.remove(i)
        for i in self.symNumThermodatFiles:
            self.SymmetryNumberThermo(os.path.normpath(self.symNumPath + '/' + i))


    def SymmetryNumberMultiWell(self,MultiWelldat):
        'modify symmetry numbers in MultiWell input files *.dat'

        self.symNumFileIO = open(MultiWelldat,'r')
        self.symNumString = self.symNumFileIO.read()
        self.symNumFileIO.close()

        self.symNumSpeciesTemp1 = re.findall('\n(?:\d+)(?: +)([A-Za-z]\w*)(?: +)(?:.+?)(?: +)(?:.+?)(?: +)1\?\?\?',self.symNumString)
        self.symNumSpeciesTemp2 = re.findall('\n(?:\d+)(?: +)(?:\d+)(?: +)([A-Za-z]\w*)(?: +)(?:.+?)(?: +)1\?\?\?',self.symNumString)
        self.symNumSpeciesTemp = self.symNumSpeciesTemp1 + self.symNumSpeciesTemp2
        for i in range(len(self.symNumSpeciesTemp)):
            self.symNumString = re.sub('1\?\?\?',self.symNumDic[self.symNumSpeciesTemp[i]],self.symNumString,count=1)
         
        self.symNumFileIO = open(MultiWelldat,'w')
        self.symNumFileIO.write(self.symNumString)
        self.symNumFileIO.close()


    def SymmetryNumberMultiWellFiles(self):
        'modify symmetry numbers in Path/MultiWell/*.dat'

        self.symNumPath = os.path.normpath(self.Path + '/MultiWell/')
        self.symNumMultiWelldatFiles = os.listdir(self.symNumPath)
        for i in self.symNumMultiWelldatFiles:
            if not re.search('\.dat',i,re.I) : self.symNumMultiWelldatFiles.remove(i)
        for i in self.symNumMultiWelldatFiles:
            self.SymmetryNumberMultiWell(os.path.normpath(self.symNumPath + '/' + i))
        

    def SymmetryNumber(self):
        'symmetry number driver. modify symmetry number in all the input files of MESMER,Thermo,MultiWell'

        self.ReadSymmetryNumber()
        self.SymmetryNumberThermoFiles()
        self.SymmetryNumberMESMERFiles()
        self.SymmetryNumberMultiWellFiles()
 



##########################END#########################

if __name__ == '__main__':
    path = 'C:\Users\dodo\Desktop\soothair_singlet\R51C4H2branch'
    #'E:\Research\soothair_g09\R71C2H2'
    #post = PostProcessClass(os.path.normpath(os.getcwd()+'/R512ndSiteA/'))
    post = PostProcessClass(os.path.normpath(path))
    #post = PostProcessClass('C:\\Users\\dodo\\Desktop\\soothair_2nd\\2_Systems_FullRev\\R51_C4H2')
    post.SymmetryNumber()
    #post.SymmetryNumberMESMER(os.path.normpath(os.getcwd()+'/R512ndSiteA/MESMER/atest.xml')) ## for single xml file
    #post.SymmetryNumberThermo(os.path.normpath(os.getcwd()+'/R512ndSiteA/Thermo/Keq/atest.dat')) ## for single Keq dat file
    #post.SymmetryNumberThermo(os.path.normpath(os.getcwd()+'/R512ndSiteA/Thermo/ctst/atest.dat')) ## for single ctst dat file
    #post.SymmetryNumberMultiWell(os.path.normpath(os.getcwd()+'/R512ndSiteA/MultiWell/atest.dat')) ## for single MultiWell dat file
