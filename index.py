from flask import Flask, render_template, redirect, url_for, request
from vix import VixHost
import subprocess

app = Flask(__name__, template_folder='templates')

host = VixHost()
vm = host.open_vm(r'C:\Users\Raynold kennedy L\Documents\UKP\semester 6\Tekvir\CentOS.vmx')

@app.route("/", methods=["POST","GET"])
def home():
    return render_template("index.html")

@app.route("/poweron", methods=["POST","GET"])
def poweron():
    if request.method == "POST":
        vm.power_on(launch_gui=True)
        return render_template("poweron.html")
    else :
        return render_template("poweron.html")

@app.route("/poweroff", methods=["POST","GET"])
def poweroff():
    if request.method == "POST":
        vm.power_off(from_guest=False)
        return render_template("index.html")
    else :
        return render_template("index.html")

@app.route("/suspend", methods=["POST","GET"])
def suspend():
    if request.method == "POST":
        vm.suspend()
        return render_template("suspend.html")
    else :
        return render_template("suspend.html")

@app.route("/restart", methods=["POST","GET"])
def restart():
    if request.method == "POST":
        vm.reset(from_guest=False)
        return render_template("poweron.html")
    else :
        return render_template("poweron.html")

@app.route("/resume", methods=["POST","GET"])
def resume():
    if request.method == "POST":
        vm.power_on(launch_gui=True)
        return render_template("poweron.html")
    else :
        return render_template("poweron.html")

@app.route("/run_program", methods=["POST","GET"])
def run_script():
    vm.wait_for_tools(timeout=300)
    if request.method == "POST":
        vm.login('raynedys',"Raynedys061199",require_interactive=False)
        vm.proc_run('/usr/sbin/ifconfig','ens33 > /tmp/outfile',should_block=True)
        vm.copy_guest_to_host('/tmp/outfile','.//outfile')
        with open('outfile','r') as f:
            return render_template("program.html", text=f.read())
    else :
        return render_template("program.html")

# @app.route("/run_script", methods=["POST","GET"])
# def run_script():
#     vm.wait_for_tools(timeout=300)
#     if request.method == "POST":
#         vm.login('raynedys',"Raynedys061199",require_interactive=False)
#         return render_template("index.html")
#     else :
#         return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
    app.static_folder = "static"