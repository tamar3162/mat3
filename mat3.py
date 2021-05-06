# -*- coding: utf-8 -*-
"""
Created on Sun May  2 17:50:51 2021

@author: proled
"""
import json #Import and read the file
path_chat = "C:/Users/proled/Desktop/python/WhatsApp.txt"
open_file_WhatsApp_chat = open(path_chat,mode='r',encoding='utf-8')
read_file_WhatsApp_chat = open_file_WhatsApp_chat.read()

lines_chat=read_file_WhatsApp_chat.split('\n')

#Filling in the dictionary and making the data anonymous-
def make_anonymous(line,contact,c_id): 
        dict_line=dict()
        flag="Null"
        dict_line['datetime']=line.split("-")[0]
        short_line=line[15:].split(":")
        if short_line[0] in contact:
            dict_line["id"]=contact.index(short_line[0])+1
        else:
            flag=short_line[0]
            dict_line["id"]=c_id
        dict_line['text']=short_line[1]
        return [dict_line,flag]

#Create a dictionary that contains all the key data on the file
def creat_metadata(line):
    info_line=dict()
    info_line["chat_name"]=line.split('"')[1]
    info_line["creation_date"]=line.split("-")[0]
    info_line["num_of_participants"]=0
    the_creator=line.find("נוצרה על ידי")+len("נוצרה על ידי")
    info_line["creator"]=line[the_creator:]
    return info_line

#Send a single line to functions to create a new file
contacts=[]
united_dict=dict()  
count_id=1
i=1
new_file=list()
for line in lines_chat:
    if "נוצרה על ידי" in line:
        metadata=creat_metadata(line)
    if(":" not in line):
       new_file[len(new_file)-1]["text"]=new_file[len(new_file)-1]["text"]+" "+line
    try:
        line.split("-")[1].split(":")
        new_line=make_anonymous(line,contacts,count_id)
        new_file.append(new_line[0])
        if new_line[1]!="Null":
            contacts.append(new_line[1])
            count_id=count_id+1
    except:
        continue

metadata["num_of_participants"]=len(contacts)
united_dict["messages"]=new_file
united_dict["metadata"]=metadata
print(united_dict)


#Convert a file created in the desired format
info=json.dumps(united_dict)
file_name=united_dict["metadata"]["chat_name"]+".txt"
finish_file=open(file_name, "w")
finish_file.write(info)
finish_file.close() 
open_file_WhatsApp_chat.close()


