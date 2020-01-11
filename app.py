from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
import json
import os
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Super Secret App Key'
heroku = Heroku(app)
db = SQLAlchemy(app)


pp =    {
            "backgroundColor": "#F5F6F8",
            "checkboxSize": "16",
            "combineWallets": "false",
            "containerPadding": "16",
            "cornerRadius": "10.0",
            "cvvInputBoxType": "boxed",
            "expandPopularNBView": "true",
            "expandUpiView": "false",
            "expandedWalletView": "true",
            "fontColor": "#000000",
            "fontSize": "16",
            "gridFontSize": "14",
            "gridIconSize": "38",
            "headerSize": "18",
            "highlight": [],
            "highlightViewType": "list",
            "iconSize": "38",
            "lineSeparator": "true",
            "listItemHeight": "60",
            "modalView": "false",
            "moreOption": {
                "icon": "wallet_icon",
                "name": "WalletFlow",
                "view": {
                    "action": "payWithWallet",
                    "content": "editText",
                    "footer": "button",
                    "toolbar": {
                        "back": "VISIBLE",
                        "pageTitle": "MoreOptionTitle"
                    }
                },
                "visibility": "gone"
            },
            "offers": "gone",
            "paymentOptions": [
                {
                    "group": "others",
                    "po": "askAFriend",
                    "visibility": "gone"
                },
                {
                    "group": "others",
                    "onlyDisable": [
                        "GOOGLEPAY",
                        "PAYPAL",
                        "OLAPOSTPAID"
                    ],
                    "onlyEnable": [
                        "LAZYPAY",
                        "PAYTM",
                        "MOBIKWIK",
                        "FREECHARGE"
                    ],
                    "po": "wallets",
                    "visibility": "VISIBLE"
                },
                {
                    "group": "others",
                    "onlyDisable": [
                        "NB_DUMMY",
                        "NB_SBM",
                        "NB_SBT",
                        "NB_CANR"
                    ],
                    "po": "nb",
                    "visibility": "VISIBLE"
                },
                {
                    "group": "others",
                    "onlyDisable": [
                        "SHAREit",
                        "WhatsApp"
                    ],
                    "po": "upi",
                    "visibility": "visible"
                },
                {
                    "group": "others",
                    "onlyDisable": [],
                    "po": "cards",
                    "visibility": "VISIBLE"
                }
            ],
            "popularBanks": [
                "NB_AXIS",
                "NB_ICICI",
                "NB_SBI",
                "NB_HDFC"
            ],
            "primaryColor": "#28B3E3",
            "primaryFont": "Arial",
            "saved": {
                "otherSaved": "visible",
                "preffered": "visible",
                "saved": "VISIBLE"
            },
            "screenTransition": {
                "curve": [
                    "0.1",
                    "0.4",
                    "0.4",
                    "0.9"
                ],
                "duration": "200"
            },
            "spacing": "16",
            "toolbar": {
                "back": "VISIBLE",
                "pageTitle": "Payment Methods"
            },
            "toolbarColor": "#FBBA19",
            "upiCollectWithGodel": "false",
            "verifyMobile": "true"
        } 

class PPConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    config = db.Column(db.String(5000))

    def __init__(self, config):
        self.config = config


@app.route('/update', methods = ['POST'])
def update():
    pp = request.form['json']
    try:
        a = json.loads(pp)
        x = json.dumps(a)
    except:
        return "INVALID JSON"
    conf = PPConfig.query.get(1)
    conf.config = x
    db.session.commit()
    return redirect(url_for('edit'))


@app.route('/edit')
def edit():
    conf = PPConfig.query.get(1)
    pp = conf.config
    x = json.dumps(pp, indent = 4, sort_keys=True)
    return render_template('display.html', jsonpp = x)

@app.route('/')
def config():
    conf = PPConfig.query.get(1)
    pp = conf.config
    return pp

@app.route('/faq/prefetch')
def prefetchFAQ():
    return render_template('prefetch.html')

@app.route('/faq/signing')
def signingFAQ():
    return render_template('signature.html')

@app.route('/faq/initiate')
def initiateFAQ():
    return render_template('initiate.html')

@app.route('/faq/process')
def processFAQ():
    return render_template('process.html')

@app.route('/faq/terminate')
def terminateFAQ():
    return render_template('terminate.html')

@app.route('/faq/orderID')
def terminateFAQ():
    return render_template('orderID.html')

@app.route('/default')
def insert():
    conf = PPConfig.query.get(1)
    a = json.dumps(pp)
    if conf is not None:
        conf.config = a
    else:
        x = PPConfig(a)
        db.session.add(x)
    db.session.commit()
    return "Default Inserted"

if __name__ == '__main__':
    app.run(debug = True, port = os.getenv('PORT', '8000'), host = os.getenv('IP', '0.0.0.0'))