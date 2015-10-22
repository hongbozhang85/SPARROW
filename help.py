#coding=utf-8
#!/usr/bin/python

#class ClassPackageHelp():
#    'Documentation for SPARROW'
#    def ShowAlias(self):
#        print ("The alias name of this package is: %s" % ClassPackageHelp.PackageAlias


PackageHelp = {'PackageAlias':'SPARROW','PackageFullName':'Systematical Python Assistant for Reaction Rate cOefficient Widget','Update':'','Version':''}
PackageUpdateHistory=[]

def UpdateVersion(PackageHelp,PackageUpdateHistory,Update,Version):
    PackageHelp["Update"]= Update
    PackageHelp["Version"]= Version
    PackageUpdateHistory += [[Update,Version]]

def PackageHelpOutput():
    print ("The name of this package is: %s" % PackageHelp['PackageFullName'])
    print ("The alias name of this package is: %s" % PackageHelp['PackageAlias'])
    print ("The version: %s" % PackageHelp['Version'])
    print ("The most recent update: %s" % PackageHelp['Update'])
    print ("Python 2.7")

def PackageUpdateHistoryOutput():
    for i in PackageUpdateHistory:
        print i


UpdateVersion(PackageHelp,PackageUpdateHistory,'2015-01-15:2015-01-24','V0.alpha')
UpdateVersion(PackageHelp,PackageUpdateHistory,'2015-01-24:2015-01-28','V0.beta')


PackageHelpOutput()
PackageUpdateHistoryOutput()

V0gamma = '''V0.gamma,
FUNCTIONS ADDED:
	user speicified initial directory in 'A Single PES' in GUI
	debug the function WriteMathematica 15-02-04
	debug the function WriteMathematica and function ReadGaussian 15-02-07
	add function WriteJmol: generate *.jpg of the molecule and animation of the spinning molecule 15-02-10
	debug WriteMESMER: the order of two ProcessingInstruction 15-02-24 
	add a module PostProcess. SymmetryNumber() is finished. 15-02-24
	debug WriteThermo: i%3 -> i%self.NumberofReactions 15-03-02
TODO and NOTICE:
	window's gaussian's output *.out is not supported! Since /HF=.../ in Linux version, but |HF=...| in windows version.
	read energy: \HF=...\ may be splitted into two lines.
'''


V0beta = '''V0.beta,
FUNCTIONS ADDED:
	write *.tex and generate *.dvi, *.ps and *.pdf
	GUI tkinter
TODO and NOTICE:
	Only JPG and EPS are supported in WriteLaTeX. TIF is not supported by any complier of latex, but we can convert it to png and then pdflatex.
	GUI: TKinter in current version. Other advanced GUI such as PyQt4 will be developed in the future.
	executable format
'''


V0alpha = '''V0.alpha, 
FUNCTIONS:
	1. Read a *.log/out file, and output *.param under the path /../KeyParams where ./ is the directory of *.log/out
	2. Read a PES, i.e., a set of log/out files, and output *.param files
	3. Read a PES and generate multiwell, thermo, densum, mesmer and mathematica input.
USAGE:
	1. if working directory is ./
	2. create *.ini under ./ and write information of PES in *.ini
	3. put all the *.log/out under ./Gaussian/
	4. uncomment/modify relevant lines on the bottom of Reactions.py or write a driver importing Reactions.py
	5. run
TODO and NOTICE:
	G3B3 CBSQB3 guess = (...) are not supported
    Energy keyword: 'Har','kcalmol','kJmol','eV','cm-1','GHz','K'
    Length keyword: 'Ang','Bohr'
    Collision model: exponential model with default DeltaEdown = 260cm-1 without considering T dependence
    Default LJ parameters: from H. Wang and M. Frenklach C&F 1994
    1 atom molecule is not supported at present
    Only first 20 Elements in Elements Periodic Table
    *.log and *.out must in initial case. Stupid design
	Reactions check routine: such as: check whether all the log file have the same method and base set
	OutputMolecules.py should be combined with DataClass.py, and OutputReactions should be a method in Class MoleculeClass
    ReactionsIniClass: MESMER only includes (TopHill,GrainSize); MultiWell only 'Default' is allowed
	Bath gas : Ar
	only read one imaginary freq, so if there are more than one imaginary freqs, no warning will be given
	Torsion is not supported: atomlist,bondlist,hinder...
	pressure in the unit of atm
	Thermo: 1000~2000 K
	optical number = 1; electronic energy level = 1
	All try... except haven't been coded yet.
	Many repeated codes, such as calc scaled ZPE, energy barrier, find index of molecule from its name and so on. 
	The reactant in the first reaction in inifile is the initial well or extrance
	In nbfragment.dat the order of the TraS is not good
	copy template of *.nb to /PES
'''
