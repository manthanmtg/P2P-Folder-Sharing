# -*- coding: utf-8 -*-
"""
Created on Mon Oct 7 14:12:37 2019

Run the program using: python3 NewServer.py

@author: Manthan B Y, Abhishek Patil, Adeesh
"""
import time
import os
from os import path
from mimetypes import MimeTypes
import urllib
from socket import *
from html_snips import *
from resp_header import get_header
from my_zipper import create_zip

home_dir = '/home/manthanby'
times = 0
serverPort = 12556          # serverPort for the server
serverAddr = ('', serverPort)
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(serverAddr)

response = bytes()      # reponse bytes object
serverSocket.listen(1)
prev_req_name = ''
prev_req_time = -1000   # previous request time to handle duplicate requests
while 1:
    print('The server lsitening at', serverPort)
    connectionSocket, addr = serverSocket.accept()
    data = connectionSocket.recv(1024).decode() # receiving the request data from the client
    if(data == ''):         # if the data received is empty don't proceed
        connectionSocket.close()
        continue
    req_name = (data.split('\n')[0]).split(' ')[1].strip()
    curr_req_time = time.time()
    if(req_name == prev_req_name and (curr_req_time - prev_req_time) < 2):   # if the request is duplicate don't proceed
        connectionSocket.close()
        continue
    prev_req_name = req_name
    prev_req_time = curr_req_time
    print("\n------------ Connection Accepted ----------------")    
    print('=== Request from ' + str(addr) + ' ===')
    print(data)
    
    resp_data = html_start
    print("*******" + req_name + "*********")
    if(req_name[-3:] == "get"):
        file_path = home_dir + req_name[:-3]
        print("file Path: ", file_path)
        mime = MimeTypes()
        mime_type = mime.guess_type(file_path)[0]
        if(mime_type == None):
            mime_type = 'text/plain'
        response = get_header(200, 'download', mime_type, os.path.getsize(file_path), req_name[1:-3]).encode()
        if(os.path.isdir(file_path)):
            create_zip(req_name[1:-3], file_path)
            data = ''
            with open(req_name[1:-3] + '.zip', "rb") as f:
                data = f.read()     # reading the file in the binary format
            zip_path = os.getcwd() + '/' + req_name[1:-3] + ".zip"
            mime_type = mime.guess_type(zip_path)[0]
            if(mime_type == None):
                mime_type = 'text/plain'
            response = get_header(200, 'download', mime_type, os.path.getsize(zip_path), req_name[1:-3] + ".zip").encode()
            response += data    # attaching the binary format of the text to the http response
            os.remove(zip_path)
            print(response)
        else:
            with open(file_path, "rb") as f:
                data = f.read()     # reading the file in the binary format
                response += data    # attaching the binary format of the text to the http response
            print(response)
        connectionSocket.send(response)
        connectionSocket.close()
        continue
    curr_req_name = home_dir + req_name
    if(os.path.isdir(curr_req_name)):
        resp_data += "<h1> Here are the list of files</h1> <br>"
        resp_data += "<ul>"
        for content in os.listdir(curr_req_name):
            curr_full_path = curr_req_name.rstrip('/') + '/' + content
            print(curr_full_path)
            if(os.path.isfile(curr_full_path)):
                resp_data += "<li>" + """<a href = "{}">""".format(curr_full_path.replace("/home/manthanby", "", 1)) +  content + """</a>""" + """ Download """ +  """<a href="{}get" target="_blank">""".format(curr_full_path.replace("/home/manthanby", "", 1)) + """GET</a>""" + "</li>"
            else:
                resp_data += "<li>" + """<a href = "{}">""".format(curr_full_path.replace("/home/manthanby", "", 1)) +  content + """</a>""" + """ Download """ +  """<a href="{}get" target="_blank">""".format(curr_full_path.replace("/home/manthanby", "", 1)) + """GET</a>""" + "</li>"
        resp_data += "</ul>"        
    
    
    resp_data += html_end
    response = get_header(200).encode() + bytes(resp_data, 'utf-8')
    connectionSocket.send(response)
    print('=== Response ===')
    print(response)
    connectionSocket.close()
    times += 1
    print("\n------- " + str(times) + " ------ Connection Closed ----------------\n")
serverSocket.close()
