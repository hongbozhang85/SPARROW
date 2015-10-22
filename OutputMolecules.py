#coding = utf-8
#!/usr/bin/python
'''
a module in SPARROW
copyright Hong-Bo Zhang
write the key informations in *.log/out into files for further application
'''

import os
import re
import platform
import DataClass
import UnitConvert

#JmolJarPath = os.path.normpath('D:\Jmol-13.3.5-binary\jmol-13.3.5\jmol')
JmolJarPath = os.path.normpath('D:\Jmol-13.3.5-binary\jmol-13.3.5')


def ToElement(index):
    ElementList = ['H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar','K','Ca']
    return ElementList[index-1]

def WriteJmol(Mol): # Mol belongs to class MoleculeClass
    'generate the image in JPG and animation in gif'

    # mkdir and open file
    SupInfoPath = os.path.normpath(Mol.Directory+'/../SupInfo/')
    if not os.path.exists(SupInfoPath): os.mkdir(SupInfoPath)
    JmolPath = os.path.normpath(SupInfoPath+'/JmolScript/')
    if not os.path.exists(JmolPath): os.mkdir(JmolPath)
    PicPath = os.path.normpath(SupInfoPath+'/Image/')
    if not os.path.exists(PicPath): os.mkdir(PicPath)
    RotGifPath = os.path.normpath(SupInfoPath+'/SpinGif/')
    if not os.path.exists(RotGifPath): os.mkdir(RotGifPath)

    # image of molecule
    JmolFile = open(os.path.join(JmolPath,Mol.MolName+'.jmol'),'w')
    JmolFile.write('#Created by SPARROW\n\n')
    JmolFile.write(('load "'+Mol.OutputName+'"\n').replace('\\','/'))
    JmolFile.write( ('fileName = "'+PicPath+'\\'+Mol.MolName+'.jpg"\n').replace('\\','/')  )
    JmolFile.write('frank off\n')
    JmolFile.write('background [255, 255, 255]\n')
    JmolFile.write('set echo top center;font echo 24 serif;color echo white\nset zoomLarge false\n')
    JmolFile.write('write image jpg @fileName\n')
    JmolFile.write('quit\n')
    JmolFile.close()
    nowdirec = os.getcwd()
    os.chdir(JmolJarPath)
    os.system( 'jmol -xs %s' % os.path.join(JmolPath,Mol.MolName+'.jmol')) # jmol -ioxs
    os.chdir(nowdirec)

    # spinning molecule animation
    JmolFile = open(os.path.join(JmolPath,Mol.MolName+'Spin.jmol'),'w')
    JmolFile.write('#Created by SPARROW\n\n')
    JmolFile.write(('load "'+Mol.OutputName+'"\n').replace('\\','/'))
    JmolFile.write( ('name = "'+RotGifPath+'\\'+Mol.MolName+'000.jpg"\n').replace('\\','/')  )
    JmolFile.write('nFrames = 36 \n')
    JmolFile.write('nDegrees = 10 \n')
    JmolFile.write('thisDegree = 0 \n')
    JmolFile.write('#width = 640\n#height = 480\n')
    JmolFile.write('background [0, 0, 0]\nfrank off\n')
    JmolFile.write('set echo top center\nfont echo 24 serif\ncolor echo white\nset zoomLarge false\n')
    JmolFile.write('spin on\n')
    JmolFile.write('for (var i = 1; i <= nFrames; i = i + 1)\n')
    JmolFile.write('\tthisDegree = thisDegree  + nDegrees\n')
    JmolFile.write('\tdegreeText = "Degree = " + thisDegree + ""\n')
    JmolFile.write('\tfileName = name.replace("000","" + ("000" + thisDegree)[-2][0])\n')
    JmolFile.write('\t#rotate x @nDegrees  # use these options if you want to rotate the molecule\n')
    JmolFile.write('\trotate y @nDegrees\n')
    JmolFile.write('\t#rotate z @nDegrees\n')
    JmolFile.write('\t#frame next # only use this if you have a multiframe file.\n')
    JmolFile.write('\techo @degreeText\n')
    JmolFile.write('\trefresh\n')
    JmolFile.write('\t#write image jpg @width @height @fileName\n')
    JmolFile.write('\twrite image jpg @fileName\n')
    JmolFile.write('end for\n')
    JmolFile.write('spin off\n')
    JmolFile.write('quit\n')
    JmolFile.close()
    nowdirec = os.getcwd()
    MencoderPath = os.getcwd()
    os.chdir(JmolJarPath)
    os.system('jmol -ioxs %s'% os.path.join(JmolPath,Mol.MolName+'Spin.jmol'))
    os.chdir(nowdirec)
    if platform.system()=='Windows':
        os.chdir(RotGifPath)
        #os.system('copy '+MencoderPath+'\\mencoder.exe '+RotGifPath+'\\mencoder.exe')
        os.system(MencoderPath+'\\mencoder mf://*.jpg -o '+Mol.MolName+'.avi -ovc lavc -lavcopts vcodec=msmpeg4v2:autoaspect:vbitrate=2160000:mbd=2:keyint=132:vqblur=1.0:cmp=2:subcmp=2:dia=2:mv0:last_pred=3 -fps 8 > NUL 2>&1') 
        os.system('del *.jpg')
    elif platform.system()=='Linux':
        os.chdir(RotGifPath)
        os.system('convert *.jpg %s' % Mol.MolName+'.gif')
        os.system('rm *.jpg')
        #os.system('mencoder  mf://*.jpg -o %s -ovc lavc -lavcopts vcodec=msmpeg4v2:autoaspect:vbitrate=2160000:mbd=2:keyint=132:vqblur=1.0:cmp=2:subcmp=2:dia=2:mv0:last_pred=3 -fps 8 > NUL 2>&1' % Mol.MolName+'.avi')
    else:
        print 'Warning: Neither Windows nor Linux, no spinning animation was generated.'
    os.chdir(nowdirec)
    #print os.getcwd()


