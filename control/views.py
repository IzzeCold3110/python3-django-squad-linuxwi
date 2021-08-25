from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import subprocess
from subprocess import Popen,PIPE
import json
import os

def test_file(request, filename:str, folder:str="/tmp"):
    server_status_ = test_server_running_UDP(27165)
    template = loader.get_template('control/index.html')
    result = False
    if os.path.isfile(os.path.join(folder, filename)) and server_status_["result"] is True:
        os.remove(os.path.join(folder, filename))
        result = True
    response_data = {
        "rslt": result
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json")



def test_server_running_UDP(port, test_string="SquadGame"):
    if not isinstance(port, int):
        return False
    p1 = Popen(["netstat","-anpu"], stdout=PIPE, stderr=PIPE)
    p2 = Popen(["grep", str(port)], stdin=p1.stdout, stdout=PIPE, stderr=PIPE)
    p1.stdout.close()

    output,err = p2.communicate()
    p2.stdout.close()
    b_result = test_string in output.decode()
    
    return {"result": b_result}

def start(request):
    template = loader.get_template('control/redirect.html')
    with subprocess.Popen(["screen", "-AmdS", "server_1", "/bin/bash", "startserver1.sh"], cwd="/home/steam_squad") as ps:
        out,err = ps.communicate()
        print(out)
        print(err)
    
    with open("/tmp/server_1-wi", "w") as f:
        f.write("")
        f.close()
        print("wrote")
        
    context = {"status": test_server_running_UDP(27165)["result"]}
    return HttpResponse(template.render(context, request))


def stop(request):
    with subprocess.Popen(["screen", "-ls"], cwd="/home/steam_squad", stderr=subprocess.PIPE, stdout=subprocess.PIPE) as p1:
        p2 = Popen(["grep", "server_1"], stdin=p1.stdout, stdout=PIPE, stderr=PIPE)
        p1.stdout.close()

        output,err = p2.communicate()
        p2.stdout.close()
        tmp = []
        for item in output.decode().split("\t"):
            if len(item) > 0:
                if "server_1" in item:
                    tmp.append(item)
        if len(tmp) > 0:
            if "." in tmp[0]:
                current_pid = int(tmp[0].split(".")[0])
                with subprocess.Popen(["kill", "-term", str(current_pid)], stderr=subprocess.PIPE, stdout=subprocess.PIPE) as ps:
                    out,err = ps.communicate()
                    
        print(err)

    template = loader.get_template('control/redirect.html')
    context = {"status": test_server_running_UDP(27165)["result"]}
    return HttpResponse(template.render(context, request))

def index(request):
    server_status_ = test_server_running_UDP(27165)
    template = loader.get_template('control/index.html')
    if os.path.isfile("/tmp/server_1-wi") and server_status_["result"] is True:
        os.remove("/tmp/server_1-wi")
        context = {"status": test_server_running_UDP(27165)["result"]}
    elif os.path.isfile("/tmp/server_1-wi") and not server_status_["result"] :
        context = {"status": "starting"}
    else:
        context = {"status": test_server_running_UDP(27165)["result"]}
    
    return HttpResponse(template.render(context, request))