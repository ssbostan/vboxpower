# VirtualBox Power Driver for MAAS (Metal as a Service)
# Copyright 2021 Saeid Bostandoust <ssbostan@linuxmail.org>

import logging
from flask import Flask, url_for
from virtualbox import VirtualBox, Session

# this is for configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

vbox = VirtualBox()

RESPONSES = {
    "running": {
        "status": "running"
    },
    "stopped": {
        "status": "stopped"
    },
    "unknown": {
        "status": "unknown"
    }
}

RUNNING_STATES = ["Starting", "FirstOnline", "Running", "LastOnline", "Paused"]
STOPPED_STATES = ["PoweredOff", "Saved", "Aborted"]

def check_machine_status(machine):
    status = "unknown"
    if str(machine.state) in RUNNING_STATES:
        status = "running"
    elif str(machine.state) in STOPPED_STATES:
        status = "stopped"
    logging.info(f"machine {machine.name} status check {status}")
    return status

def generate_machine_info(machine):
    info = {
        "name": machine.name,
        "status": check_machine_status(machine),
        "links": {
            "on": url_for("machine_power_on", machine_name=machine.name),
            "off": url_for("machine_power_off", machine_name=machine.name),
            "status": url_for("machine_power_status", machine_name=machine.name)
        }
    }
    logging.info(f"generated machine info {machine.name}")
    return info

@app.route("/")
def index():
    return {
        "machines": [generate_machine_info(m) for m in vbox.machines]
    }

@app.route("/<machine_name>/on", methods=["POST"])
def machine_power_on(machine_name):
    try:
        machine = vbox.find_machine(machine_name)
        logging.info(f"Machine {machine_name} found for power on request.")
    except:
        logging.error(f"Machine {machine_name} not found for power on request.")
        return RESPONSES["unknown"], 404
    if check_machine_status(machine) == "stopped":
        machine.launch_vm_process(Session(), "headless", [])
        return RESPONSES["running"], 202
    elif check_machine_status(machine) == "running":
        return RESPONSES["running"], 200
    else:
        return RESPONSES["unknown"], 500

@app.route("/<machine_name>/off", methods=["POST"])
def machine_power_off(machine_name):
    try:
        machine = vbox.find_machine(machine_name)
    except Exception as e:
        logging.error(f"error finding machine {machine_name}: {e}")
        return RESPONSES["unknown"], 404
    if check_machine_status(machine) == "running":
        session = machine.create_session()
        session.console.power_down()
        logging.info(f"machine {machine_name} powered off.")
        return RESPONSES["stopped"], 202
    elif check_machine_status(machine) == "stopped":
        logging.info(f"machine {machine_name} already stopped.")
        return RESPONSES["stopped"], 200
    else:
        logging.error(f"machine {machine_name} in an unknown state.")
        return RESPONSES["unknown"], 500

@app.route("/<machine_name>/status")
def machine_power_status(machine_name):
    try:
        machine = vbox.find_machine(machine_name)
    except Exception as e:
        logging.error(f"error finding machine {machine_name}: {e}")
        return RESPONSES["unknown"], 404
    if check_machine_status(machine) == "running":
        return RESPONSES["running"], 200
    elif check_machine_status(machine) == "stopped":
        return RESPONSES["stopped"], 200
    else:
        return RESPONSES["unknown"], 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5241")
