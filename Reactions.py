#coding = utf-8
#!/usr/bin/python
'''
a module in SPARROW
copyright Hong-Bo Zhang
read a PES and generate input files for MESMER and MultiWell
'''

import DataClass
import OutputMolecules
import UnitConvert
import os
import re
import math
from xml.dom import minidom


class ReactionsIniClass:
    'method related to inifile'

    def __init__(self,iniFile):
        'Set default vaule and read parameters from *.ini for further usage in generating MESMER/MultiWell input'
        #set initial value
        self.iniFilePath = os.path.dirname(iniFile)
        self.ReactionGaussianPath = os.path.normpath(os.path.dirname(iniFile)+'/Gaussian')
        self.ReactionGaussianName = os.listdir(os.path.normpath(os.path.dirname(iniFile)+'/Gaussian'))
        self.MESMERTopHill = 120
        self.MESMERGrainSize = 100
        self.MultiWellDoubleArray = (10,   10000,   14000,   300000,   2113989025)

        # Determined the number of reactions
        self.FileIO = open(iniFile,'r')
        self.NumberofReactions = len(self.FileIO.readlines()) - 5
        self.Reactants = [' ' for i in range(self.NumberofReactions)]
        self.TranStats = [' ' for i in range(self.NumberofReactions)]
        self.Products = [' ' for i in range(self.NumberofReactions)]
        self.Tunneling = ['NO' for i in range(self.NumberofReactions)]
        self.Reversible = ['YES' for i in range(self.NumberofReactions)]
        self.Excess = ['' for i in range(self.NumberofReactions)]
        self.ExcessMoleFraction = [0.0 for i in range(self.NumberofReactions)]
        self.FileIO.close()
        #read MESMER and MultiWell settings from *.ini
        self.FileIO = open(iniFile,'r')
        print "Reading Reation IniFile: ",self.FileIO.name
        self.String = self.FileIO.readline()
        if self.String == 'MESMER:Default\n':
            print 'MESMER: using default settings'
        elif re.search('( *)(\d*)(\.*)(\d*)( +)(\d*)(\.*)(\d*)( *)\n',self.String):
            self.MESMERTopHill =  re.sub(' +',',',self.String.strip()).split(',')[0]
            self.MESMERGrainSize =  re.sub(' +',',',self.String.strip()).split(',')[1]
            print self.MESMERTopHill,self.MESMERGrainSize
        else:
            print 'Warning: MESMER setting in inifile is not correct.'
        self.String = self.FileIO.readline()
        if self.String == 'MultiWell:Default\n':
            print 'MultiWell: using default settings'
        else:
            print 'Warning: MultiWell settings: NOT Supported in this version'

        # read Temp and Pres
        self.String = self.FileIO.readline()
        if re.search('( *)T( *)=( *)\((((.*?),)*)(.*?)\)',self.String):
            self.Temp = [0 for i in range(len(re.sub('T( *)=( *)\(','',self.String.strip()).replace(')','').split(',')))]
            for i in range(len(re.sub('T( *)=( *)\(','',self.String.strip()).replace(')','').split(','))):
                self.Temp[i] = float(re.sub('T( *)=( *)\(','',self.String.strip()).replace(')','').split(',')[i])
        else :
            print 'Warning: Temperature range: incorrect'
        self.String = self.FileIO.readline()
        if re.search('( *)P( *)=( *)\((((.*?),)*)(.*?)\)',self.String):
            self.Pres = [0 for i in range(len(re.sub('P( *)=( *)\(','',self.String.strip()).replace(')','').split(',')))]
            for i in range(len(re.sub('P( *)=( *)\(','',self.String.strip()).replace(')','').split(','))):
                self.Pres[i] = float(re.sub('P( *)=( *)\(','',self.String.strip()).replace(')','').split(',')[i])
        else :
            print 'Warning: Pressure range: incorrect'

        # read reactions
        self.String = self.FileIO.readline()
        if self.String == '\n':
            self.String = self.FileIO.readline()
        else :
            print 'Warning: There should be a blanck line under Pressure range line'
        if self.String == '\n': print 'Warning: There should be only one blanck line under Pressure range line'
        print 'There are %d reactions in %s'%(self.NumberofReactions,iniFile)
              
        for i in range(self.NumberofReactions):
            if re.search('^( *)\(',self.String):
                self.Reactants[i] = re.search('^( *)\((.*?)\)',self.String).group().strip()
            else :
                self.Reactants[i] = re.search('^( *)(\w+?) ',self.String).group().strip()

            self.String = self.String.replace(self.Reactants[i],'')
            #print self.Reactants
            #print self.String

            self.TranStats[i] = re.search('^( *)(\w+?) ',self.String).group().strip()
            self.String = self.String.replace(self.TranStats[i],'')
            #print self.TranStats
            #print self.String

            if re.search('^( *)\(',self.String):
                self.Products[i] = re.search('^( *)\((.*?)\)',self.String).group().strip()
            else :
                self.Products[i] = re.search('^( *)(\w+?) ',self.String).group().strip()

            self.String = self.String.replace(self.Products[i],'')
            #print self.Products
            #print self.String

            if re.search('( *)NOTUN( )',self.String):
                self.Tunneling[i] = 'NO'
                self.String = self.String.replace('NOTUN','')
            elif re.search('( *)TUN( )',self.String):
                self.Tunneling[i] = 'YES'
                self.String = self.String.replace('TUN','')
            else :
                print 'Warning: Tunneling session has some problem'
            #print self.Tunneling
            #print self.String

            if re.search('( *)NOREV',self.String):
                self.Reversible[i] = 'NO'
                self.String = self.String.replace('NOREV','')
            elif re.search('( *)REV',self.String):
                self.Reversible[i] = 'YES'
                self.String = self.String.replace('REV','')
            else:
                print 'Warning: Reverisbility session has some problem'
            #print self.Reversible
            #print self.String

            if (self.String.strip() == '' or self.String.strip() == '\n'):
                print ('Reaction %d has been read'%(i+1))
            else :
                self.Excess[i] = re.search('( *)(\w+) ',self.String).group().strip()
                #print self.Excess
                self.String = self.String.replace(self.Excess[i],'')
                #print self.String
                self.ExcessMoleFraction[i] = float(re.search('( *)(\d*)\.(\d*)',self.String).group().strip())
                self.String = self.String.replace(re.search('( *)(\d*)\.(\d*)',self.String).group(),'')
                #print self.ExcessMoleFraction
                if (self.String.strip() == '' or self.String.strip() == '\n'):
                    print ('Reaction %d has been read'%(i+1))
                else:
                    print 'Warning: some problem was encountered in reading Reaction 1'
            self.String = self.FileIO.readline()

        #print self.FileIO.readline()
        print self.Reactants
        print self.TranStats
        print self.Products 
        print self.Tunneling 
        print self.Reversible 
        print self.Excess 
        print self.ExcessMoleFraction 

        # close *.ini
        self.FileIO.close()
        del self.String
        print "Closing Reation IniFile: ",self.FileIO.name        


    def OutputReactions(self):
        'read all the .log/.out files and write the key informations into files'

        # setting file and path
        for i in self.ReactionGaussianName:
            if not re.search('\.log|\.out',i,re.I) : self.ReactionGaussianName.remove(i)
           
        # Read Gaussian output one by one
        for i in self.ReactionGaussianName:
            self.Moli = DataClass.MoleculeClass(self.ReactionGaussianPath,re.sub('\.[Ll][Oo][Gg]|\.[Oo][Uu][Tt]','',i))
            self.Moli.ReadGaussian(0)
            OutputMolecules.WriteMolintoFile(self.Moli)

        print 'All the Gaussian output files under '+self.ReactionGaussianPath+' have been read'


    def WriteJmolReactions(self):
        'generate *.jpg and *.avi or *.gif to visualize a molecule'
        
        # setting file and path
        for i in self.ReactionGaussianName:
            if not re.search('\.log|\.out',i,re.I) : self.ReactionGaussianName.remove(i)
           
        # Read Gaussian output one by one
        for i in self.ReactionGaussianName:
            self.Moli = DataClass.MoleculeClass(self.ReactionGaussianPath,re.sub('\.[Ll][Oo][Gg]|\.[Oo][Uu][Tt]','',i))
            self.Moli.ReadGaussian(0)
            OutputMolecules.WriteJmol(self.Moli)

        print 'All the Gaussian output files under '+self.ReactionGaussianPath+' have been converted to *.jpg and/or *.gif *.avi'


    def WriteSupInfoLaTexReactions(self):
        'read all the .log/out files and write them into *.tex files, subsequently compile them to *.dvi *.ps and *.pdf'
        
        # setting file and path
        for i in self.ReactionGaussianName:
            if not re.search('\.log|\.out',i,re.I) : self.ReactionGaussianName.remove(i)
           
        # Read Gaussian output one by one
        for i in self.ReactionGaussianName:
            self.Moli = DataClass.MoleculeClass(self.ReactionGaussianPath,re.sub('\.[Ll][Oo][Gg]|\.[Oo][Uu][Tt]','',i))
            self.Moli.ReadGaussian(0)
            OutputMolecules.WriteSupInfoLaTeX(self.Moli)

        print 'All the Gaussian output files under '+self.ReactionGaussianPath+' have been converted to *.tex *.dvi *.ps and *.pdf'
        

    def WriteMathematica(self):
        'Generate some code fragments for mathematica'


        # read Gaussian *.log/out as DataClass.MoleculeClass
        self.ReactionGaussianNameTemp = [0 for i in range(len(self.ReactionGaussianName))]
        for i in range(len(self.ReactionGaussianName)):
            self.ReactionGaussianNameTemp[i] = self.ReactionGaussianName[i]
        for i in self.ReactionGaussianNameTemp:
            if not re.search('\.log|\.out',i,re.I) : self.ReactionGaussianName.remove(i)
        self.Mol = [0 for i in range(len(self.ReactionGaussianName))]
        for i in range(len(self.ReactionGaussianName)):
            self.Mol[i] = DataClass.MoleculeClass(self.ReactionGaussianPath,re.sub('\.[Ll][Oo][Gg]|\.[Oo][Uu][Tt]','',self.ReactionGaussianName[i]))
            self.Mol[i].ReadGaussian(0)    

        # file and path
        self.PESPath = os.path.normpath(self.iniFilePath + '/PES/' )
        if not os.path.exists(self.PESPath): os.mkdir(self.PESPath)

        self.PESInp = open(os.path.normpath(self.PESPath + '/nbFragment.dat'),'w')

        # Species Specification
        self.PESInp.write('Created by SPARROW\n\n\n')
        self.PESInp.write('(*Species Specification*)\n')
        self.PESReac = {}
        self.PESProd = {}
        self.PESIntM = {}
        self.PESTraS = {}

        # Reac, Prod, IntM in PES.nb
        for i in self.Reactants:
            if i in self.Products:
                self.PESIntM[i] = 1
            else :
                self.PESReac[i] = 1
        for i in self.Products:
            if i in self.Reactants:
                self.PESIntM[i] = 1
            else :
                self.PESProd[i] = 1
        for i in self.TranStats:
            self.PESTraS[i] = 1
        self.PESInp.write('numReac = %d;\n' % len(self.PESReac.keys()))
        self.PESInp.write('numProd = %d;\n' % len(self.PESProd.keys()))
        self.PESInp.write('numIntM = %d;\n' % len(self.PESIntM.keys()))
        self.PESInp.write('numTraS = %d;\n' % self.NumberofReactions)

        # Species Energy with zero-point correction
        self.PESInp.write('(*Species Eenergy with zero-point correction*)\n')

        self.EReacString = "EReac = {"
        self.EReacComment = "(*"
        for i in self.PESReac.keys():        
            if re.search('\(',i):
                self.PESReacTemp = re.sub(' +',',',i.replace('(','').replace(')','').strip()).split(',')
                for itest in range(len(self.ReactionGaussianName)): # find the molecule index from its name
                    if self.Mol[itest].MolName == self.PESReacTemp[0]: ireac = itest           
                self.PESReacZPEtemp0 = UnitConvert.EnergyConvert(InE=self.Mol[ireac].EleEnergy,InUnit='Har',OutUnit='Har')+UnitConvert.EnergyConvert(InE=sum(self.Mol[ireac].Freq)*self.Mol[ireac].ScaleFactor/2,InUnit='K',OutUnit='Har') # ZPE
                for itest in range(len(self.ReactionGaussianName)): # find the molecule index from its name
                    if self.Mol[itest].MolName == self.PESReacTemp[1]: ireac = itest           
                self.PESReacZPEtemp1 = UnitConvert.EnergyConvert(InE=self.Mol[ireac].EleEnergy,InUnit='Har',OutUnit='Har')+UnitConvert.EnergyConvert(InE=sum(self.Mol[ireac].Freq)*self.Mol[ireac].ScaleFactor/2,InUnit='K',OutUnit='Har') # ZPE
                self.EReacString = self.EReacString + ' ' + str(self.PESReacZPEtemp0) + ' + ' + str(self.PESReacZPEtemp1)+','
                self.EReacComment= self.EReacComment + ' ' + re.sub(' +','+',i.replace('(','').replace(')','').strip()) + ','
            else :
                for itest in range(len(self.ReactionGaussianName)): # find the molecule index from its name
                    if self.Mol[itest].MolName == i: ireac = itest           
                self.PESReacZPEtemp = UnitConvert.EnergyConvert(InE=self.Mol[ireac].EleEnergy,InUnit='Har',OutUnit='Har')+UnitConvert.EnergyConvert(InE=sum(self.Mol[ireac].Freq)*self.Mol[ireac].ScaleFactor/2,InUnit='K',OutUnit='Har') # ZPE
                self.EReacString = self.EReacString + ' '+str(self.PESReacZPEtemp)+','
                self.EReacComment= self.EReacComment + ' ' + i  +','             
        self.EReacString = re.sub(',$','',self.EReacString) + "} " + re.sub(',$','',self.EReacComment) + " *);\n"
        self.PESInp.write(self.EReacString)

        self.EProdString = "EProd = {"
        self.EProdComment = "(*"
        for i in self.PESProd.keys():        
            if re.search('\(',i):
                self.PESProdTemp = re.sub(' +',',',i.replace('(','').replace(')','').strip()).split(',')
                for itest in range(len(self.ReactionGaussianName)): # find the molecule index from its name
                    if self.Mol[itest].MolName == self.PESProdTemp[0]: ireac = itest           
                self.PESProdZPEtemp0 = UnitConvert.EnergyConvert(InE=self.Mol[ireac].EleEnergy,InUnit='Har',OutUnit='Har')+UnitConvert.EnergyConvert(InE=sum(self.Mol[ireac].Freq)*self.Mol[ireac].ScaleFactor/2,InUnit='K',OutUnit='Har') # ZPE
                for itest in range(len(self.ReactionGaussianName)): # find the molecule index from its name
                    if self.Mol[itest].MolName == self.PESProdTemp[1]: ireac = itest           
                self.PESProdZPEtemp1 = UnitConvert.EnergyConvert(InE=self.Mol[ireac].EleEnergy,InUnit='Har',OutUnit='Har')+UnitConvert.EnergyConvert(InE=sum(self.Mol[ireac].Freq)*self.Mol[ireac].ScaleFactor/2,InUnit='K',OutUnit='Har') # ZPE
                self.EProdString = self.EProdString + ' ' + str(self.PESProdZPEtemp0) + ' + ' + str(self.PESProdZPEtemp1)+','
                self.EProdComment= self.EProdComment + ' ' + re.sub(' +','+',i.replace('(','').replace(')','').strip()) + ','
            else :
                for itest in range(len(self.ReactionGaussianName)): # find the molecule index from its name
                    if self.Mol[itest].MolName == i: ireac = itest           
                self.PESProdZPEtemp = UnitConvert.EnergyConvert(InE=self.Mol[ireac].EleEnergy,InUnit='Har',OutUnit='Har')+UnitConvert.EnergyConvert(InE=sum(self.Mol[ireac].Freq)*self.Mol[ireac].ScaleFactor/2,InUnit='K',OutUnit='Har') # ZPE
                self.EProdString = self.EProdString + str(self.PESProdZPEtemp)+','
                self.EProdComment= self.EProdComment + ' ' + i  +','             
        self.EProdString = re.sub(',$','',self.EProdString) + "} " + re.sub(',$','',self.EProdComment) + " *);\n"
        self.PESInp.write(self.EProdString)        
                
        self.EIntMString = "EIntM = {"
        self.EIntMComment = "(*"
        for i in self.PESIntM.keys():        
            for itest in range(len(self.ReactionGaussianName)): # find the molecule index from its name
                if self.Mol[itest].MolName == i: ireac = itest           
            self.PESIntMZPEtemp = UnitConvert.EnergyConvert(InE=self.Mol[ireac].EleEnergy,InUnit='Har',OutUnit='Har')+UnitConvert.EnergyConvert(InE=sum(self.Mol[ireac].Freq)*self.Mol[ireac].ScaleFactor/2,InUnit='K',OutUnit='Har') # ZPE
            self.EIntMString = self.EIntMString + str(self.PESIntMZPEtemp)+','
            self.EIntMComment= self.EIntMComment + ' ' + i  +','             
        self.EIntMString = re.sub(',$','',self.EIntMString) + "} " + re.sub(',$','',self.EIntMComment) + " *);\n"
        self.PESInp.write(self.EIntMString)                       

        self.ETraSString = "ETraS = {"
        self.ETraSComment = "(*"
        for i in self.PESTraS.keys():        
            for itest in range(len(self.ReactionGaussianName)): # find the molecule index from its name
                if self.Mol[itest].MolName == i: ireac = itest           
            self.PESTraSZPEtemp = UnitConvert.EnergyConvert(InE=self.Mol[ireac].EleEnergy,InUnit='Har',OutUnit='Har')+UnitConvert.EnergyConvert(InE=sum(self.Mol[ireac].Freq)*self.Mol[ireac].ScaleFactor/2,InUnit='K',OutUnit='Har') # ZPE
            self.ETraSString = self.ETraSString + str(self.PESTraSZPEtemp)+','
            self.ETraSComment= self.ETraSComment + ' ' + i  +','             
        self.ETraSString = re.sub(',$','',self.ETraSString) + "} " + re.sub(',$','',self.ETraSComment) + " *);\n"
        self.PESInp.write(self.ETraSString)                       

        # linking Transition States
        self.PESInp.write('\n')
        for i in range(self.NumberofReactions):        
            for itest in range(len(self.PESTraS.keys())): # find the index of TS in the ith reax
                if self.PESTraS.keys()[itest] == self.TranStats[i]: indextras = itest
            for itest in range(len(self.PESReac.keys())): # find the index of R in the ith reax
                if self.PESReac.keys()[itest] == self.Reactants[i]: indexreac, labelreac = itest, "Reac"
            for itest in range(len(self.PESProd.keys())):
                if self.PESProd.keys()[itest] == self.Reactants[i]: indexreac, labelreac = itest, "Prod"
            for itest in range(len(self.PESIntM.keys())): 
                if self.PESIntM.keys()[itest] == self.Reactants[i]: indexreac, labelreac = itest, "IntM"
            for itest in range(len(self.PESReac.keys())): # find the index of P in the ith reax
                if self.PESReac.keys()[itest] == self.Products[i]: indexprod, labelprod = itest, "Reac"
            for itest in range(len(self.PESProd.keys())):
                if self.PESProd.keys()[itest] == self.Products[i]: indexprod, labelprod = itest, "Prod"
            for itest in range(len(self.PESIntM.keys())): 
                if self.PESIntM.keys()[itest] == self.Products[i]: indexprod, labelprod = itest, "IntM"
            self.PESInp.write("TraS[%d] = Append[TraS[%d], {%s[%d][[3]], %s[%d][[3]]}];\n" % ( indextras+1, indextras+1, labelreac, indexreac+1, labelprod, indexprod+1 ))        
        
        self.PESInp.close()


    def WriteMultiWell(self):
        'Generate MultiWell input files'

        # read Gaussian *.log/out as DataClass.MoleculeClass
        for i in self.ReactionGaussianName:
            if not re.search('\.log|\.out',i,re.I) : self.ReactionGaussianName.remove(i)
        self.Mol = [0 for i in range(len(self.ReactionGaussianName))]
        for i in range(len(self.ReactionGaussianName)):
            self.Mol[i] = DataClass.MoleculeClass(self.ReactionGaussianPath,re.sub('\.[Ll][Oo][Gg]|\.[Oo][Uu][Tt]','',self.ReactionGaussianName[i]))
            self.Mol[i].ReadGaussian(0)    
        
        self.MultiPath = os.path.normpath(self.iniFilePath + '/MultiWell/')
        if not os.path.exists(self.MultiPath): os.mkdir(self.MultiPath)

        for indexTemp in self.Temp:
            self.MultiInp = open(os.path.normpath(self.MultiPath+'/multiwell'+'T'+str(indexTemp).replace('.','_')+'.dat'),'w')
            self.MultiInp.write('%s\n' % self.iniFilePath)
            self.MultiInp.write('%d   %d   %d   %d   %d\n' % self.MultiWellDoubleArray[:] )
            self.MultiInp.write('ATM   KCAL   AMUA\n')
            self.MultiInp.write('%f   %f\n' % (indexTemp, indexTemp))
            self.MultiInp.write('%d\n' % len(self.Pres))
            for i in self.Pres: self.MultiInp.write(str(i)+'   ')
            self.MultiInp.write('\n')

            # using dictionary to take account prodcuts and wells
            self.ProductDictionary = {}
            self.WellDictionary = {}
            for i in self.Reactants:
                if re.search('\(',i):
                    self.ProductDictionary[i] = 1
                else :
                    self.WellDictionary[i] = 1
            for i in self.Products:
                if re.search('\(',i):
                    self.ProductDictionary[i] = 1
                else :
                    self.WellDictionary[i] = 1

            self.MultiInp.write('%d   %d\n' % ( len(self.WellDictionary.keys()), len(self.ProductDictionary.keys()) ))

            for i in range(len(self.WellDictionary.keys())):
                for itest in range(len(self.ReactionGaussianName)): # find the molecule index from its name
                    if self.Mol[itest].MolName == self.WellDictionary.keys()[i]: ireac = itest
                self.MultiMasstemp = self.Mol[ireac].Mass
                self.MultiZPEtemp = UnitConvert.EnergyConvert(InE=self.Mol[ireac].EleEnergy,InUnit='Har',OutUnit='kcalmol')+UnitConvert.EnergyConvert(InE=sum(self.Mol[ireac].Freq)*self.Mol[ireac].ScaleFactor/2,InUnit='K',OutUnit='kcalmol') # ZPE            
                self.MultiInp.write('%d   %s   %f   %f   %s   %d   1\n' % ( (i+1), self.WellDictionary.keys()[i], self.MultiZPEtemp, UnitConvert.RotConConvert(InRC=self.Mol[ireac].AdRot,InUnit='GHz',OutUnit='amuA2'), self.Mol[ireac].ExternalSymm, self.Mol[ireac].SpinMulti)  )
            for i in range(len(self.ProductDictionary.keys())):
                self.MultiProdTemp = re.sub(' +',',',self.ProductDictionary.keys()[i].replace('(','').replace(')','').strip()).split(',')
                for itest in range(len(self.ReactionGaussianName)): # find the molecule index from its name
                    if self.Mol[itest].MolName == self.MultiProdTemp[0]: ireac = itest            
                self.MultiZPEtemp0 = UnitConvert.EnergyConvert(InE=self.Mol[ireac].EleEnergy,InUnit='Har',OutUnit='kcalmol')+UnitConvert.EnergyConvert(InE=sum(self.Mol[ireac].Freq)*self.Mol[ireac].ScaleFactor/2,InUnit='K',OutUnit='kcalmol') # ZPE
                for itest in range(len(self.ReactionGaussianName)): # find the molecule index from its name
                    if self.Mol[itest].MolName == self.MultiProdTemp[1]: ireac = itest            
                self.MultiZPEtemp1 = UnitConvert.EnergyConvert(InE=self.Mol[ireac].EleEnergy,InUnit='Har',OutUnit='kcalmol')+UnitConvert.EnergyConvert(InE=sum(self.Mol[ireac].Freq)*self.Mol[ireac].ScaleFactor/2,InUnit='K',OutUnit='kcalmol') # ZPE            
                self.MultiInp.write('%d   %s   %f\n' % ( i+1+len(self.WellDictionary.keys()), self.MultiProdTemp[0]+'_'+self.MultiProdTemp[1], self.MultiZPEtemp0+self.MultiZPEtemp1 )  )

            #  Ar
            self.MultiInp.write('3.47   114   40   %f\n' % ( self.MultiMasstemp ))

            # collision model
            for itest in range(len(self.ReactionGaussianName)): # find the molecule index from its name
                if self.Mol[itest].MolName == self.WellDictionary.keys()[0]: ireac = itest
            for i in range(len(self.WellDictionary.keys())):
                self.MultiInp.write('%d   %f   %f   1   %f   0   0   0   0   0   0   0\nLJ\n' %( i+1, self.Mol[ireac].LJsigma, self.Mol[ireac].LJepsilon, self.Mol[ireac].DeltaEDown))

            # reactions
            self.MultiInp.write('%d\n' % self.NumberofReactions)

            for i in range(self.NumberofReactions):
                if re.search('\(',self.Reactants[i]) and re.search('\(',self.Products[i]): # bimolecular reaction
                    print ("Warning: Reaction %d is bimolecular reaction in nature" % (i+1))
                elif re.search('\(',self.Reactants[i]) or re.search('\(',self.Products[i]):
                    if re.search('\(',self.Products[i]):  # dissociation reaction 1 -> 2
                        for idex in range(len(self.WellDictionary.keys())):
                            if self.WellDictionary.keys()[idex] == self.Reactants[i]: ireac = idex
                        for idex in range(len(self.ProductDictionary.keys())):
                            if self.ProductDictionary.keys()[idex] == self.Products[i]: iprod = idex
                        self.MultiInp.write("%d   %d   %s" % ( ireac+1, iprod+1+len(self.WellDictionary.keys()), self.TranStats[i] ))
                        for idex in range(len(self.ReactionGaussianName)):
                            if self.TranStats[i] == self.Mol[idex].MolName: itras = idex
                        for idex in range(len(self.ReactionGaussianName)):
                            if self.Mol[idex].MolName == self.Reactants[i]: ireac = idex
                        self.MultiZPEtemp0 = UnitConvert.EnergyConvert(InE=self.Mol[itras].EleEnergy,InUnit='Har',OutUnit='kcalmol')+UnitConvert.EnergyConvert(InE=sum(self.Mol[itras].Freq)*self.Mol[itras].ScaleFactor/2,InUnit='K',OutUnit='kcalmol') # ZPE
                        self.MultiZPEtemp1 = UnitConvert.EnergyConvert(InE=self.Mol[ireac].EleEnergy,InUnit='Har',OutUnit='kcalmol')+UnitConvert.EnergyConvert(InE=sum(self.Mol[ireac].Freq)*self.Mol[ireac].ScaleFactor/2,InUnit='K',OutUnit='kcalmol') # ZPE
                        self.MultiEE = self.MultiZPEtemp0 - self.MultiZPEtemp1
                        self.MultiInp.write('   %f   %s   %d   1   1E16   %f' % ( UnitConvert.RotConConvert(InRC=self.Mol[itras].AdRot,InUnit='GHz',OutUnit='amuA2'), self.Mol[itras].ExternalSymm, self.Mol[itras].SpinMulti, self.MultiEE ))
                        if self.Reversible[i] == 'YES':
                            self.MultiInp.write('   REV   FAST   ')
                        else :
                            self.MultiInp.write('   NOREV   FAST   ')
                        if self.Tunneling[i] == 'YES':
                            self.MultiInp.write('TUN   NOCENT   SUM\nTUN   %f\n' % (-1*UnitConvert.EnergyConvert(InE=self.Mol[itras].ImagFreq*self.Mol[itras].ScaleFactor,InUnit='K',OutUnit='cm-1')) )
                        else:
                            self.MultiInp.write('NOTUN   CENT2   SUM\n')
                    else :   # recombination/chemical activated 2 -> 1. Using 1 as 'reactant' and 2 as 'prodcut' actually
                        for idex in range(len(self.WellDictionary.keys())):
                            if self.WellDictionary.keys()[idex] == self.Products[i]: ireac = idex
                        for idex in range(len(self.ProductDictionary.keys())):
                            if self.ProductDictionary.keys()[idex] == self.Reactants[i]: iprod = idex
                        self.MultiInp.write("%d   %d   %s" % ( ireac+1, iprod+1+len(self.WellDictionary.keys()), self.TranStats[i] ))
                        for idex in range(len(self.ReactionGaussianName)):
                            if self.TranStats[i] == self.Mol[idex].MolName: itras = idex
                        for idex in range(len(self.ReactionGaussianName)):
                            if self.Mol[idex].MolName == self.Products[i]: ireac = idex
                        self.MultiZPEtemp0 = UnitConvert.EnergyConvert(InE=self.Mol[itras].EleEnergy,InUnit='Har',OutUnit='kcalmol')+UnitConvert.EnergyConvert(InE=sum(self.Mol[itras].Freq)*self.Mol[itras].ScaleFactor/2,InUnit='K',OutUnit='kcalmol') # ZPE
                        self.MultiZPEtemp1 = UnitConvert.EnergyConvert(InE=self.Mol[ireac].EleEnergy,InUnit='Har',OutUnit='kcalmol')+UnitConvert.EnergyConvert(InE=sum(self.Mol[ireac].Freq)*self.Mol[ireac].ScaleFactor/2,InUnit='K',OutUnit='kcalmol') # ZPE
                        self.MultiEE = self.MultiZPEtemp0 - self.MultiZPEtemp1
                        self.MultiInp.write('   %f   %s   %d   1   1E16   %f' % ( UnitConvert.RotConConvert(InRC=self.Mol[itras].AdRot,InUnit='GHz',OutUnit='amuA2'), self.Mol[itras].ExternalSymm, self.Mol[itras].SpinMulti, self.MultiEE ))
                        if self.Reversible[i] == 'YES':
                            self.MultiInp.write('   REV   FAST   ')
                        else :
                            self.MultiInp.write('   NOREV   FAST   ')
                        if self.Tunneling[i] == 'YES':
                            self.MultiInp.write('TUN   NOCENT   SUM\nTUN   %f\n' % (-1*UnitConvert.EnergyConvert(InE=self.Mol[itras].ImagFreq*self.Mol[itras].ScaleFactor,InUnit='K',OutUnit='cm-1')) )
                        else:
                            self.MultiInp.write('NOTUN   CENT2   SUM\n')
                else : # unimolecular isomerization
                    for idex in range(len(self.WellDictionary.keys())):
                        if self.WellDictionary.keys()[idex] == self.Reactants[i]: ireac = idex
                    for idex in range(len(self.WellDictionary.keys())):
                        if self.WellDictionary.keys()[idex] == self.Products[i]: iprod = idex
                    self.MultiInp.write("%d   %d   %s" % ( ireac+1, iprod+1, self.TranStats[i] ))
                    for idex in range(len(self.ReactionGaussianName)):
                        if self.TranStats[i] == self.Mol[idex].MolName: itras = idex
                    for idex in range(len(self.ReactionGaussianName)):
                        if self.Mol[idex].MolName == self.Reactants[i]: ireac = idex
                    self.MultiZPEtemp0 = UnitConvert.EnergyConvert(InE=self.Mol[itras].EleEnergy,InUnit='Har',OutUnit='kcalmol')+UnitConvert.EnergyConvert(InE=sum(self.Mol[itras].Freq)*self.Mol[itras].ScaleFactor/2,InUnit='K',OutUnit='kcalmol') # ZPE
                    self.MultiZPEtemp1 = UnitConvert.EnergyConvert(InE=self.Mol[ireac].EleEnergy,InUnit='Har',OutUnit='kcalmol')+UnitConvert.EnergyConvert(InE=sum(self.Mol[ireac].Freq)*self.Mol[ireac].ScaleFactor/2,InUnit='K',OutUnit='kcalmol') # ZPE
                    self.MultiEE = self.MultiZPEtemp0 - self.MultiZPEtemp1
                    self.MultiInp.write('   %f   %s   %d   1   1E16   %f' % ( UnitConvert.RotConConvert(InRC=self.Mol[itras].AdRot,InUnit='GHz',OutUnit='amuA2'), self.Mol[itras].ExternalSymm, self.Mol[itras].SpinMulti, self.MultiEE ))
                    if self.Reversible[i] == 'YES':
                        self.MultiInp.write('   REV   FAST   ')
                    else :
                        self.MultiInp.write('   NOREV   FAST   ')
                    if self.Tunneling[i] == 'YES':
                        self.MultiInp.write('TUN   NOCENT   SUM\nTUN   %f\n' % (-1*UnitConvert.EnergyConvert(InE=self.Mol[itras].ImagFreq*self.Mol[itras].ScaleFactor,InUnit='K',OutUnit='cm-1')) )
                    else:
                        self.MultiInp.write('NOTUN   CENT2   SUM\n')

            # calculation specification
            self.MultiInp.write('1000000   TIME   1.0E-07   ')
            if re.search('\(', self.Reactants[0]) and (not re.search('\(',self.Products[0])):
                self.MultiInp.write('CHEMACT   ')
                for idex in range(len(self.WellDictionary.keys())):
                    if self.WellDictionary.keys()[idex] == self.Products[0]: ireac = idex
                for idex in range(len(self.ProductDictionary.keys())):
                    if self.ProductDictionary.keys()[idex] == self.Reactants[0]: iprod = idex
                self.MultiInp.write('%d   %d   0\n' % ( ireac+1, iprod+1+len(self.WellDictionary.keys()) ) )
            elif not re.search('\(', self.Reactants[0]):
                for idex in range(len(self.WellDictionary.keys())):
                    if self.WellDictionary.keys()[idex] == self.Reactants[0] : ireac = idex
                self.MultiInp.write('THERMAL   %d   0   0' % (ireac+1))
                
            #   close file            
            self.MultiInp.close()
        

        

    def WriteDensum(self):
        'Generate Densum input files'

        self.MultiPath = os.path.normpath(self.iniFilePath + '/MultiWell/')
        if not os.path.exists(self.MultiPath): os.mkdir(self.MultiPath)
        self.DensumPath = os.path.normpath(self.MultiPath+'/DensData/')
        if not os.path.exists(self.DensumPath): os.mkdir(self.DensumPath)
        
        # read Gaussian *.log/out as DataClass.MoleculeClass
        for i in self.ReactionGaussianName:
            if not re.search('\.log|\.out',i,re.I) : self.ReactionGaussianName.remove(i)
        self.Mol = [0 for i in range(len(self.ReactionGaussianName))]
        for i in range(len(self.ReactionGaussianName)):
            self.DensumMol = DataClass.MoleculeClass(self.ReactionGaussianPath,re.sub('\.[Ll][Oo][Gg]|\.[Oo][Uu][Tt]','',self.ReactionGaussianName[i]))
            self.DensumMol.ReadGaussian(0)
            self.DensumInp = open(os.path.normpath(self.DensumPath+'/'+self.DensumMol.MolName+'.vibs'),'w')
            self.DensumInp.write("%s,  Created by Sparrow\n" % self.DensumMol.MolName)
            self.DensumInp.write('%s\n' % self.DensumMol.MolName)
            self.DensDof = len(self.DensumMol.Freq)+(len(self.DensumMol.RotCon)-1)/2
            self.DensumInp.write('%d   0   HAR   AMUA\n' % self.DensDof)
            self.DensumInp.write('%d   %d   %d   %d\n' % self.MultiWellDoubleArray[:4] )
            for ivib in range(len(self.DensumMol.Freq)): # vibs
                self.DensumInp.write("%d    vib    %f    0    1\n"%( (ivib+1), UnitConvert.EnergyConvert(InE=self.DensumMol.Freq[ivib]*self.DensumMol.ScaleFactor,InUnit='K',OutUnit='cm-1') ))
            if len(self.DensumMol.RotCon) != 1:
                self.DensumInp.write("%d    rot    %f    1    1\n"%( (len(self.DensumMol.Freq)+1), UnitConvert.RotConConvert(InRC=self.DensumMol.KRot,InUnit='GHz',OutUnit='amuA2')  ))
            self.DensumInp.close()

        self.DensBatch = open(os.path.normpath(self.DensumPath+'/densum.batch'),'w')
        self.DensBatch.write('%d,   %d,   %d,   %d\n' % self.MultiWellDoubleArray[:4] )
        for i in self.ReactionGaussianName: self.DensBatch.write(re.sub('\.[Ll][Oo][Gg]|\.[Oo][Uu][Tt]','',i).strip()+'.vibs\n')
        self.DensBatch.close()      
        

    def WriteThermo(self):
        'Generate Thermo input files'
        
        # read Gaussian *.log/out as DataClass.MoleculeClass
        for i in self.ReactionGaussianName:
            if not re.search('\.log|\.out',i,re.I) : self.ReactionGaussianName.remove(i)
        self.Mol = [0 for i in range(len(self.ReactionGaussianName))]
        for i in range(len(self.ReactionGaussianName)):
            self.Mol[i] = DataClass.MoleculeClass(self.ReactionGaussianPath,re.sub('\.[Ll][Oo][Gg]|\.[Oo][Uu][Tt]','',self.ReactionGaussianName[i]))
            self.Mol[i].ReadGaussian(0)
        
        self.ThermoPath = os.path.normpath(self.iniFilePath+'/Thermo/')
        if not os.path.exists(self.ThermoPath): os.mkdir(self.ThermoPath)
        
        # Keq (self.NumberofReactions)*2 files: Kp and Kc
        for i in range(self.NumberofReactions*2):
            
            self.KeqPath = os.path.normpath(self.ThermoPath+'/Keq/') # file and path
            if not os.path.exists(self.KeqPath): os.mkdir(self.KeqPath)
            
            if i < self.NumberofReactions :     # 1st line: units
                self.KeqInp = open(os.path.normpath(self.KeqPath+'/Reax'+str(i%self.NumberofReactions+1)+'Kp.dat'),'w')
                self.KeqInp.write('KCAL  ATM\n')
            else :
                self.KeqInp = open(os.path.normpath(self.KeqPath+'/Reax'+str(i%self.NumberofReactions+1)+'Kc.dat'),'w')
                self.KeqInp.write('KCAL  MCC\n')
                
            self.KeqInp.writelines('11\n')  # 11 temperatures
            self.KeqInp.writelines('1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000\n')
            
            self.ThermoSpecies = 2 # number of species
            if re.search('\(',self.Reactants[i%self.NumberofReactions]):
                self.ThermoSpecies = self.ThermoSpecies + 1
            if re.search('\(',self.Products[i%self.NumberofReactions]):
                self.ThermoSpecies = self.ThermoSpecies + 1
            self.KeqInp.write('%d\n' % self.ThermoSpecies)
            self.KeqInp.write('\n')

            if re.search('\(',self.Reactants[i%self.NumberofReactions]): # reactant
                self.ThermoReacTemp = re.sub(' +',',',self.Reactants[i%self.NumberofReactions].replace('(','').replace(')','').strip()).split(',')
                # 1st reactant
                for itest in range(len(self.ReactionGaussianName)): # find the molecule index from its name
                    if self.Mol[itest].MolName == self.ThermoReacTemp[0]: ireac = itest
                self.ThermoZPEtemp = UnitConvert.EnergyConvert(InE=self.Mol[ireac].EleEnergy,InUnit='Har',OutUnit='kcalmol')+UnitConvert.EnergyConvert(InE=sum(self.Mol[ireac].Freq)*self.Mol[ireac].ScaleFactor/2,InUnit='K',OutUnit='kcalmol') # ZPE
                self.KeqInp.write('reac  %s  %f\n' %(self.Mol[ireac].MolName,self.ThermoZPEtemp)) # ZPE
                self.KeqInp.write(self.Mol[ireac].MolFormula+'\n') # formula
                self.KeqInp.write("a) %s \nb) zero point corrected \nc) RRHO \n"%self.Mol[ireac].MethodBase) # comments
                self.KeqInp.write("%s  1  1\n"%(self.Mol[ireac].ExternalSymm)) # symmertrynumber opticalnumber electronicenergylevels
                self.KeqInp.write("0.0     %d\n"%self.Mol[ireac].SpinMulti) # electronic energy level , spin multiplicity
                self.KeqInp.write("%d   HAR   AMUA\n"% (len(self.Mol[ireac].Freq) + (len(self.Mol[ireac].RotCon)+1)/2)) # number of dof
                for ivib in range(len(self.Mol[ireac].Freq)): # vibs
                    self.KeqInp.write("%d    vib    %f    0    1\n"%( (ivib+1), UnitConvert.EnergyConvert(InE=self.Mol[ireac].Freq[ivib]*self.Mol[ireac].ScaleFactor,InUnit='K',OutUnit='cm-1') ))
                self.KeqInp.write("%d    rot    %f    1    2\n"%( (len(self.Mol[ireac].Freq)+1), UnitConvert.RotConConvert(InRC=self.Mol[ireac].AdRot,InUnit='GHz',OutUnit='amuA2')  )) # external rot
                if len(self.Mol[ireac].RotCon) != 1:
                    self.KeqInp.write("%d    rot    %f    1    1\n"%( (len(self.Mol[ireac].Freq)+2), UnitConvert.RotConConvert(InRC=self.Mol[ireac].KRot,InUnit='GHz',OutUnit='amuA2')  ))
                self.KeqInp.write('\n')
                # 2nd reactant
                for itest in range(len(self.ReactionGaussianName)): # find the molecule index from its name
                    if self.Mol[itest].MolName == self.ThermoReacTemp[1]: ireac = itest
                self.ThermoZPEtemp = UnitConvert.EnergyConvert(InE=self.Mol[ireac].EleEnergy,InUnit='Har',OutUnit='kcalmol')+UnitConvert.EnergyConvert(InE=sum(self.Mol[ireac].Freq)*self.Mol[ireac].ScaleFactor/2,InUnit='K',OutUnit='kcalmol') # ZPE
                self.KeqInp.write('reac  %s  %f\n' %(self.Mol[ireac].MolName,self.ThermoZPEtemp)) # ZPE
                self.KeqInp.write(self.Mol[ireac].MolFormula+'\n') # formula
                self.KeqInp.write("a) %s \nb) zero point corrected \nc) RRHO \n"%self.Mol[ireac].MethodBase) # comments
                self.KeqInp.write("%s  1  1\n"%(self.Mol[ireac].ExternalSymm)) # symmertrynumber opticalnumber electronicenergylevels
                self.KeqInp.write("0.0     %d\n"%self.Mol[ireac].SpinMulti) # electronic energy level , spin multiplicity
                self.KeqInp.write("%d   HAR   AMUA\n"% (len(self.Mol[ireac].Freq) + (len(self.Mol[ireac].RotCon)+1)/2)) # number of dof
                for ivib in range(len(self.Mol[ireac].Freq)): # vibs
                    self.KeqInp.write("%d    vib    %f    0    1\n"%( (ivib+1), UnitConvert.EnergyConvert(InE=self.Mol[ireac].Freq[ivib]*self.Mol[ireac].ScaleFactor,InUnit='K',OutUnit='cm-1') ))
                self.KeqInp.write("%d    rot    %f    1    2\n"%( (len(self.Mol[ireac].Freq)+1), UnitConvert.RotConConvert(InRC=self.Mol[ireac].AdRot,InUnit='GHz',OutUnit='amuA2')  )) # external rot
                if len(self.Mol[ireac].RotCon) != 1:
                    self.KeqInp.write("%d    rot    %f    1    1\n"%( (len(self.Mol[ireac].Freq)+2), UnitConvert.RotConConvert(InRC=self.Mol[ireac].KRot,InUnit='GHz',OutUnit='amuA2')  ))
                self.KeqInp.write('\n')
            else :
                for itest in range(len(self.ReactionGaussianName)): # find the molecule index from its name
                    if self.Mol[itest].MolName == self.Reactants[i%self.NumberofReactions]: ireac = itest
                self.ThermoZPEtemp = UnitConvert.EnergyConvert(InE=self.Mol[ireac].EleEnergy,InUnit='Har',OutUnit='kcalmol')+UnitConvert.EnergyConvert(InE=sum(self.Mol[ireac].Freq)*self.Mol[ireac].ScaleFactor/2,InUnit='K',OutUnit='kcalmol') # ZPE
                self.KeqInp.write('reac  %s  %f\n' %(self.Mol[ireac].MolName,self.ThermoZPEtemp)) # ZPE
                self.KeqInp.write(self.Mol[ireac].MolFormula+'\n') # formula
                self.KeqInp.write("a) %s \nb) zero point corrected \nc) RRHO \n"%self.Mol[ireac].MethodBase) # comments
                self.KeqInp.write("%s  1  1\n"%(self.Mol[ireac].ExternalSymm)) # symmertrynumber opticalnumber electronicenergylevels
                self.KeqInp.write("0.0     %d\n"%self.Mol[ireac].SpinMulti) # electronic energy level , spin multiplicity
                self.KeqInp.write("%d   HAR   AMUA\n"% (len(self.Mol[ireac].Freq) + (len(self.Mol[ireac].RotCon)+1)/2)) # number of dof
                for ivib in range(len(self.Mol[ireac].Freq)): # vibs
                    self.KeqInp.write("%d    vib    %f    0    1\n"%( (ivib+1), UnitConvert.EnergyConvert(InE=self.Mol[ireac].Freq[ivib]*self.Mol[ireac].ScaleFactor,InUnit='K',OutUnit='cm-1') ))
                self.KeqInp.write("%d    rot    %f    1    2\n"%( (len(self.Mol[ireac].Freq)+1), UnitConvert.RotConConvert(InRC=self.Mol[ireac].AdRot,InUnit='GHz',OutUnit='amuA2')  )) # external rot
                if len(self.Mol[ireac].RotCon) != 1:
                    self.KeqInp.write("%d    rot    %f    1    1\n"%( (len(self.Mol[ireac].Freq)+2), UnitConvert.RotConConvert(InRC=self.Mol[ireac].KRot,InUnit='GHz',OutUnit='amuA2')  ))
                self.KeqInp.write('\n')


            if re.search('\(',self.Products[i%self.NumberofReactions]): # products 
                self.ThermoProdTemp = re.sub(' +',',',self.Products[i%self.NumberofReactions].replace('(','').replace(')','').strip()).split(',')
                # 1st product
                for itest in range(len(self.ReactionGaussianName)): # find the molecule index from its name
                    if self.Mol[itest].MolName == self.ThermoProdTemp[0]: ireac = itest
                self.ThermoZPEtemp = UnitConvert.EnergyConvert(InE=self.Mol[ireac].EleEnergy,InUnit='Har',OutUnit='kcalmol')+UnitConvert.EnergyConvert(InE=sum(self.Mol[ireac].Freq)*self.Mol[ireac].ScaleFactor/2,InUnit='K',OutUnit='kcalmol') # ZPE
                self.KeqInp.write('prod  %s  %f\n' %(self.Mol[ireac].MolName,self.ThermoZPEtemp)) # ZPE
                self.KeqInp.write(self.Mol[ireac].MolFormula+'\n') # formula
                self.KeqInp.write("a) %s \nb) zero point corrected \nc) RRHO \n"%self.Mol[ireac].MethodBase) # comments
                self.KeqInp.write("%s  1  1\n"%(self.Mol[ireac].ExternalSymm)) # symmertrynumber opticalnumber electronicenergylevels
                self.KeqInp.write("0.0     %d\n"%self.Mol[ireac].SpinMulti) # electronic energy level , spin multiplicity
                self.KeqInp.write("%d   HAR   AMUA\n"% (len(self.Mol[ireac].Freq) + (len(self.Mol[ireac].RotCon)+1)/2)) # number of dof
                for ivib in range(len(self.Mol[ireac].Freq)): # vibs
                    self.KeqInp.write("%d    vib    %f    0    1\n"%( (ivib+1), UnitConvert.EnergyConvert(InE=self.Mol[ireac].Freq[ivib]*self.Mol[ireac].ScaleFactor,InUnit='K',OutUnit='cm-1') ))
                self.KeqInp.write("%d    rot    %f    1    2\n"%( (len(self.Mol[ireac].Freq)+1), UnitConvert.RotConConvert(InRC=self.Mol[ireac].AdRot,InUnit='GHz',OutUnit='amuA2')  )) # external rot
                if len(self.Mol[ireac].RotCon) != 1:
                    self.KeqInp.write("%d    rot    %f    1    1\n"%( (len(self.Mol[ireac].Freq)+2), UnitConvert.RotConConvert(InRC=self.Mol[ireac].KRot,InUnit='GHz',OutUnit='amuA2')  ))
                self.KeqInp.write('\n')
                # 2nd product
                for itest in range(len(self.ReactionGaussianName)): # find the molecule index from its name
                    if self.Mol[itest].MolName == self.ThermoProdTemp[1]: ireac = itest
                self.ThermoZPEtemp = UnitConvert.EnergyConvert(InE=self.Mol[ireac].EleEnergy,InUnit='Har',OutUnit='kcalmol')+UnitConvert.EnergyConvert(InE=sum(self.Mol[ireac].Freq)*self.Mol[ireac].ScaleFactor/2,InUnit='K',OutUnit='kcalmol') # ZPE
                self.KeqInp.write('prod  %s  %f\n' %(self.Mol[ireac].MolName,self.ThermoZPEtemp)) # ZPE
                self.KeqInp.write(self.Mol[ireac].MolFormula+'\n') # formula
                self.KeqInp.write("a) %s \nb) zero point corrected \nc) RRHO \n"%self.Mol[ireac].MethodBase) # comments
                self.KeqInp.write("%s  1  1\n"%(self.Mol[ireac].ExternalSymm)) # symmertrynumber opticalnumber electronicenergylevels
                self.KeqInp.write("0.0     %d\n"%self.Mol[ireac].SpinMulti) # electronic energy level , spin multiplicity
                self.KeqInp.write("%d   HAR   AMUA\n"% (len(self.Mol[ireac].Freq) + (len(self.Mol[ireac].RotCon)+1)/2)) # number of dof
                for ivib in range(len(self.Mol[ireac].Freq)): # vibs
                    self.KeqInp.write("%d    vib    %f    0    1\n"%( (ivib+1), UnitConvert.EnergyConvert(InE=self.Mol[ireac].Freq[ivib]*self.Mol[ireac].ScaleFactor,InUnit='K',OutUnit='cm-1') ))
                self.KeqInp.write("%d    rot    %f    1    2\n"%( (len(self.Mol[ireac].Freq)+1), UnitConvert.RotConConvert(InRC=self.Mol[ireac].AdRot,InUnit='GHz',OutUnit='amuA2')  )) # external rot
                if len(self.Mol[ireac].RotCon) != 1:
                    self.KeqInp.write("%d    rot    %f    1    1\n"%( (len(self.Mol[ireac].Freq)+2), UnitConvert.RotConConvert(InRC=self.Mol[ireac].KRot,InUnit='GHz',OutUnit='amuA2')  ))
                self.KeqInp.write('\n')
            else :
                for itest in range(len(self.ReactionGaussianName)): # find the molecule index from its name
                    if self.Mol[itest].MolName == self.Products[i%self.NumberofReactions]: ireac = itest
                self.ThermoZPEtemp = UnitConvert.EnergyConvert(InE=self.Mol[ireac].EleEnergy,InUnit='Har',OutUnit='kcalmol')+UnitConvert.EnergyConvert(InE=sum(self.Mol[ireac].Freq)*self.Mol[ireac].ScaleFactor/2,InUnit='K',OutUnit='kcalmol') # ZPE
                self.KeqInp.write('prod  %s  %f\n' %(self.Mol[ireac].MolName,self.ThermoZPEtemp)) # ZPE
                self.KeqInp.write(self.Mol[ireac].MolFormula+'\n') # formula
                self.KeqInp.write("a) %s \nb) zero point corrected \nc) RRHO \n"%self.Mol[ireac].MethodBase) # comments
                self.KeqInp.write("%s  1  1\n"%(self.Mol[ireac].ExternalSymm)) # symmertrynumber opticalnumber electronicenergylevels
                self.KeqInp.write("0.0     %d\n"%self.Mol[ireac].SpinMulti) # electronic energy level , spin multiplicity
                self.KeqInp.write("%d   HAR   AMUA\n"% (len(self.Mol[ireac].Freq) + (len(self.Mol[ireac].RotCon)+1)/2)) # number of dof
                for ivib in range(len(self.Mol[ireac].Freq)): # vibs
                    self.KeqInp.write("%d    vib    %f    0    1\n"%( (ivib+1), UnitConvert.EnergyConvert(InE=self.Mol[ireac].Freq[ivib]*self.Mol[ireac].ScaleFactor,InUnit='K',OutUnit='cm-1') ))
                self.KeqInp.write("%d    rot    %f    1    2\n"%( (len(self.Mol[ireac].Freq)+1), UnitConvert.RotConConvert(InRC=self.Mol[ireac].AdRot,InUnit='GHz',OutUnit='amuA2')  )) # external rot
                if len(self.Mol[ireac].RotCon) != 1:
                    self.KeqInp.write("%d    rot    %f    1    1\n"%( (len(self.Mol[ireac].Freq)+2), UnitConvert.RotConConvert(InRC=self.Mol[ireac].KRot,InUnit='GHz',OutUnit='amuA2')  ))
                self.KeqInp.write('\n')

            self.KeqInp.close() # close file

        # CTST (self.NumberofReactions)*2 files: kf and kb
        for i in range(self.NumberofReactions*2):

            self.ctstPath = os.path.normpath(self.ThermoPath+'/ctst')
            if not os.path.exists(self.ctstPath): os.mkdir(self.ctstPath)

            if i < self.NumberofReactions :
                self.ctstInp = open(os.path.normpath(self.ctstPath+'/Reax'+str(i%self.NumberofReactions+1)+'kf.dat'),'w')
            else:
                self.ctstInp = open(os.path.normpath(self.ctstPath+'/Reax'+str(i%self.NumberofReactions+1)+'kb.dat'),'w')

            self.ctstInp.write('KCAL  MCC\n')
            self.ctstInp.write('11\n')
            self.ctstInp.write('1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000\n')

            self.ThermoSpecies = 2
            if i < self.NumberofReactions:
                if re.search('\(',self.Reactants[i%self.NumberofReactions]): self.ThermoSpecies = 3
            else :
                if re.search('\(',self.Products[i%self.NumberofReactions]): self.ThermoSpecies = 3
            self.ctstInp.write('%d\n' % self.ThermoSpecies)
            self.ctstInp.write('\n')

            if i < self.NumberofReactions:
                self.ctstReacTemp = self.Reactants[i%self.NumberofReactions]
            else:
                self.ctstReacTemp = self.Products[i%self.NumberofReactions]

            if re.search('\(',self.ctstReacTemp): # reactant
                self.ctstReacTemp1 = re.sub(' +',',',self.ctstReacTemp.replace('(','').replace(')','').strip()).split(',')
                # 1st reactant
                for itest in range(len(self.ReactionGaussianName)): # find the molecule index from its name
                    if self.Mol[itest].MolName == self.ctstReacTemp1[0]: ireac = itest
                self.ThermoZPEtemp = UnitConvert.EnergyConvert(InE=self.Mol[ireac].EleEnergy,InUnit='Har',OutUnit='kcalmol')+UnitConvert.EnergyConvert(InE=sum(self.Mol[ireac].Freq)*self.Mol[ireac].ScaleFactor/2,InUnit='K',OutUnit='kcalmol') # ZPE
                self.ctstInp.write('reac  %s  %f\n' %(self.Mol[ireac].MolName,self.ThermoZPEtemp)) # ZPE
                self.ctstInp.write(self.Mol[ireac].MolFormula+'\n') # formula
                self.ctstInp.write("a) %s \nb) zero point corrected \nc) RRHO \n"%self.Mol[ireac].MethodBase) # comments
                self.ctstInp.write("%s  1  1\n"%(self.Mol[ireac].ExternalSymm)) # symmertrynumber opticalnumber electronicenergylevels
                self.ctstInp.write("0.0     %d\n"%self.Mol[ireac].SpinMulti) # electronic energy level , spin multiplicity
                self.ctstInp.write("%d   HAR   AMUA\n"% (len(self.Mol[ireac].Freq) + (len(self.Mol[ireac].RotCon)+1)/2)) # number of dof
                for ivib in range(len(self.Mol[ireac].Freq)): # vibs
                    self.ctstInp.write("%d    vib    %f    0    1\n"%( (ivib+1), UnitConvert.EnergyConvert(InE=self.Mol[ireac].Freq[ivib]*self.Mol[ireac].ScaleFactor,InUnit='K',OutUnit='cm-1') ))
                self.ctstInp.write("%d    rot    %f    1    2\n"%( (len(self.Mol[ireac].Freq)+1), UnitConvert.RotConConvert(InRC=self.Mol[ireac].AdRot,InUnit='GHz',OutUnit='amuA2')  )) # external rot
                if len(self.Mol[ireac].RotCon) != 1:
                    self.ctstInp.write("%d    rot    %f    1    1\n"%( (len(self.Mol[ireac].Freq)+2), UnitConvert.RotConConvert(InRC=self.Mol[ireac].KRot,InUnit='GHz',OutUnit='amuA2')  ))
                self.ctstInp.write('\n')
                # 2nd reactant
                for itest in range(len(self.ReactionGaussianName)): # find the molecule index from its name
                    if self.Mol[itest].MolName == self.ctstReacTemp1[1]: ireac = itest
                self.ThermoZPEtemp = UnitConvert.EnergyConvert(InE=self.Mol[ireac].EleEnergy,InUnit='Har',OutUnit='kcalmol')+UnitConvert.EnergyConvert(InE=sum(self.Mol[ireac].Freq)*self.Mol[ireac].ScaleFactor/2,InUnit='K',OutUnit='kcalmol') # ZPE
                self.ctstInp.write('reac  %s  %f\n' %(self.Mol[ireac].MolName,self.ThermoZPEtemp)) # ZPE
                self.ctstInp.write(self.Mol[ireac].MolFormula+'\n') # formula
                self.ctstInp.write("a) %s \nb) zero point corrected \nc) RRHO \n"%self.Mol[ireac].MethodBase) # comments
                self.ctstInp.write("%s  1  1\n"%(self.Mol[ireac].ExternalSymm)) # symmertrynumber opticalnumber electronicenergylevels
                self.ctstInp.write("0.0     %d\n"%self.Mol[ireac].SpinMulti) # electronic energy level , spin multiplicity
                self.ctstInp.write("%d   HAR   AMUA\n"% (len(self.Mol[ireac].Freq) + (len(self.Mol[ireac].RotCon)+1)/2)) # number of dof
                for ivib in range(len(self.Mol[ireac].Freq)): # vibs
                    self.ctstInp.write("%d    vib    %f    0    1\n"%( (ivib+1), UnitConvert.EnergyConvert(InE=self.Mol[ireac].Freq[ivib]*self.Mol[ireac].ScaleFactor,InUnit='K',OutUnit='cm-1') ))
                self.ctstInp.write("%d    rot    %f    1    2\n"%( (len(self.Mol[ireac].Freq)+1), UnitConvert.RotConConvert(InRC=self.Mol[ireac].AdRot,InUnit='GHz',OutUnit='amuA2')  )) # external rot
                if len(self.Mol[ireac].RotCon) != 1:
                    self.ctstInp.write("%d    rot    %f    1    1\n"%( (len(self.Mol[ireac].Freq)+2), UnitConvert.RotConConvert(InRC=self.Mol[ireac].KRot,InUnit='GHz',OutUnit='amuA2')  ))
                self.ctstInp.write('\n')
            else :
                for itest in range(len(self.ReactionGaussianName)): # find the molecule index from its name
                    if self.Mol[itest].MolName == self.ctstReacTemp: ireac = itest
                self.ThermoZPEtemp = UnitConvert.EnergyConvert(InE=self.Mol[ireac].EleEnergy,InUnit='Har',OutUnit='kcalmol')+UnitConvert.EnergyConvert(InE=sum(self.Mol[ireac].Freq)*self.Mol[ireac].ScaleFactor/2,InUnit='K',OutUnit='kcalmol') # ZPE
                self.ctstInp.write('reac  %s  %f\n' %(self.Mol[ireac].MolName,self.ThermoZPEtemp)) # ZPE
                self.ctstInp.write(self.Mol[ireac].MolFormula+'\n') # formula
                self.ctstInp.write("a) %s \nb) zero point corrected \nc) RRHO \n"%self.Mol[ireac].MethodBase) # comments
                self.ctstInp.write("%s  1  1\n"%(self.Mol[ireac].ExternalSymm)) # symmertrynumber opticalnumber electronicenergylevels
                self.ctstInp.write("0.0     %d\n"%self.Mol[ireac].SpinMulti) # electronic energy level , spin multiplicity
                self.ctstInp.write("%d   HAR   AMUA\n"% (len(self.Mol[ireac].Freq) + (len(self.Mol[ireac].RotCon)+1)/2)) # number of dof
                for ivib in range(len(self.Mol[ireac].Freq)): # vibs
                    self.ctstInp.write("%d    vib    %f    0    1\n"%( (ivib+1), UnitConvert.EnergyConvert(InE=self.Mol[ireac].Freq[ivib]*self.Mol[ireac].ScaleFactor,InUnit='K',OutUnit='cm-1') ))
                self.ctstInp.write("%d    rot    %f    1    2\n"%( (len(self.Mol[ireac].Freq)+1), UnitConvert.RotConConvert(InRC=self.Mol[ireac].AdRot,InUnit='GHz',OutUnit='amuA2')  )) # external rot
                if len(self.Mol[ireac].RotCon) != 1:
                    self.ctstInp.write("%d    rot    %f    1    1\n"%( (len(self.Mol[ireac].Freq)+2), UnitConvert.RotConConvert(InRC=self.Mol[ireac].KRot,InUnit='GHz',OutUnit='amuA2')  ))
                self.ctstInp.write('\n')


            for itest in range(len(self.ReactionGaussianName)):
                if self.Mol[itest].MolName == self.TranStats[i%self.NumberofReactions]: ireac = itest
            self.ThermoZPEtemp = UnitConvert.EnergyConvert(InE=self.Mol[ireac].EleEnergy,InUnit='Har',OutUnit='kcalmol')+UnitConvert.EnergyConvert(InE=sum(self.Mol[ireac].Freq)*self.Mol[ireac].ScaleFactor/2,InUnit='K',OutUnit='kcalmol') # ZPE
            if i < self.NumberofReactions :
                self.ctstprod = self.Products[i%self.NumberofReactions]
            else :
                self.ctstprod = self.Reactants[i%self.NumberofReactions]
            if re.search('\(',self.ctstprod):
                self.ctstprodTemp = re.sub(' +',',',self.ctstprod.replace('(','').replace(')','').strip()).split(',')
                for jtest in range(len(self.ReactionGaussianName)):
                    if self.Mol[jtest].MolName == self.ctstprodTemp[0]: iprod = jtest
                self.ctstZPEprod0 = UnitConvert.EnergyConvert(InE=self.Mol[iprod].EleEnergy,InUnit='Har',OutUnit='kcalmol')+UnitConvert.EnergyConvert(InE=sum(self.Mol[iprod].Freq)*self.Mol[ireac].ScaleFactor/2,InUnit='K',OutUnit='kcalmol')
                for jtest in range(len(self.ReactionGaussianName)):
                    if self.Mol[jtest].MolName == self.ctstprodTemp[1]: iprod = jtest
                self.ctstZPEprod1 = UnitConvert.EnergyConvert(InE=self.Mol[iprod].EleEnergy,InUnit='Har',OutUnit='kcalmol')+UnitConvert.EnergyConvert(InE=sum(self.Mol[iprod].Freq)*self.Mol[ireac].ScaleFactor/2,InUnit='K',OutUnit='kcalmol')        
                self.VVR = self.ThermoZPEtemp -self.ctstZPEprod0 - self.ctstZPEprod1
            else :
                for jtest in range(len(self.ReactionGaussianName)):
                    if self.Mol[jtest].MolName == self.ctstprod: iprod = jtest
                self.ctstZPEprod = UnitConvert.EnergyConvert(InE=self.Mol[iprod].EleEnergy,InUnit='Har',OutUnit='kcalmol')+UnitConvert.EnergyConvert(InE=sum(self.Mol[iprod].Freq)*self.Mol[ireac].ScaleFactor/2,InUnit='K',OutUnit='kcalmol')
                self.VVR = self.ThermoZPEtemp - self.ctstZPEprod
            self.ctstInp.write('ctst  %s  %f  %f  %f\n' % ( self.Mol[ireac].MolName, self.ThermoZPEtemp, -1*self.Mol[ireac].ImagFreq, self.VVR )) # ctst molname DelH vimag VVR
            self.ctstInp.write(self.Mol[ireac].MolFormula+'\n') # formula
            self.ctstInp.write("a) %s \nb) zero point corrected \nc) RRHO \n"%self.Mol[ireac].MethodBase) # comments
            self.ctstInp.write("%s  1  1\n"%(self.Mol[ireac].ExternalSymm)) # symmertrynumber opticalnumber electronicenergylevels
            self.ctstInp.write("0.0     %d\n"%self.Mol[ireac].SpinMulti) # electronic energy level , spin multiplicity
            self.ctstInp.write("%d   HAR   AMUA\n"% (len(self.Mol[ireac].Freq) + (len(self.Mol[ireac].RotCon)+1)/2)) # number of dof
            for ivib in range(len(self.Mol[ireac].Freq)): # vibs
                self.ctstInp.write("%d    vib    %f    0    1\n"%( (ivib+1), UnitConvert.EnergyConvert(InE=self.Mol[ireac].Freq[ivib]*self.Mol[ireac].ScaleFactor,InUnit='K',OutUnit='cm-1') ))
            self.ctstInp.write("%d    rot    %f    1    2\n"%( (len(self.Mol[ireac].Freq)+1), UnitConvert.RotConConvert(InRC=self.Mol[ireac].AdRot,InUnit='GHz',OutUnit='amuA2')  )) # external rot
            if len(self.Mol[ireac].RotCon) != 1:
                self.ctstInp.write("%d    rot    %f    1    1\n"%( (len(self.Mol[ireac].Freq)+2), UnitConvert.RotConConvert(InRC=self.Mol[ireac].KRot,InUnit='GHz',OutUnit='amuA2')  ))
            self.ctstInp.write('\n')

            self.ctstInp.close()
        


    def WriteMESMER(self):
        'Generate MESMER input files'

        # read Gaussian *.log/out as DataClass.MoleculeClass
        for i in self.ReactionGaussianName:
            if not re.search('\.log|\.out',i,re.I) : self.ReactionGaussianName.remove(i)
        self.Mol = [0 for i in range(len(self.ReactionGaussianName))]
        for i in range(len(self.ReactionGaussianName)):
            self.Mol[i] = DataClass.MoleculeClass(self.ReactionGaussianPath,re.sub('\.[Ll][Oo][Gg]|\.[Oo][Uu][Tt]','',self.ReactionGaussianName[i]))
            self.Mol[i].ReadGaussian(0)

        for iTemp in range(len(self.Temp)):
            for iPres in range(len(self.Pres)):
                
                # create document
                self.doc = minidom.Document()

                # root node -- me:mesmer
                self.MEmesmer = self.doc.createElement("me:mesmer") 
                self.MEmesmer.setAttribute("xmlns","http://www.xml-cml.org/schema") 
                self.MEmesmer.setAttribute("xmlns:me","http://www.chem.leeds.ac.uk/mesmer")
                self.MEmesmer.setAttribute("xmlns:xsi","http://www.w3.org/2001/XMLSchema-instance")
                self.MEmesmer.setAttribute("xmlns:cml","http://www.xml-cml.org/schema")
                self.doc.appendChild(self.MEmesmer)  
                
                # first level trees
                # me:title
                self.MEtitle = self.doc.createElement("me:title") 
                self.MEtitle.appendChild(self.doc.createTextNode(self.iniFilePath)) 
                self.MEmesmer.appendChild(self.MEtitle) 
                # moleculeList
                self.MEmolList = self.doc.createElement("moleculeList")
                self.MEmesmer.appendChild(self.MEmolList)
                # reactionList
                self.MEreaList = self.doc.createElement("reactionList")
                self.MEmesmer.appendChild(self.MEreaList)
                # me:conditions
                self.MEcondition = self.doc.createElement("me:conditions")
                self.MEmesmer.appendChild(self.MEcondition)
                # me:modelParameters
                self.MEmodelPar = self.doc.createElement("me:modelParameters")
                self.MEmesmer.appendChild(self.MEmodelPar)
                # me:control
                self.MEcontrol = self.doc.createElement("me:control")
                self.MEmesmer.appendChild(self.MEcontrol) 

                # moleculeList-branch: loops for molecule
                for i in range(len(self.ReactionGaussianName)) :
                    self.MEmol = self.doc.createElement("molecule")
                    self.MEmol.setAttribute("id",self.Mol[i].MolName)
                    self.MEmolList.appendChild(self.MEmol)
                    self.proList = self.doc.createElement("propertyList")
                    self.MEmol.appendChild(self.proList) 
                    self.ZPE = self.doc.createElement('property') # ZPE
                    self.proList.appendChild(self.ZPE)
                    self.ZPE.setAttribute('dictRef','me:ZPE')
                    self.ZPEvalue = self.doc.createElement('scalar')
                    self.ZPE.appendChild(self.ZPEvalue)
                    self.ZPEvalue.setAttribute('units','kcal/mol')
                    self.ZPEtemp = UnitConvert.EnergyConvert(InE=self.Mol[i].EleEnergy,InUnit='Har',OutUnit='kcalmol')+UnitConvert.EnergyConvert(InE=sum(self.Mol[i].Freq)*self.Mol[i].ScaleFactor/2,InUnit='K',OutUnit='kcalmol')
                    self.ZPEvalue.appendChild(self.doc.createTextNode(str(self.ZPEtemp)))
                    self.RotCon = self.doc.createElement('property') # rotational constants
                    self.proList.appendChild(self.RotCon)
                    self.RotCon.setAttribute('dictRef','me:rotConsts')
                    self.RotConvalue = self.doc.createElement('array')
                    self.RotCon.appendChild(self.RotConvalue)
                    self.RotConvalue.setAttribute('units','cm-1')
                    self.RotContemp = ['','','']
                    for j in range(len(self.Mol[i].RotCon)): 
                        if self.Mol[i].RotCon[j] != 0: self.RotContemp[j] = UnitConvert.EnergyConvert(InE=self.Mol[i].RotCon[j],InUnit='GHz',OutUnit='cm-1')
                    self.RotConvalue.appendChild(self.doc.createTextNode(str(self.RotContemp[0])+' '+str(self.RotContemp[1])+' '+str(self.RotContemp[2])))
                    self.Freq = self.doc.createElement('property') # harmonics vibration
                    self.proList.appendChild(self.Freq)
                    self.Freq.setAttribute('dictRef','me:vibFreqs')
                    self.Freqvalue = self.doc.createElement('array')
                    self.Freq.appendChild(self.Freqvalue)
                    self.Freqvalue.setAttribute('units','cm-1')
                    self.Freqtemp = ''
                    for j in self.Mol[i].Freq: 
                        self.Freqtemp = self.Freqtemp + str(UnitConvert.EnergyConvert(InE=j,InUnit='K',OutUnit='cm-1')) +' '  
                    self.Freqvalue.appendChild(self.doc.createTextNode(self.Freqtemp))
                    self.ScalFac = self.doc.createElement('property') # scale factor
                    self.proList.appendChild(self.ScalFac)
                    self.ScalFac.setAttribute('dictRef','me:frequenciesScaleFactor')
                    self.ScalFacvalue = self.doc.createElement('scalar')
                    self.ScalFac.appendChild(self.ScalFacvalue)            
                    self.ScalFacvalue.appendChild(self.doc.createTextNode(str(self.Mol[i].ScaleFactor)))
                    self.SymNum = self.doc.createElement('property') # symmetry number
                    self.proList.appendChild(self.SymNum)
                    self.SymNum.setAttribute('dictRef','me:symmetryNumber')
                    self.SymNumvalue = self.doc.createElement('scalar')
                    self.SymNum.appendChild(self.SymNumvalue)            
                    self.SymNumvalue.appendChild(self.doc.createTextNode(self.Mol[i].ExternalSymm))
                    self.Mass = self.doc.createElement('property') # molecular mass
                    self.proList.appendChild(self.Mass)
                    self.Mass.setAttribute('dictRef','me:MW')
                    self.Massvalue = self.doc.createElement('scalar')
                    self.Mass.appendChild(self.Massvalue)
                    self.Massvalue.setAttribute('units','amu')            
                    self.Massvalue.appendChild(self.doc.createTextNode(str(self.Mol[i].Mass)))
                    self.SpinMul = self.doc.createElement('property') # spin multiplicity
                    self.proList.appendChild(self.SpinMul)
                    self.SpinMul.setAttribute('dictRef','me:spinMultiplicity')
                    self.SpinMulvalue = self.doc.createElement('scalar')
                    self.SpinMul.appendChild(self.SpinMulvalue)            
                    self.SpinMulvalue.appendChild(self.doc.createTextNode(str(self.Mol[i].SpinMulti)))
                    if self.Mol[i].CalcType == 'Local Minima':
                        self.epsilon = self.doc.createElement('property') # LJ epsilon
                        self.proList.appendChild(self.epsilon)
                        self.epsilon.setAttribute('dictRef','me:epsilon')
                        self.epsilonvalue = self.doc.createElement('scalar')
                        self.epsilon.appendChild(self.epsilonvalue)            
                        self.epsilonvalue.appendChild(self.doc.createTextNode(str(self.Mol[i].LJepsilon)))
                        self.sigma = self.doc.createElement('property') # LJ sigma
                        self.proList.appendChild(self.sigma)
                        self.sigma.setAttribute('dictRef','me:sigma')
                        self.sigmavalue = self.doc.createElement('scalar')
                        self.sigma.appendChild(self.sigmavalue)            
                        self.sigmavalue.appendChild(self.doc.createTextNode(str(self.Mol[i].LJsigma)))
                    elif self.Mol[i].CalcType == 'Saddle Point':
                        self.imFreq = self.doc.createElement('property') # imaginary freq
                        self.proList.appendChild(self.imFreq)
                        self.imFreq.setAttribute('dictRef','me:imFreqs')
                        self.imFreqvalue = self.doc.createElement('scalar')
                        self.imFreq.appendChild(self.imFreqvalue)            
                        self.imFreqvalue.appendChild(self.doc.createTextNode(str(-1.0*self.Mol[i].ImagFreq)))              
                    if self.Mol[i].CalcType == 'Local Minima': # collision model
                        self.Edown = self.doc.createElement("me:energyTransferModel")
                        self.MEmol.appendChild(self.Edown)
                        self.Edown.setAttribute('xsi:type','me:ExponentialDown')
                        self.deltaEdown = self.doc.createElement("me:deltaEDown")
                        self.Edown.appendChild(self.deltaEdown)
                        self.deltaEdown.setAttribute('units','cm-1')
                        self.deltaEdown.appendChild(self.doc.createTextNode(str(self.Mol[i].DeltaEDown)))
                        self.EdownTExponent = self.doc.createElement('me:deltaEDownTExponent')
                        self.Edown.appendChild(self.EdownTExponent)
                        self.EdownTExponent.setAttribute('referenceTemperature','298.')
                        self.EdownTExponent.appendChild(self.doc.createTextNode(str(0.0)))
                    self.DoSMethod = self.doc.createElement("me:DOSCMethod") # density of state method
                    self.MEmol.appendChild(self.DoSMethod)
                    self.DoSMethod.setAttribute('name','ClassicalRotors')
                #   Ar
                self.MEmol = self.doc.createElement("molecule")
                self.MEmol.setAttribute("id",'Ar')
                self.MEmolList.appendChild(self.MEmol)
                self.proList = self.doc.createElement("propertyList")
                self.MEmol.appendChild(self.proList) 
                self.ArMass = self.doc.createElement('property') # molecular mass
                self.proList.appendChild(self.ArMass)
                self.ArMass.setAttribute('dictRef','me:MW')
                self.ArMassvalue = self.doc.createElement('scalar')
                self.ArMass.appendChild(self.ArMassvalue)
                self.ArMassvalue.setAttribute('units','amu')            
                self.ArMassvalue.appendChild(self.doc.createTextNode(str(40)))
                self.Arepsilon = self.doc.createElement('property') # LJ epsilon
                self.proList.appendChild(self.Arepsilon)
                self.Arepsilon.setAttribute('dictRef','me:epsilon')
                self.Arepsilonvalue = self.doc.createElement('scalar')
                self.Arepsilon.appendChild(self.Arepsilonvalue)            
                self.Arepsilonvalue.appendChild(self.doc.createTextNode(str(114)))
                self.Arsigma = self.doc.createElement('property') # LJ sigma
                self.proList.appendChild(self.Arsigma)
                self.Arsigma.setAttribute('dictRef','me:sigma')
                self.Arsigmavalue = self.doc.createElement('scalar')
                self.Arsigma.appendChild(self.Arsigmavalue)            
                self.Arsigmavalue.appendChild(self.doc.createTextNode(str(3.47)))

                # reactionList-branch: loops for reactions
                for i in range(self.NumberofReactions): 

                    self.MEreac = self.doc.createElement("reaction") 
                    self.MEreac.setAttribute("id",'R'+str(i+1))
                    if self.Reversible[i] == 'YES':
                        self.MEreac.setAttribute("reversible","true")
                    else:
                        self.MEreac.setAttribute("reversible","false")
                    self.MEreaList.appendChild(self.MEreac)
                    self.reactantList = self.doc.createElement("reactantList") # reactants
                    self.MEreac.appendChild(self.reactantList)
                    if re.search('\(',self.Reactants[i]):
                        self.ReactantTemp =  re.split(',',re.sub(' +',',',self.Reactants[i].replace('(','').replace(')','').strip()))
                        self.reactant1 = self.doc.createElement("reactant")
                        self.reactantList.appendChild(self.reactant1)
                        self.reactant1value = self.doc.createElement("molecule")
                        if self.ReactantTemp[0].strip() == self.Excess[i]:
                            self.reactant1value.setAttribute("me:type","excessReactant")
                        else :
                            self.reactant1value.setAttribute("me:type","deficientReactant")
                        self.reactant1value.setAttribute("ref",self.ReactantTemp[0].strip())
                        self.reactant1.appendChild(self.reactant1value)
                        self.reactant2 = self.doc.createElement("reactant")                    
                        self.reactantList.appendChild(self.reactant2)      
                        self.reactant2value = self.doc.createElement("molecule")
                        if self.ReactantTemp[1].strip() == self.Excess[i]:
                            self.reactant2value.setAttribute("me:type","excessReactant")
                        else :
                            self.reactant2value.setAttribute("me:type","deficientReactant")
                        self.reactant2value.setAttribute("ref",self.ReactantTemp[1].strip())
                        self.reactant2.appendChild(self.reactant2value)
                    else :
                        self.reactant1 = self.doc.createElement("reactant")
                        self.reactantList.appendChild(self.reactant1)
                        self.reactant1value = self.doc.createElement("molecule")
                        self.reactant1value.setAttribute("me:type","modelled")
                        self.reactant1value.setAttribute("ref",self.Reactants[i].strip())
                        self.reactant1.appendChild(self.reactant1value)                

                    self.productList = self.doc.createElement("productList") # products
                    self.MEreac.appendChild(self.productList)
                    if re.search('\(',self.Products[i]):
                        self.ProductTemp =  re.split(',',re.sub(' +',',',self.Products[i].replace('(','').replace(')','').strip()))
                        self.product1 = self.doc.createElement("product")
                        self.productList.appendChild(self.product1)
                        self.prodcut1value = self.doc.createElement("molecule")
                        self.product1value.setAttribute("me:type","sink")
                        self.product1value.setAttribute("ref",self.ProductTemp[0].strip())
                        self.product1.appendChild(self.product1value)
                        self.product2 = self.doc.createElement("product")                    
                        self.productList.appendChild(self.product2)      
                        self.product2value = self.doc.createElement("molecule")
                        self.product2value.setAttribute("me:type","sink")
                        self.product2value.setAttribute("ref",self.ProductTemp[1].strip())
                        self.product2.appendChild(self.product2value)
                    else :
                        self.product1 = self.doc.createElement("product")
                        self.productList.appendChild(self.product1)
                        self.product1value = self.doc.createElement("molecule")
                        if self.Reversible[i] == 'YES': 
                            self.product1value.setAttribute("me:type","modelled")
                        else:
                            self.product1value.setAttribute("me:type","sink")
                        self.product1value.setAttribute("ref",self.Products[i].strip())
                        self.product1.appendChild(self.product1value)

                    if self.Excess[i] != '': # excess reactant concentration
                        self.exRecon = self.doc.createElement("me:excessReactantConc")
                        self.MEreac.appendChild(self.exRecon)
                        self.exRecon.appendChild(self.doc.createTextNode(str(self.ExcessMoleFraction[i]*6.02E23*self.Pres[iPres]/self.Temp[iTemp]/82.0574587)))

                    self.MEMCRC = self.doc.createElement("me:MCRCMethod") # micro canonical rate constant method
                    self.MEreac.appendChild(self.MEMCRC)
                    self.MEMCRC.setAttribute("name","SimpleRRKM")

                    if self.Tunneling[i] == 'YES': # tunneling
                        self.tunnel = self.doc.createElement("me:tunneling")
                        self.MEreac.appendChild(self.tunnel)
                        self.tunnel.appendChild(self.doc.createTextNode('Eckart'))

                    self.transtat = self.doc.createElement("me:transitionState") # transition states
                    self.MEreac.appendChild(self.transtat)
                    self.transtatvalue = self.doc.createElement("molecule")
                    self.transtat.appendChild(self.transtatvalue)
                    self.transtatvalue.setAttribute("ref",self.TranStats[i].strip())
                    self.transtatvalue.setAttribute("me:type","transitionState")

                # me:conditions branch
                self.bathGas = self.doc.createElement("me:bathGas")
                self.bathGas.appendChild(self.doc.createTextNode('Ar'))
                self.MEcondition.appendChild(self.bathGas)
                self.PTs = self.doc.createElement("me:PTs")
                self.MEcondition.appendChild(self.PTs)
                self.PTsvalue = self.doc.createElement("me:PTpair")
                self.PTs.appendChild(self.PTsvalue)
                self.PTsvalue.setAttribute("me:units","atm")
                self.PTsvalue.setAttribute("me:P",str(self.Pres[iPres]))
                self.PTsvalue.setAttribute("me:T",str(self.Temp[iTemp]))
                self.PTsvalue.setAttribute("precision","dd")
                  
                # me:modelParameters branch
                self.grainsize = self.doc.createElement("me:grainSize")
                self.MEmodelPar.appendChild(self.grainsize)
                self.grainsize.setAttribute("units","cm-1")
                self.grainsize.appendChild(self.doc.createTextNode(str(self.MESMERGrainSize)))
                self.tophill = self.doc.createElement("me:energyAboveTheTopHill")
                self.MEmodelPar.appendChild(self.tophill)
                self.tophill.appendChild(self.doc.createTextNode(str(self.MESMERTopHill)))

                # me:control branch
                self.eigen = self.doc.createElement("me:eigenvalues")
                self.MEcontrol.appendChild(self.eigen)
                self.eigen.appendChild(self.doc.createTextNode(str(10)))
                self.calcMethod = self.doc.createElement("me:calcMethod")
                self.MEcontrol.appendChild(self.calcMethod)
                self.calcMethod.appendChild(self.doc.createTextNode("simpleCalc"))
                self.MEcontrol.appendChild(self.doc.createElement("me:hideInactive"))
                self.MEcontrol.appendChild(self.doc.createElement("me:printGrainBoltzmann"))
                self.MEcontrol.appendChild(self.doc.createElement("me:testMicroRates"))
                self.MEcontrol.appendChild(self.doc.createElement("me:testRateConstants"))
                self.MEcontrol.appendChild(self.doc.createElement("me:printGrainDOS"))
                self.MEcontrol.appendChild(self.doc.createElement("me:printGrainkbE"))
                self.MEcontrol.appendChild(self.doc.createElement("me:printGrainkfE"))
                self.MEcontrol.appendChild(self.doc.createElement("me:testDOS"))
                self.MEcontrol.appendChild(self.doc.createElement("me:printCellDOS"))
                self.MEcontrol.appendChild(self.doc.createElement("me:printSpeciesProfile"))
                self.MEcontrol.appendChild(self.doc.createElement("me:printGrainedSpeciesProfile"))
                self.diagramoffset = self.doc.createElement("me:diagramEnergyOffset")
                self.MEcontrol.appendChild(self.diagramoffset)
                self.diagramoffset.appendChild(self.doc.createTextNode(str(0)))

                # processing instruction
                self.pi1 = self.doc.createProcessingInstruction('xml-stylesheet',"type='text/xsl' href='../../mesmer1.xsl' media='screen'")
                self.doc.insertBefore(self.pi1,self.doc.firstChild)
                self.pi2 = self.doc.createProcessingInstruction('xml-stylesheet',"type='text/xsl' href='../../mesmer2.xsl' media='other'")
                self.doc.insertBefore(self.pi2,self.doc.firstChild)
                
                # write in to *.xml
                self.MESMERpath = os.path.normpath(self.iniFilePath+'/MESMER/')
                if not os.path.exists(self.MESMERpath): os.mkdir(self.MESMERpath)
                self.xmloutput = open(os.path.normpath(self.iniFilePath+'/MESMER/'+'P'+str(self.Pres[iPres]).replace('.','_')+'T'+str(self.Temp[iTemp]).replace('.','_')+'.xml'),'w')
                self.doc.writexml(self.xmloutput,'','\t','\n','utf-8')
                self.xmloutput.close()




#####################END##############################

if __name__ == '__main__':
    siteA = ReactionsIniClass(os.path.normpath(os.getcwd()+'/R512ndSiteA/R512ndSiteA.ini'))
    ##siteA.OutputReactions()
    ##siteA.WriteMESMER()
    ##siteA.WriteThermo()
    ##siteA.WriteDensum()
    ##siteA.WriteMultiWell()
    ##siteA.WriteMathematica()
    ##siteA.WriteSupInfoLaTexReactions()
    siteA.WriteJmolReactions()
