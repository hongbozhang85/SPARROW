#coding = utf-8
#!/usr/bin/python
'''
a module in SPARROW
copyright Hong-Bo Zhang
functions for converting units
'''

def UnitConvertHelp():
    print "Energy keyword: 'Har','kcalmol','kJmol','eV','cm-1','GHz','K'"
    print "Length keyword: 'Ang','Bohr'"
    print "Rontational Constant keyword: 'GHz','amuA2'. Using EnergyConvert to convert between 'GHz' and 'cm-1'"

def EnergyConvert(InE,InUnit,OutUnit):
    EneConList = ['Har','kcalmol','kJmol','eV','cm-1','GHz','K']
    if InUnit not in EneConList: print "Energy keyword: 'Har','kcalmol','kJmol','eV','cm-1','GHz','K'"
    if OutUnit not in EneConList: print "Energy keyword: 'Har','kcalmol','kJmol','eV','cm-1','GHz','K'"
    indexin = EneConList.index(InUnit)
    indexout = EneConList.index(OutUnit)
    #EneConvertFactor = [[1.0 for i in range(len(EneConList))] for i in range(len(EneConList))]
    EneConvertFactor = [
        [1.0, 627.51, 2625.5, 27.21138, 219474.63137, 6.579684E6, 3.15773E5], # 1 Har = ? other unit
        [1.593601E-3, 1.0, 4.184, 4.336411E-2, 349.755, 1.048539E4, 503.217], # 1 kcalmol = ? other unit
        [3.808798E-4, 0.239006, 1.0, 1.036427E-2, 83.5935, 2.506069E3, 120.272], # 1 kJmol = ? other unit
        [3.674931E-2, 23.0605, 96.4853, 1.0, 8065.541, 2.417988E5, 1.16045E4], # 1 eV = ? other unit
        [4.556335E-6, 2.85914E-3, 1.196226E-2, 1.239842E-4, 1.0, 2.997925E1, 1.438769], # 1 cm-1 = ? other unit
        [1.519830E-7, 9.53708E-5, 3.990313E-4, 4.135669E-6, 3.33564E-2, 1.0, 4.79922E-2 ], # 1 GHz = ? other unit
        [3.16683E-6, 1.98722E-3, 8.31451E-3, 8.61738E-5, 0.695039, 2.08367E1, 1.0] # 1 K = ? other unit
        ]
    #for i in range(7): print EneConvertFactor[5][i]*EneConvertFactor[i][5]
    OutE = InE*EneConvertFactor[indexin][indexout]
    return OutE

def LengthConvert(InL,InUnit,OutUnit):
    LenConList = ['Ang','Bohr']
    if InUnit not in LenConList: print "Length keyword: 'Ang','Bohr'"
    if OutUnit not in LenConList: print "Length keyword: 'Ang','Bohr'"
    indexin = LenConList.index(InUnit)
    indexout = LenConList.index(OutUnit)
    LenConvertFactor = [
        [1.0, 1.8897], # 1 Angstrom = ? other unit
        [0.52918, 1.0] # 1 Bohr = ? other unit
        ]
    OutL = InL * LenConvertFactor[indexin][indexout]
    return OutL

def RotConConvert(InRC,InUnit,OutUnit):
    RotConList = ['GHz','amuA2']
    if InUnit not in RotConList: print "Rontational Constant keyword: 'GHz','amuA2'. Using EnergyConvert to convert between 'GHz' and 'cm-1'"
    if OutUnit not in RotConList: print "Rontational Constant keyword: 'GHz','amuA2'. Using EnergyConvert to convert between 'GHz' and 'cm-1'"
    if InUnit == 'GHz' :
        if OutUnit == 'GHz' :
            OutRC = InRC*1.0
        elif OutUnit == 'amuA2' :
            OutRC = 5.0538E2 / InRC
    elif InUnit == 'amuA2':
        if OutUnit == 'GHz':
            OutRC = 5.0538E2 / InRC
        if OutUnit == 'amuA2':
            OutRC = InRC
    return OutRC

##UnitConvertHelp()
##print EnergyConvert(InE=1.0,InUnit='Har',OutUnit='kcalmol')
##print LengthConvert(InL=1.0,InUnit='Bohr',OutUnit='Ang')
##print RotConConvert(InRC=0.29958,InUnit='GHz',OutUnit='amuA2')
