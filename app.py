from flask import Flask
app = Flask(__name__)
import json
import os

@app.route('/')
def config():
    pp = {
            "primaryColor": "#4527A0",
            
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
        
    return pp

# if __name__ == '__main__':
#    app.run(debug = True, port = os.getenv('PORT', '8000'), host = os.getenv('IP', '0.0.0.0'))