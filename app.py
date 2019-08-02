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
            "expandPopularNBView": "true",
            "expandedWalletView": "false",
            "highlight": [
                {
                    "group": "others",
                    "onlyDisable": None,
                    "onlyEnable": [
                        "GOOGLEPAY",
                        "PAYTM"
                    ],
                    "po": "upi",
                    "visibility": "VISIBLE"
                },
                {
                    "group": "others",
                    "onlyDisable": None,
                    "onlyEnable": [
                        "FREECHARGE"
                    ],
                    "po": "wallets",
                    "visibility": "visible"
                }
            ],
            "highlightViewType": "grid",
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
            "paymentOptions": [
                {
                    "group": "others",
                    "onlyDisable": [
                        "GOOGLEPAY",
                        "PAYPAL",
                        "OLAPOSTPAID"
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
                    "po": "upi",
                    "visibility": "VISIBLE"
                },
                {
                    "group": "others",
                    "onlyDisable": [
                        "CREDIT",
                        "5500000000000004"
                    ],
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
            "primaryColor": "#2196F3",
            "primaryFont": "Radomir-Tinkov-Gilroy",
            "saved": {
                "otherSaved": "VISIBLE",
                "preffered": "VISIBLE",
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
            "toolbar": {
                "back": "VISIBLE",
                "pageTitle": "PaymentPageHosted"
            },
            "upiCollectWithGodel": "true"
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