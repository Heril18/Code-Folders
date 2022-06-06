from tkinter import *
from tkinter import filedialog
from tkinter import ttk


from aiohttp import request
from pyparsing import htmlComment
import requests
from bs4 import BeautifulSoup
import urllib3
import csv
import os
import shutil



root = Tk ( )

root.iconbitmap("Code-folders.ico")
root.geometry ( "400x400" )
root.title ( "Code Folders" )
root.config ( bg = "lightblue" )
root.resizable ( False , False )

ext_name=['.cpp','.py','.c','.java','.php','.rust']

url_check=True
snippet_txt=open('s_loc.txt', 'w')
def bs_text():
    if(os.stat("s_loc.txt").st_size == 0):
        label1=Label(root, text="No Snippet has been added currently!!", font=("Courier 10 bold"))
        label1.pack()
        #return "No Snippet added !!"
    else:
        label2=Label(root, text="Snippet Exists!!", font=("Courier 10 bold"))
        label2.pack()
        #return "Update Snippet ?"
    return "Add/Update Snippet ?"

def snippet_loc():
    snippet_loc = filedialog.askopenfilename()
    for extension in ext_name:
        if snippet_loc.endswith(extension):
            with open('s_loc.txt', 'w') as f:
                    f.write(snippet_loc)
    if(os.stat("s_loc.txt").st_size != 0):
        label3=Label(root, text="Snippet has been Added/Updated!!", font=("Courier 10 bold"))
        label3.pack()

        



        
# FOLDER CREATER OVERALL start
def select_folder() :
    if url_check==True:
        folder_selected = filedialog.askdirectory()
        return folder_selected

def take_url():
    global entry
    string= entry.get()
    y = string.rfind("/")
    CF_link=string[0:y]
    CF_int =string[y+1:]
    if(CF_link=="https://codeforces.com/contest" and CF_int.isdigit()):  
        return string
    else:    
        label=Label(root, text="Invalid URL!!", font=("Courier 10 bold"))
        url_check=False
        label.pack()
        return False
        


def make_folder():

        url=take_url()
        if(url!=False):
            parent_dir=select_folder()
            x = url.rfind("/")
            name=url[x+1:len(url)]
            r=requests.get(url)
            htmlcontent=r.content

            soup=BeautifulSoup(htmlcontent,'html.parser')
            allanchortags=soup.find_all('a')

            folder_set=set()


            link_contest=url+"/problem/"
            for link in allanchortags:
                    link_text="https://codeforces.com" + link.get('href')
                    y = link_text.rfind("/")
                    if(link_text[0:y+1]==link_contest):
                        folder_set.add(link_text)
            path = os.path.join(parent_dir,name) 
            os.makedirs(path,exist_ok=True)
                
            parent_dir=parent_dir+'/' + name
            
            
            #folder_set contains link of all problems in the contest


            for xx in folder_set:
                y = xx.rfind("/")
                dirq =xx[y+1:]
                path = os.path.join(parent_dir, dirq) 
                os.makedirs(path,exist_ok=True)
                # print(path)

                if(os.stat("s_loc.txt").st_size > 0):
                    with open('s_loc.txt') as f:
                        source = f.read()
                        extension = os.path.splitext(source)[1]
                    file_name = dirq + extension
                    destination_file_make = open(path+'/'+file_name, 'w')    
                    destination=path+'/'+file_name
                    shutil.copy(source, destination) 
                else:
                    file_name = dirq + ".cpp"
                    destination_file_make = open(path+'/'+file_name, 'w')   


            label=Label(root, text="Folder has been made!", font=("Courier 10 bold"))
            label.pack()
# FOLDER CREATER OVERALL end


ttk.Button(root, text= "Select path and make Folders",width= 40, command=make_folder).pack(pady=20)
ttk.Button(root, text=bs_text() ,width= 40, command=snippet_loc).pack(pady=20)


entry= Entry(root, width= 40)
entry.focus_set()
entry.pack()



root.mainloop()


# TODO
#1. UI/UX poor, change ordering
#2. Icon missing
#3. Live update snippet button changes
