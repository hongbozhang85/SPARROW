#coding=utf-8
#!/usr/bin/python
'''
a module in SPARROW
copyright Hong-Bo Zhang
Read Gaussian .log or .out files
'''

import os
import re
import math

class MoleculeClass:
    'data type of a molecule calcualted by Gaussian'
    def __init__(self,Directory,MolName):
        # file and directory
        self.MolName = MolName
        self.Directory = Directory
        if os.path.exists(os.path.join(self.Directory,self.MolName+'.log')):
            self.OutputName = os.path.join(self.Directory,self.MolName+'.log')
        elif os.path.exists(os.path.join(self.Directory,self.MolName+'.out')):
            self.OutputName = os.path.join(self.Directory,self.MolName+'.out')
        else :
            print 'Warning: there is no ', MolName
        print ("Molecule: %s" %self.OutputName)
        # primary data        
        self.Gaussian = ''
        self.Charge = 0
        self.SpinMulti = 1
        self.Spin2 = 0.0
        self.Spin2A = 0.0
        self.EleEnergy = 0.0
        self.RotCon= []
        self.MolFormula = ''
        self.Mass = 0.0
        self.Freq = []
        self.Coordinate = []
        self.CalcKeywords = ''
        self.DoF = 0
        self.ExternalSymm = '1???'
        # un-nessaccary data
        self.ZeroPointCorrectRead = 0.0
        self.ZPERead = 0.0
        # derived data
        self.ScaleFactor = 0.968 #check
        self.CalcType = ''
        self.MethodBase = ''
        self.LJepsilon = 0.0
        self.LJsigma = 0.0
        self.AdRot = 0.0
        self.KRot = 0.0
        # assitant data
        self.Help = ("All energies are in the unit of Hartree, rotational consants in GHz, mass in amu, frequencies in Kelvin, coordinates in Angstrom, DeltaEDown in cm-1, LJsigma in Angstrom, LJepsilon in Kelvin")
        # missing data in Gaussian
        self.DeltaEDown = 260.0

    def SetDeltaEDown(self,DeltaE):
        self.DeltaEDown = DeltaE
        
    def ReadGaussian(self,debug):
        
        # open and read Gaussian file
        self.FileIO = open(self.OutputName,'r')
        print "Reading File: ",self.FileIO.name
        self.String = self.FileIO.read()

        # check Error Termination or Normal Termination
        if re.search('Error termination(.*)\n',self.String):
            print "Warning: ", re.search('Error termination(.*)\n',self.String).group().strip()
        # read Gaussian version
        if debug==1: print "previous: ",self.Gaussian
        self.Gaussian = re.search('\n(.*)\n',re.search('Cite this work as:\n (.*)\n',self.String).group()).group().strip()
        if debug==1: print "present: ",self.Gaussian
        
        # Calculation Keywords and Calc Type: Saddle point or Local mimima. imaginary frequency
        if debug == 1: print "previous: ",self.CalcKeywords
        self.CalcKeywords = re.search('#(.*)\n',self.String).group().strip()
        if debug == 1: print "present: ",self.CalcKeywords
        if debug == 1: print "previous: ",self.CalcType
        if re.search('Mod|IRC|scan',self.CalcKeywords,re.I):
            print ('Warning: scan or IRC job instead of opt or TS')
        if re.search('G3B3|CBS|QB3',self.CalcKeywords,re.I):
            print ('Warning: NOT supported in this version')
        if re.search('TS|ts|tS|Ts|QST2|QSt2|QsT2|qST2|Qst2|qSt2|qsT2|qst2|QST3|QSt3|QsT3|qST3|Qst3|qSt3|qsT3|qst3',self.CalcKeywords):
            self.CalcType = 'Saddle Point'
            self.ImagFreq = 0.0
            self.ImagFreq = float(re.search(' Frequencies --( *)-(\d+)\.(\d+) ',self.String).group().replace(' Frequencies --','').strip())
            #print self.ImagFreq
        else :
            self.CalcType = 'Local Minima'
        if debug == 1: print "present: ",self.CalcType
        
        # find out the method and base set
        if debug == 1: print "previous: ",self.MethodBase
        if re.search('opt( *)=( *)\(',self.CalcKeywords,re.I): # opt = (...)
            self.temp1 = re.search( 'opt(.*?)\)',self.CalcKeywords,re.I )
        elif re.search('opt( *)=',self.CalcKeywords,re.I): # opt = ...
            self.temp1 = re.search('opt( *)=( *)(\w+)',self.CalcKeywords,re.I)
        elif re.search('opt( *)\(',self.CalcKeywords,re.I): # opt (...)
            self.temp1 = re.search('opt(.*?)\)',self.CalcKeywords,re.I)
        elif re.search('opt',self.CalcKeywords,re.I): # opt alone
            self.temp1 = re.search('opt',self.CalcKeywords,re.I)
        else : # there is no opt
            print ("Warning: There is no keyword 'opt'. LOOK STRANGE")
        self.temp2 = self.CalcKeywords.replace(self.temp1.group(),'')
        if re.search('freq',self.temp2,re.I):
            self.temp2 = self.temp2.replace('freq','')
        if re.search('nosymm',self.temp2,re.I):
            self.temp2 = self.temp2.replace('nosymm','')
        if re.search('geom=connectivity',self.temp2,re.I):
            self.temp2 = self.temp2.replace('geom=connectivity','')
        if re.search('guess',self.temp2,re.I):
            self.tempt = re.search('guess( *)=(\w*)',self.temp2,re.I)
            self.temp6 = self.temp2.replace(self.tempt.group(),'')
        else :
            self.temp6 = self.temp2
        if re.search('scf( *)=( *)\(',self.temp6,re.I): # scf = (...)
            self.temp7 = re.search( 'scf(.*?)\)',self.temp6,re.I ).gourp()
        elif re.search('scf( *)=',self.temp6,re.I): # scf = ...
            self.temp7 = re.search('scf( *)=( *)(\w+)',self.temp6,re.I).group()
        elif re.search('scf( *)\(',self.temp6,re.I): # scf (...)
            self.temp7 = re.search('scf(.*?)\)',self.temp6,re.I).group()
        elif re.search('scf',self.temp6,re.I): # scf alone
            self.temp7 = re.search('scf',self.temp6,re.I).group()
        else :
            self.temp7 = self.temp6
        self.MethodBase = self.temp7.replace('#','').strip()
        if debug == 1: print "present: ",self.MethodBase

        # determind the scale factor
        if debug == 1: print "previous: ",self.ScaleFactor
        if re.search('b3lyp\/6\-31g\(d\)',self.CalcKeywords,re.I):
            self.ScaleFactor = 0.961
        elif re.search('b3lyp\/6\-311\+g\(d,p\)',self.CalcKeywords,re.I):
            self.ScaleFactor = 0.968
        else:
            self.ScaleFactor = 1.0
        if debug == 1: print "present: ",self.ScaleFactor

        # Charge
        if debug == 1: print "previous: ",self.Charge
        self.Charge = int(re.search('Charge( *)=( *)\d',self.String).group().replace('Charge =','').strip())
        if debug == 1: print "present: ",self.Charge

        # Spin Multiplicity
        if debug == 1: print "previous: ",self.SpinMulti
        self.SpinMulti = int(re.search('Multiplicity( *)=( *)\d',self.String).group().replace('Multiplicity =','').strip())
        if debug == 1: print "present: ",self.SpinMulti

        # Molecule Stoichiometry Formula
        if debug == 1: print "previous: ",self.MolFormula
        self.MolFormulatemp = re.search('Stoichiometry(.*)\n',self.String).group().replace('Stoichiometry','').strip()
        if self.SpinMulti == 1:
            self.MolFormula = self.MolFormulatemp
        else :
            self.MolFormula = self.MolFormulatemp.replace('('+str(self.SpinMulti)+')','').strip()
        if debug == 1: print "present: ",self.MolFormula

        # Molecular Mass
        if debug == 1: print "previous: ",self.Mass, self.LJsigma, self.LJepsilon
        self.Mass = float(re.search('Molecular mass:(.*)\n',self.String).group().replace('Molecular mass:','').replace('amu.','').strip())
        self.LJsigma = 1.234*pow(self.Mass,0.33)
        self.LJepsilon = 37.15*pow(self.Mass,0.58)
        if debug == 1: print "present: ",self.Mass, self.LJsigma, self.LJepsilon

        # S^2 and Spin2A
        if debug == 1: print "previous: ",self.Spin2,self.Spin2A
        if re.search('S2=(.*?)\\\\',self.String):
            self.Spin2 = float(re.search('S2=(.*?)\\\\',self.String).group().replace('S2=','').replace('\\','').strip())
            self.Spin2A = float(re.search('S2A=(.*?)\\\\',self.String).group().replace('S2A=','').replace('\\','').strip())
        if debug == 1: print "present: ",self.Spin2,self.Spin2A

        # Degrees of Freedom
        if debug == 1: print "previous: ",self.DoF
        self.DoF = int(re.search('Deg. of freedom(.*)\n',self.String).group().replace('Deg. of freedom','').strip())
        if debug == 1: print "present: ",self.DoF

        # Rotational Constant
        if debug == 1: print "previous: ",self.RotCon
        self.RotContemp = re.search('Rotational temperature(s*) \(Kelvin\)(.*)\n Rotational constant(s*) \(GHZ\):(.*)\n',self.String).group()
        self.RotContemp2 = re.search('Rotational temperature(s*) \(Kelvin\)(.*)\n',self.RotContemp).group()
        self.RotContemp3 = re.sub('Rotational constant(s*) \(GHZ\):','',self.RotContemp.replace(self.RotContemp2,'')).strip()
        self.RotContemp4 = re.sub(' +',',',self.RotContemp3)
        self.RotCon = [0.0 for i in range(len(self.RotContemp4.split(',')))]
        for i in range(len(self.RotContemp4.split(','))): self.RotCon[i] = float(self.RotContemp4.split(',')[i])
        if len(self.RotCon) == 1:
            self.AdRot = self.RotCon[0]
        else :
            self.RotConSort = sorted(self.RotCon)
            if self.RotConSort[2]/self.RotConSort[1] > self.RotConSort[1]/self.RotConSort[0] :
                self.KRot = self.RotConSort[2]
                self.AdRot = math.sqrt(self.RotConSort[0]*self.RotConSort[1])
            else :
                self.KRot = self.RotConSort[0]
                self.AdRot = math.sqrt(self.RotConSort[1]*self.RotConSort[2])
        if debug == 1: print "present: ",self.RotCon

        # Harmonic Frequencies
        if debug == 1: print "previous: ",self.Freq
        self.FreqTemp = re.search(' Vibrational temperatures:(((.*)\n)*) Zero-point correction=',self.String).group()
        self.FreqTemp2 = re.sub(' +',',',re.sub('[^\d\. ]','',self.FreqTemp).strip())
        self.Freq = [0.0 for i in range(len(self.FreqTemp2.split(',')))]
        for i in range(len(self.FreqTemp2.split(','))):
            self.Freq[i] = float(self.FreqTemp2.split(',')[i])
        if debug == 1: print 'present: Harmonic Frequencies ( in Kelvin): ',self.Freq
        if debug == 1: print ('There are %d normal modes in total' %len(self.Freq))

        # Electronic Energy
        if debug == 1: print "previous: ",self.EleEnergy
        self.EleEnergy = float(re.search('\\\\HF=(.*?)\\\\',self.String).group().replace('\\HF=','').replace('\\',''))
        if debug == 1: print "present: ", self.EleEnergy

        # zero-point correction read from Gaussian output
        if debug == 1: print "previous: ",self.ZeroPointCorrectRead,self.ZPERead
        self.ZeroPointCorrectRead = float(re.search('Zero-point correction=(.*)\n',self.String).group().replace('Zero-point correction=','').replace('(Hartree/Particle)','').strip())
        if debug == 1: print 'present: zero-point correction read from Gaussian output is ', self.ZeroPointCorrectRead
        self.ZPERead = float(re.search('Sum of electronic and zero-point Energies=(.*)\n',self.String).group().replace('Sum of electronic and zero-point Energies=','').strip())
        if debug == 1: print 'present: Enthalphy at 0 K read from Gaussian output is ',self.ZPERead

        # coordinate
        if debug == 1: print "previous: ",self.Coordinate
        self.CoordinateTemp = re.findall('Standard orientation:(?:.*)\n(?:(?:(?:.*)\n)*?) Rotational constants(?:.*)\n',self.String)
        self.CoordinateTemp1 = self.CoordinateTemp[len(self.CoordinateTemp)-1]
        self.CoordinateTemp2 = re.sub('--------------(.*)\n Rotational constants(.*)\n','',re.sub('Standard orientation:(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n','',self.CoordinateTemp1)).strip()
        self.CoordinateTemp3 = re.sub('\n( *)','\n',self.CoordinateTemp2)
        self.CoordinateTemp4 = re.sub('\n',',',re.sub(' +',',',self.CoordinateTemp3))
        self.Coordinate = [ [0,0,0,0.0,0.0,0.0] for i in range(len(self.CoordinateTemp4.split(','))/6)]
        for i in range(len(self.CoordinateTemp4.split(','))/6) :
            self.Coordinate[i][0] = int(self.CoordinateTemp4.split(',')[6*i])
            self.Coordinate[i][1] = int(self.CoordinateTemp4.split(',')[6*i+1])
            self.Coordinate[i][2] = int(self.CoordinateTemp4.split(',')[6*i+2])
            self.Coordinate[i][3] = float(self.CoordinateTemp4.split(',')[6*i+3])
            self.Coordinate[i][4] = float(self.CoordinateTemp4.split(',')[6*i+4])
            self.Coordinate[i][5] = float(self.CoordinateTemp4.split(',')[6*i+5])
        if debug == 1: 
            for i in range(len(self.CoordinateTemp4.split(','))/6) :
                print self.Coordinate[i] 

        # close Gaussian file and clear buffer
        print "Finish Reading File: ",self.OutputName,"\nClosing File and Clearing Buffers"
        self.FileIO.close()
        del self.String
        del self.temp1
        del self.temp2
        del self.temp6
        del self.temp7
        del self.MolFormulatemp
        del self.RotContemp
        del self.RotContemp2
        del self.RotContemp3
        del self.RotContemp4
        del self.FreqTemp
        del self.FreqTemp2
        del self.CoordinateTemp
        del self.CoordinateTemp1
        del self.CoordinateTemp2
        del self.CoordinateTemp3
        del self.CoordinateTemp4

###########################END OF CLASS MoleculeClass######################################    


##print ("current directory: ",os.getcwd())
##IM2 = MoleculeClass(os.path.normpath(os.getcwd()+'/Gaussian'),'IM2')
##IM2.ReadGaussian(0)
##print '\n****'
##for i in dir(IM2):
##    print i,getattr(IM2,i)


