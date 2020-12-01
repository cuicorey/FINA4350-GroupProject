from glob import glob
import re
import os
import win32com.client as win32
from win32com.client import constants
import docx
from tqdm import tqdm

def save_as_docx(path):
    # Opening MS Word
    try:
        word = win32.gencache.EnsureDispatch('Word.Application')
        doc = word.Documents.Open(path)
        doc.Activate ()

        # Rename path with .docx
        new_file_abs = os.path.abspath(path)
        new_file_abs = re.sub(r'\.\w+$', '.docx', new_file_abs)
        
        if os.path.exists(new_file_abs):
            pass
        
        else:
            # Save and Close
            word.ActiveDocument.SaveAs(
                new_file_abs, FileFormat=constants.wdFormatXMLDocument
            )
        doc.Close()
        print("finish ", new_file_abs)
    except:
        print('Error in ',path)
        
def convert_to_txt(file_path,txt_path):
    for file in os.listdir(file_path):
        try:
            if file.split('.')[1]=='docx':
                doc=docx.Document(file_path+"\\"+file)
                text = ""
                fullText = []
                for para in doc.paragraphs:
                    fullText.append(para.text)
                text='\n'.join(fullText)

                with open(txt_path+'\\'+'{}.txt'.format(file.split('.')[0]),'w',encoding="utf-8") as out:
                    out.write(text)
            else:
                continue
        except:
            pass

path='D:\\FINA4350\\'
industries=['Retailing',"Transportation","Automobiles and components","Consumer services","Healthcare"]

for industry in industries:
    if os.path.exists(path+industry):
        with tqdm (os.listdir(path+industry), desc = "convert docx to txt", ncols=80) as t:            
            for i in t:
                #if i not in finish:
                    file_path=path+industry+'\\'+ i
                    print(file_path)
                    doc_path= glob(file_path+"\\*.doc", recursive=True)
                    for file in doc_path:
                        save_as_docx(file)
                                                
                    if not os.path.exists(file_path+"\\"+'txt'):
                        os.makedirs(file_path+"\\"+'txt')
                    txt_path=file_path+"\\"+'txt'
                    convert_to_txt(file_path,txt_path)
        
        t.close()
        print("Finish the industry of ", industry)
