from flask import Flask, request, redirect, make_response
from twilio.twiml.messaging_response import MessagingResponse
from twilio import twiml
from flask import jsonify
from queue.hotqueue import HotQueue
import shortuuid
import time
from messages.messages import acknowlegements
import datetime
import pdb

app = Flask(__name__)

QQ=HotQueue('smart_biogas_queue', max_queue_length=1000)

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    #pdb.set_trace()
    number = request.form['From']
    message_body = request.form['Body']
    cookie_value = shortuuid.uuid() + "%" + str(0)
    cookie = request.cookies.get('message_id',str(cookie_value))
    messagecount = int(cookie.split("%")[1])
    messagecount +=1
    cookie_id = cookie.split("%")[0]
    cookie_new = cookie_id +"%" + str(messagecount) #'SMe85bdd60793fa0711b2940c2dd7ef24a', 'SMe85bdd60793fa0711b2940c2dd7ef24a'

    message_id = shortuuid.uuid()
    time_now=time.time()
    message_type = keyword_check(message_body)
    #twml = twiml.Response()
    #twml.sms(acknowlegements["ack1"])
    #resp = make_response(str(twml))
    resp = MessagingResponse()
    resp.message(acknowlegements["ack1"])
    resp = make_response(str(resp))
    expires=datetime.datetime.utcnow() + datetime.timedelta(hours=4)
    QQ.put({"number":number, "message":message_body,"mode":"sms","msg_type":message_type,"message_id":message_id,"time":time_now,"cookie":cookie_id,"cookie_expires":expires,"message_count":messagecount-1})
    resp.set_cookie('message_id',value=str(cookie_new),expires=expires.strftime('%a, %d %b %Y %H:%M:%S GMT'))

    return resp

def keyword_check(body):
    body = body.decode('utf-8').lower()
    if any(x in body for x in ['sign up','sign','register','reg']): # sign up check
        message_type = 'signup'
    elif any(x in body for x in ['tech','technition','tec','tek']):
        message_type = 'signup_technition'
    elif len(body)==0: # if there is no message
        message_type ='empty'
    else:
        message_type = 'standard'

    return message_type


@app.route("/trigger/<string:biogas_id>", methods=['GET'])
def trigger_issue(biogas_id):
    error_detected="gas pressure low"
    #pdb.set_trace()
    message_id = shortuuid.uuid()
    time_now=time.time()
    QQ.put({"biogas_id":biogas_id, "message":error_detected,"type":"monitor","message_id":message_id,"time":time_now})

    return jsonify("Issue_triggered")

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=7053, debug=False)
