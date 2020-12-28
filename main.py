import ftplib
import xlrd
import os
import shutil
import pandas as pd
import sys
import pdb
from datetime import date
FTP_HOST = "talend.ecolotrans.net"
FTP_USER = "talend"
FTP_PASS = "Rand069845"
# connect to the FTP server
ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
# force UTF-8 encoding
ftp.encoding = "utf-8"

#nom_de_fichier = sys.argv[1]
#pdb.set_trace()
#print(nom_de_fichier)
ftp.cwd('/Preprod/IN/POC_ON_DEMAND/INPUT/ClientInput')

clients = ftp.nlst()
print(clients)
if not os.path.exists('ClientInput'):
    os.makedirs('ClientInput')
for client in clients:
    path_racine = '/Preprod/IN/POC_ON_DEMAND/INPUT/ClientInput'
    path_client = path_racine + '/' + client
    ftp.cwd(path_client)
    print("success")
    liste_fichier_client = ftp.nlst(path_client)
    print(liste_fichier_client)
    if(len(liste_fichier_client) != 0):
        if not os.path.exists("ClientInput/"+ client):
            os.makedirs("ClientInput/"+ client)
        for fichier in liste_fichier_client:
            file_name = fichier.split('/')[7]
            print(file_name)
            with open(file_name, "wb") as file:
                commande = "RETR " + file_name
                ftp.retrbinary(commande, file.write)
            shutil.copy2(file_name, "ClientInput/"+ client)
            os.remove(file_name)
            #shutil.move(file_name, "ClientInput/"+ client)
path_racine = 'ClientInput'
#filename_rech = nom_de_fichier + '_EDI.xlsx'
mergedData = pd.DataFrame()
for client in os.listdir(path_racine):
    path_client = path_racine + '/' + client
    for file in os.listdir(path_client):
        #if file == filename_rech:
        path_file = path_client + '/' + file
        print(path_file)
        data = pd.read_excel(path_file, index_col=None)
        mergedData = mergedData.append(data)
        print("ahmed")
print(mergedData)
liste_index= []
for i in range(len(mergedData.index)):
    liste_index.append(i)
mergedData.index = liste_index
print(mergedData)
if mergedData.empty == False:
    now = date.today()
    file_name = now.strftime('%d_%m_%y') + '_EDI.xlsx'
    mergedData.to_excel(file_name)
    ftp.cwd('/Preprod/IN/POC_ON_DEMAND/INPUT/TalendInput')
    print(file_name)
    with open (file_name, 'rb') as file:
        ftp.storbinary('STOR {}'.format(file_name), file)
    os.remove(file_name)
