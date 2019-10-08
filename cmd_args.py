import os
while(1):
    cmd = input("> ")
    if(cmd == "exit"):
        break
    out = os.popen(cmd).read()
    print(out)