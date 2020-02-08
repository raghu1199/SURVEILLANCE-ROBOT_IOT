import RPi.GPIO as gpio
from flask import Flask,render_template
import datetime
app=Flask(__name__)

sw=8
led1=10
led2=12
mtr1=18
mtr2=22
mtren=16

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)
gpio.setup(mtr1,gpio.OUT)
gpio.setup(mtr2,gpio.OUT)
gpio.setup(mtren,gpio.OUT)

gpio.setup(sw,gpio.IN)
gpio.setup(led1,gpio.OUT)
gpio.setup(led2,gpio.OUT)
gpio.output(mtren,gpio.LOW)
gpio.output(mtr1,gpio.LOW)
gpio.output(mtr2,gpio.LOW)

swsts=0
mtrsts="OFF "
led1sts=0
led2sts=0

def fwd_motor():
    gpio.output(mtr1,gpio.HIGH)
    gpio.output(mtr2,gpio.LOW)
    gpio.output(mtren,gpio.HIGH)

def rev_motor():
    gpio.output(mtr1,gpio.LOW)
    gpio.output(mtr2,gpio.HIGH)
    gpio.output(mtren,gpio.HIGH)
    
def stop_motor():
    gpio.output(mtren,gpio.LOW)
    gpio.output(mtr1,gpio.LOW)
    gpio.output(mtr2,gpio.LOW)


@app.route("/")
def index():
    mtrsts='off'
    swsts=gpio.input(sw)
    led1sts=gpio.input(led1)
    led2sts=gpio.input(led2)
    now = datetime.datetime.now()
    timeString=now.strftime('%Y-%m-%d %H:%M:%S')
    templateData={
            'mtrsts':mtrsts,
            'swsts':swsts,
            'led1':led1sts,
            'led2':led2sts,
            'time':timeString,
            'title':'RPIFUN',
            }
    return render_template("home.html",**templateData)

@app.route("/<device>/<action>")
def action(device,action):
    mtrsts='off'
    now=datetime.datetime.now()
    timeString=now.strftime('%Y-%m-%d %H:%M:%S')

    if device=='led1':
        actuator=led1
    if device=='led2':
        actuator=led2

    if action=='on':
        gpio.output(actuator,gpio.HIGH)
    if action=='off':
        gpio.output(actuator,gpio.LOW)

    if device=='mtr':
        if(action=='forward'):
            mtrsts='forward'
            fwd_motor()
        if(action=='reverse'):
            mtrsts='REVERSE'
            rev_motor()
        if(action=='stop'):
            mtrsts=='OFF'
            stop_motor()
    
    swsts=gpio.input(sw)
    led1sts=gpio.input(led1)
    led2sts=gpio.input(led2)

    templateData={
            'mtrsts':mtrsts,
            'swsts':swsts,
            'led1':led1sts,
            'led2':led2sts,
            'time':timeString,
         }
    return render_template("home.html",**templateData)


if __name__=="__main__":
    app.run()







