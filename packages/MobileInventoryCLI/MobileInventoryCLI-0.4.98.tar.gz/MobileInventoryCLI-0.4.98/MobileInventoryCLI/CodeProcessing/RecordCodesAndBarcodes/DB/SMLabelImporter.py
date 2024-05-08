from bs4 import BeautifulSoup as bs
import sys
from barcode import UPCA
from upcean import convert
import csv
from pathlib import Path

from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.Prompt import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.db import *

def ScrapeLocalSmartLabelList(engine=None):
    def mkPath(text,self):
        print(text)
        try:
            p=Path(text)
            if p.exists() and p.is_file():
                return p
            else:
                return
        except Exception as e:
            print(e)

    filename=Prompt.__init2__(None,func=mkPath,ptext="Smartlabel file",helpText="from right-click save-page-as in chrome/firefox",data={})
    if filename in [None,]:
        return

    with open(filename,"r") as file,open("export.csv","w") as exported:
        writer=csv.writer(exported,delimiter=';')
        html=''
        html=file.read()
        soup=bs(html)
        tables=soup.find_all('table')
        csvd=[]
        csvd.append(['Barcode','Code','Name','ALT_Barcode'])
        for r in tables:
            links=r.find_all('a')
            for link in links:
                name,upc=link.text,str(link['href'].split('/')[-1])[2:]
                if name != '':
                    if upc != '':
                        try:
                            if len(upc) > 8:
                                upca=UPCA(upc)
                                upce=convert.convert_barcode_from_upca_to_upce(upc)
                            else:
                                upce=upc
                                upca=convert.convert_barcode_from_upce_to_upca(upc)
                            if upce == False:
                                upce=''
                            csvd.append([upca,'',name.replace('\n','$newline$').replace(';','$semicolon$'),upce])
                            print(name,upca,upce)
                        except Exception as e:
                            print(name,upc,e)
        if engine != None:
            with Session(engine) as session:
                for num,(upc,code,name,alt) in enumerate(csvd):
                    check=session.query(Entry).filter(Barcode==str(upc)).first()
                    if not check:
                        ne=Entry(Barcode=str(upc),Code=str(code),Name=name,ALT_Barcode=str(alt),Price=0,CaseCount=1)
                        session.add(ne)
                        if num % 30 == 0:
                            session.commit()
                session.commit()
                session.flush()


        writer.writerows(csvd)
        #print(links)
if __name__ == "__main__":
    ScrapeLocalSmartLabelList(engine=ENGINE)