def WriteSupInfoLaTeX(Mol): # Mol is belongs to class MoleculeClass
    'write the supporing information in doc or xls format'

    # mdkir and open file
    MolPath = os.path.normpath(Mol.Directory+'/../SupInfo/')
    if not os.path.exists(MolPath): os.mkdir(MolPath)
    MolPath = os.path.normpath(MolPath+'/LaTeX/')
    if not os.path.exists(MolPath): os.mkdir(MolPath)
    MolFile = open(os.path.join(MolPath,Mol.MolName+'.tex'),'w')
    PicPath = os.path.normpath(MolPath+'/../Image/')
    if not os.path.exists(PicPath): os.mkdir(PicPath)

    MolFile.write('\documentclass[10pt]{article}\n')
    MolFile.write('\usepackage{multirow}\n')
    MolFile.write('\usepackage{graphicx}\n')
    MolFile.write('\usepackage[a4paper]{geometry} \n\geometry{verbose,tmargin=3cm,bmargin=3cm,lmargin=2cm,rmargin=2cm}\n')
    MolFile.write('\n')
    MolFile.write('\\begin{document}\n')
    MolFile.write('\n')
    picType = ''
    if os.path.isfile(os.path.join(PicPath,Mol.MolName+'.eps')): #.eps')):
        picType = 'EPS'
        MolFile.write('\\begin{figure}\n')
        MolFile.write('\centering\n')
        MolFile.write('\includegraphics[width=\\textwidth]{%s}\n'%  os.path.join(PicPath,Mol.MolName+'.eps').replace('\\','/'))#%Mol.MolName+'.eps')#
        MolFile.write('\caption{Geometry structure of %s}\n'% Mol.MolName)
        MolFile.write('\end{figure}\n')
        MolFile.write('\n')
    elif os.path.isfile(os.path.join(PicPath,Mol.MolName+'.jpg')): #.eps')):
        picType = 'JPG'
        MolFile.write('\\begin{figure}\n')
        MolFile.write('\centering\n')
        MolFile.write('\includegraphics[width=0.5\\textwidth]{%s}\n'%  os.path.join(PicPath,Mol.MolName+'.jpg').replace('\\','/'))#%Mol.MolName+'.eps')#
        MolFile.write('\caption{Geometry structure of %s}\n'% Mol.MolName)
        MolFile.write('\end{figure}\n')
        MolFile.write('\n')
    MolFile.write('\\begin{table}\n')
    MolFile.write('\caption{The geometry configuration, frequencies and rotational constants of %s}\n' % Mol.MolName)
    MolFile.write('\centering\n')
    MolFile.write('\\begin{centering}\n')
    MolFile.write('\\begin{tabular}{|c c c c| c c c|}\n')
    MolFile.write('\hline\n')
    MolFile.write('\multicolumn{4}{|c|}{Geometry Configuration ($\AA$)} & \multicolumn{3}{|c|}{Unscaled Frequencies ($cm^{-1}$)} \n')
    MolFile.write('\\tabularnewline\n')
    MolFile.write('\hline\n')
    for i in range(len(Mol.Coordinate)):
        if i < (len(Mol.Coordinate)-2-1):
            MolFile.write('%s & \qquad %10.6f & \qquad %10.6f & \qquad %10.6f & \qquad %7.1f & \qquad %7.1f & \qquad %7.1f\n' % ((ToElement(Mol.Coordinate[i][1]),Mol.Coordinate[i][3],Mol.Coordinate[i][4],Mol.Coordinate[i][5],UnitConvert.EnergyConvert(InE=Mol.Freq[i*3],InUnit='K',OutUnit='cm-1'),UnitConvert.EnergyConvert(InE=Mol.Freq[i*3+1],InUnit='K',OutUnit='cm-1'),UnitConvert.EnergyConvert(InE=Mol.Freq[i*3+2],InUnit='K',OutUnit='cm-1'))) )
            MolFile.write('\\tabularnewline\n')
        elif i == (len(Mol.Coordinate)-2-1):
            if (len(Mol.Freq) == 3*len(Mol.Coordinate) - 7) and (Mol.CalcType == 'Saddle Point'):
                MolFile.write('%s & \qquad %10.6f & \qquad %10.6f & \qquad %10.6f & \qquad %7.1f & \qquad %7.1f & \qquad %7.1f\n' % ((ToElement(Mol.Coordinate[i][1]),Mol.Coordinate[i][3],Mol.Coordinate[i][4],Mol.Coordinate[i][5],UnitConvert.EnergyConvert(InE=Mol.Freq[i*3],InUnit='K',OutUnit='cm-1'),UnitConvert.EnergyConvert(InE=Mol.Freq[i*3+1],InUnit='K',OutUnit='cm-1'),Mol.ImagFreq)) )
                MolFile.write('\\tabularnewline\n')
            else :
                MolFile.write('%s & \qquad %10.6f & \qquad %10.6f & \qquad %10.6f & \qquad %7.1f & \qquad %7.1f & \qquad %7.1f\n' % ((ToElement(Mol.Coordinate[i][1]),Mol.Coordinate[i][3],Mol.Coordinate[i][4],Mol.Coordinate[i][5],UnitConvert.EnergyConvert(InE=Mol.Freq[i*3],InUnit='K',OutUnit='cm-1'),UnitConvert.EnergyConvert(InE=Mol.Freq[i*3+1],InUnit='K',OutUnit='cm-1'),UnitConvert.EnergyConvert(InE=Mol.Freq[i*3+2],InUnit='K',OutUnit='cm-1'))) )
                MolFile.write('\\tabularnewline\n')
        elif i == len(Mol.Coordinate)-2 :
            if (len(Mol.Freq) == 3*len(Mol.Coordinate) - 5) and (Mol.CalcType == 'Local Minima'): # IM and linear
                MolFile.write('%s & \qquad %10.6f & \qquad %10.6f & \qquad %10.6f & \qquad %7.1f & & \n' % (ToElement(Mol.Coordinate[i][1]),Mol.Coordinate[i][3],Mol.Coordinate[i][4],Mol.Coordinate[i][5],UnitConvert.EnergyConvert(InE=Mol.Freq[i*3],InUnit='K',OutUnit='cm-1'))) 
                MolFile.write('\\tabularnewline\n')
            elif (len(Mol.Freq) == 3*len(Mol.Coordinate) - 6) and (Mol.CalcType == 'Saddle Point'): # TS and linear
                MolFile.write('%s & \qquad %10.6f & \qquad %10.6f & \qquad %10.6f & \qquad %7.1f & & \n' % (ToElement(Mol.Coordinate[i][1]),Mol.Coordinate[i][3],Mol.Coordinate[i][4],Mol.Coordinate[i][5],Mol.ImagFreq)) 
                MolFile.write('\\tabularnewline\n')
            else:
                MolFile.write('\cline{5-7}\n')
                MolFile.write('%s & \qquad %10.6f & \qquad %10.6f & \qquad %10.6f & \multicolumn{3}{|c|}{Rotational Constants ($amu*\AA^2$)} \n' % ((ToElement(Mol.Coordinate[i][1]),Mol.Coordinate[i][3],Mol.Coordinate[i][4],Mol.Coordinate[i][5])) )
                MolFile.write('\\tabularnewline\n')
        elif i > len(Mol.Coordinate)-2:
            if ((len(Mol.Freq) == 3*len(Mol.Coordinate) - 5) and (Mol.CalcType == 'Local Minima') ) or ((len(Mol.Freq) == 3*len(Mol.Coordinate) - 6) and (Mol.CalcType == 'Saddle Point') ):
                MolFile.write('\cline{5-7}\n')
                MolFile.write('%s & \qquad %10.6f & \qquad %10.6f & \qquad %10.6f & \multicolumn{2}{|c|}{Rotational Constants ($amu*\AA^2$)} & \qquad %10.2f \n' % (ToElement(Mol.Coordinate[i][1]),Mol.Coordinate[i][3],Mol.Coordinate[i][4],Mol.Coordinate[i][5],UnitConvert.RotConConvert(InRC=Mol.RotCon[0],InUnit='GHz',OutUnit='amuA2') ))
                MolFile.write('\\tabularnewline\n')
            else:
                #if len(Mol.RotCon) != 1:
                    MolFile.write('\cline{5-7}\n')
                    MolFile.write('%s & \qquad %10.6f & \qquad %10.6f & \qquad %10.6f & \qquad %10.2f & \qquad %10.2f & \qquad %10.2f \n' % (ToElement(Mol.Coordinate[i][1]),Mol.Coordinate[i][3],Mol.Coordinate[i][4],Mol.Coordinate[i][5],UnitConvert.RotConConvert(InRC=Mol.RotCon[0],InUnit='GHz',OutUnit='amuA2'),UnitConvert.RotConConvert(InRC=Mol.RotCon[1],InUnit='GHz',OutUnit='amuA2'),UnitConvert.RotConConvert(InRC=Mol.RotCon[2],InUnit='GHz',OutUnit='amuA2'))) 
                    MolFile.write('\\tabularnewline\n')
                #else :
                 #   MolFile.write('\cline{5-7}\n')
                  #  MolFile.write('%s & \qquad %10.6f & \qquad %10.6f & \qquad %10.6f & \qquad %10.2f &  &  \n' % (ToElement(Mol.Coordinate[i][1]),Mol.Coordinate[i][3],Mol.Coordinate[i][4],Mol.Coordinate[i][5],UnitConvert.RotConConvert(InRC=Mol.RotCon[0],InUnit='GHz',OutUnit='amuA2'))) 
                   # MolFile.write('\\tabularnewline\n')
    #MolFile.write(' atom & x & y & z\n')
    MolFile.write('\hline\n')
    MolFile.write('\end{tabular}\n')
    MolFile.write('\end{centering}\n')
    MolFile.write('\end{table}\n')
    MolFile.write('\end{document}\n')

    MolFile.close()

    
    nowdirec = os.getcwd()
    if picType == 'JPG':
        os.chdir(PicPath)
        os.system('ebb %s'%os.path.join(PicPath,Mol.MolName+'.jpg')) # for *.jpg type 
    os.chdir(MolPath)
    tex_file = os.path.join(MolPath,Mol.MolName+'.tex')
    # remove old files
    #if os.path.isfile(tex_file.replace('.tex', '.pdf')):
     # os.remove(tex_file.replace('.tex', '.pdf')) 
    # Compile tex to dvi
    os.system('latex {}'.format(tex_file))
    os.system('latex {}'.format(tex_file))
    # Complile dvi to ps
    dvi_file = tex_file.replace('.tex', '.dvi')
    os.system('dvips {}'.format(dvi_file))
    # Compile ps to pdf
    ps_file = tex_file.replace('.tex', '.ps')
    os.system('ps2pdf {}'.format(ps_file))
