from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
import json
import os
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)
db = SQLAlchemy(app)

pp = {
            "primaryColor": "#2196F3",
            
            "primaryFont": "Radomir-Tinkov-Gilroy",
            
            "modalView": "false",

            "toolbar": {
                        "back": "VISIBLE",
                        "pageTitle": "PaymentPageHosted"
                    },
            
            "screenTransition": {
                        "duration": "200",
                        "curve" : ["0.1", "0.4", "0.4", "0.9"]
                    },
            "popularBanks" : [],

            "upiCollectWithGodel" : "true",

            "highlight": [
                {
                    "group": "others",
                    "po": "upi",
                    "visibility": "VISIBLE",
                    "onlyEnable": ["GOOGLEPAY","PAYTM"],
                    "onlyDisable": None
                },
                {
                    "group": "others",
                    "po": "wallets",
                    "visibility": "visible",
                    "onlyEnable": ["FREECHARGE"],
                    "onlyDisable": None
                }
            ],

            "saved": {
                        "saved": "VISIBLE",
                        "preffered": "VISIBLE",
                        "otherSaved": "VISIBLE"
                    },
            
            "paymentOptions": [
                {
                    "group": "others",
                    "po": "wallets",
                    "visibility": "VISIBLE",
                    "onlyDisable": ["GOOGLEPAY","PAYPAL","OLAPOSTPAID"]
                },
                {
                    "group": "others",
                    "po": "nb",
                    "visibility": "VISIBLE",
                    "onlyDisable" : ["NB_DUMMY", "NB_SBM", "NB_SBT", "NB_CANR"]
                },
                {
                    "group": "others",
                    "po": "upi",
                    "visibility": "VISIBLE"
                },
                {
                    "group": "others",
                    "po": "cards",
                    "visibility": "VISIBLE",
                    "onlyDisable": ["CREDIT","5500000000000004"]
                }
            ],

            "moreOption" : {
                    "visibility" : "gone",
                    "icon"  : "wallet_icon",
                    "name"  :   "WalletFlow",
                    "view"  : {
                        "toolbar" : {
                            "back": "VISIBLE",
                            "pageTitle": "MoreOptionTitle"
                        },
                    "content"   : "editText",
                    "footer"    : "button",
                    "action"    : "payWithWallet"
                    }          
        }

        }

class PPConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    config = db.Column(db.JSON)

    def __init__(self, config):
        self.config = config


@app.route('/update', methods = ['POST'])
def update():
    # conn = sqlite3.connect('HyperWidgetPPConfig.db')
    pp = request.form['json']
    try:
        a = json.loads(pp)
        conf = PPConfig.query.get(1)
        conf.config = pp
        db.session.commit()
        # conn.execute("UPDATE PPConfig SET Config = ?", [pp])
        # conn.commit()
        # conn.close()
        flash("JSON Inserted")
    except:
        flash("INVALID JSON")
    return redirect(url_for('edit'))


@app.route('/edit')
def edit():
    conf = PPConfig.query.get(1)
    pp = conf.config
    # conn = sqlite3.connect('HyperWidgetPPConfig.db')
    # cursor = conn.execute('SELECT Config FROM PPConfig')
    # for row in cursor:
    #     pp = row[0]
    a = json.loads(pp)
    x = json.dumps(a, indent = 4, sort_keys=True)
    return render_template('display.html', jsonpp = x)

@app.route('/')
def config():
    conf = PPConfig.query.get(1)
    pp = conf.config
    return pp
    # conn = sqlite3.connect('HyperWidgetPPConfig.db')
    # cursor = conn.execute('SELECT Config FROM PPConfig')
    # for row in cursor:
    #     pp = row[0]
    # return pp

@app.route('/default')
def insert():
    conf = PPConfig.query.get(1)
    if conf is not None:
        conf.config = pp
    else:
        db.session.add(pp)
    db.session.commit()
    # conn = sqlite3.connect('HyperWidgetPPConfig.db')
    # cursor = conn.execute('SELECT Config FROM PPConfig')
    # conn.execute("UPDATE PPConfig SET Config = ?", [json.dumps(pp)])
    # conn.commit()
    # conn.close()
    return "Default Inserted"

if __name__ == '__main__':
    app.run(debug = True, port = os.getenv('PORT', '8000'), host = os.getenv('IP', '0.0.0.0'))