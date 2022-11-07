from xlwt import Workbook
import os.path
from os.path import basename, splitext
import glob

def generate_tokens(path):
    with open(path, 'r') as fp:
        buf = []
        while True:
            ch = fp.read(1)
            if ch == '':
                break
            elif ch.isspace():
                if buf:
                    yield ''.join(buf)
                    buf = []
            elif ch=='(':
                if buf:
                    yield ''.join(buf)
                    buf = []
            else:
                buf.append(ch)
                
def listdirectory(path): 
    fichier=[] 
    l = glob.glob(path+'\\*') 
    for i in l: 
        if os.path.isdir(i): fichier.extend(listdirectory(i)) 
        else: fichier.append(i) 
    return fichier

if __name__ == '__main__':
    m=1
    book = Workbook()
    feuil1 = book.add_sheet('feuille 1')
    feuil1.write(0,0,'Pixel')
    feuil1.write(0,1,'BlockX')
    feuil1.write(0,2,'BlockY')
    feuil1.write(0,3,'Temps Total')
    feuil1.write(0,4,'QBT')
    feuil1.write(0,5,'Supression des nodes')
    feuil1.write(0,6,'Merging')
    feuil1.write(0,7,'Compute')
    feuil1.write(0,8,'Mise à jour des QBT')
    for dossier in listdirectory(os.getcwd()):
        nom = splitext(basename(dossier))[0]
        test=nom[-8:]
        if test =="cProfile":
            pixel=''
            blockx=''
            blocky=''
            j=0
            while(nom[j]!='_'):
                pixel=pixel+nom[j]
                j+=1
            j+=1
            while(nom[j]!='_'):
                blockx=blockx+nom[j]
                j+=1
            j+=1
            while(nom[j]!='_'):
                blocky=blocky+nom[j]
                j+=1
            liste = []
            for token in generate_tokens(dossier):
                liste.append(token)      
            i=0
            k=3
            
            ligne1 = feuil1.row(m)
            ligne1.write(0,int(pixel))
            ligne1.write(1,int(blockx))
            ligne1.write(2,int(blocky))
            while (i<len(liste)):
                if liste[i] =="do_QBT)" or liste[i] =="refactoring)" or liste[i] =="merging)" or liste[i] =="compute)" or liste[i] =="update_tree)":
                    ligne1.write(k,float(liste[i-4]))
                    k+=1
                if liste[i] == "in":
                    ligne1.write(k,float(liste[i+1]))
                    k+=1
        
                i=i+1
            m+=1
    book.save('resultats.xls')