##    os.system('pdflatex {}'.format(tex_file))
    # Clean files
    if os.path.isfile(tex_file.replace('.tex', '.log')):
      os.remove(tex_file.replace('.tex', '.log'))
    if os.path.isfile(tex_file.replace('.tex', '.aux')):  
      os.remove(tex_file.replace('.tex', '.aux'))
    if os.path.isfile(tex_file.replace('.tex', '.bbl')):
      os.remove(tex_file.replace('.tex', '.bbl'))
    if os.path.isfile(tex_file.replace('.tex', '.blg')):
      os.remove(tex_file.replace('.tex', '.blg'))
    if picType == 'JPG':
        os.chdir(PicPath)
        os.remove(os.path.join(PicPath,Mol.MolName+'.bb'))
    os.chdir(nowdirec)
    

def WriteMolintoFile(Mol): # Mol is belongs to class MoleculeClass
    'write the key informations in *.log/out into files for further application'

    # mkdir and open file
    MolPath = os.path.normpath(Mol.Directory+'/../KeyParams/')
    if not os.path.exists(MolPath): os.mkdir(MolPath)
    MolFile = open(os.path.join(MolPath,Mol.MolName+'.param'),'w')

    # write title:
    MolFile.write('Created by SPARROW\n')
    MolFile.write('Key parameters extracted from '+Mol.OutputName+'\n')
    MolFile.write(Mol.MolName+' is generated by '+Mol.Gaussian+'\n')
    MolFile.write('Gaussian keyword session: '+Mol.CalcKeywords+'\n')
    MolFile.write('Calculation type: '+Mol.CalcType+'\n')
    MolFile.write('Quantum chemistry method and base set used: '+Mol.MethodBase+'\n')
    MolFile.write('The corresponding scale factor is: '+str(Mol.ScaleFactor)+'\n')
    MolFile.write('\n')

    # write informations except rotational constants, harmonic freqs, energy and coordinate
    MolFile.write('Charge: %d \n'%Mol.Charge)
    MolFile.write('Spin Multiplicity: %d \n'%Mol.SpinMulti)
    MolFile.write('Molecular Formula: %s \n'%Mol.MolFormula)
    MolFile.write('Degrees of freedom: %d \n'%Mol.DoF)
    MolFile.write('S2 and S2A is %f and %f, respectively. \n' %(Mol.Spin2,Mol.Spin2A))
    MolFile.write('External Symmetry in Gaussian .log or .out file is not correct in many cases. Give this parameter manually\n')
    MolFile.write('\n')

    # write mass and LJ parameters
    MolFile.write('Molecular Mass in amu: %f \n'%Mol.Mass)
    MolFile.write('LJ sigma in Angstrom: %f \n'%Mol.LJsigma)
    MolFile.write('LJ epsilon in Kelvin: %f \n'%Mol.LJepsilon)
    MolFile.write('\n')
    
    # rotational constants
    MolFile.write('Rotational Constants \n')
    MolFile.write('GHz       :')
    for i in Mol.RotCon: MolFile.write('%15.8f'%i)
    MolFile.write('     AdRot = %15.8f, KRot = %15.8f'%(Mol.AdRot,Mol.KRot))
    MolFile.write('\n')
    MolFile.write('cm-1      :')
    for i in Mol.RotCon: MolFile.write('%15.8f'%UnitConvert.EnergyConvert(InE=i,InUnit='GHz',OutUnit='cm-1'))
    MolFile.write('     AdRot = %15.8f, KRot = %15.8f'%(UnitConvert.EnergyConvert(InE=Mol.AdRot,InUnit='GHz',OutUnit='cm-1'),UnitConvert.EnergyConvert(InE=Mol.KRot,InUnit='GHz',OutUnit='cm-1')))
    MolFile.write('\n')
    MolFile.write('amuA2     :')
    for i in Mol.RotCon: MolFile.write('%15.8f'%UnitConvert.RotConConvert(InRC=i,InUnit='GHz',OutUnit='amuA2'))
    if len(Mol.RotCon) == 1:
        MolFile.write('     AdRot = %15.8f'%UnitConvert.RotConConvert(InRC=Mol.AdRot,InUnit='GHz',OutUnit='amuA2'))
    else:
        MolFile.write('     AdRot = %15.8f, KRot = %15.8f'%(UnitConvert.RotConConvert(InRC=Mol.AdRot,InUnit='GHz',OutUnit='amuA2'),UnitConvert.RotConConvert(InRC=Mol.KRot,InUnit='GHz',OutUnit='amuA2')))
    MolFile.write('\n')
    MolFile.write('\n')

    # energies
    EneConList = ['Har','kcalmol','kJmol','eV','cm-1','GHz','K']
    MolFile.write('Energies read from Gaussian .log or .out file\n')
    MolFile.write('                            Hartree            kcal/mol              kJ/mol                  eV                cm-1                 GHz                   K\n')
    MolFile.write('Electro Energy :')
    for i in EneConList: MolFile.write('%20.6f'%UnitConvert.EnergyConvert(InE=Mol.EleEnergy,InUnit='Har',OutUnit=i))
    MolFile.write('\n')
    MolFile.write('ZP Energy      :')
    for i in EneConList: MolFile.write('%20.6f'%UnitConvert.EnergyConvert(InE=Mol.ZeroPointCorrectRead,InUnit='Har',OutUnit=i))
    MolFile.write('\n')
    MolFile.write('0 K enthalphy  :')
    for i in EneConList: MolFile.write('%20.6f'%UnitConvert.EnergyConvert(InE=Mol.ZPERead,InUnit='Har',OutUnit=i))
    MolFile.write('\n')
    MolFile.write('ZP Energy scale:')
    for i in EneConList: MolFile.write('%20.6f'%UnitConvert.EnergyConvert(InE=Mol.ZeroPointCorrectRead*Mol.ScaleFactor,InUnit='Har',OutUnit=i))
    MolFile.write('\n')
    MolFile.write('0 K H(0K) scale:')
    for i in EneConList: MolFile.write('%20.6f'%UnitConvert.EnergyConvert(InE=(Mol.EleEnergy+Mol.ZeroPointCorrectRead*Mol.ScaleFactor),InUnit='Har',OutUnit=i))
    MolFile.write('\n')
    MolFile.write('\n')

    # harmonic frequencies
    MolFile.write('Harmonic Frequencies in cm-1: \n')
    MolFile.write('There are %d normal modes in total\n'%len(Mol.Freq))
    MolFile.write('UnScaled Freq: ')
    for i in Mol.Freq: MolFile.write('%10.4f'%UnitConvert.EnergyConvert(InE=i,InUnit='K',OutUnit='cm-1'))
    MolFile.write('\nScaled Freq  : ')
    for i in Mol.Freq: MolFile.write('%10.4f'%UnitConvert.EnergyConvert(InE=i*Mol.ScaleFactor,InUnit='K',OutUnit='cm-1'))
    MolFile.write('\n')
    MolFile.write('Calculated UnScaled Zero Point Energy in kcal/mol: %10.4f'%UnitConvert.EnergyConvert(InE=sum(Mol.Freq)/2,InUnit='K',OutUnit='kcalmol'))
    MolFile.write('\n')
    MolFile.write('Calculated   Scaled Zero Point Energy in kcal/mol: %10.4f'%UnitConvert.EnergyConvert(InE=sum(Mol.Freq)*Mol.ScaleFactor/2,InUnit='K',OutUnit='kcalmol'))
    MolFile.write('\n')
    if Mol.CalcType == 'Saddle Point': MolFile.write('Imaginary frequency: %10.4f \n'%Mol.ImagFreq)
    MolFile.write('\n')

    # coordinate
    MolFile.write('Coordinate of %s: \n'%Mol.MolName)
    for i in range(len(Mol.Coordinate)): MolFile.write('%s %10.6f %10.6f %10.6f\n'%(ToElement(Mol.Coordinate[i][1]),Mol.Coordinate[i][3],Mol.Coordinate[i][4],Mol.Coordinate[i][5]))
       
    # close file
    MolFile.close()
    
#########################End##########################


if __name__ == '__main__':
    IM2 = DataClass.MoleculeClass(os.path.normpath(os.getcwd()+'/Gaussian'),'IM2')
    IM2.ReadGaussian(0)
    WriteMolintoFile(IM2)
    WriteJmol(IM2)
    WriteSupInfoLaTeX(IM2)
