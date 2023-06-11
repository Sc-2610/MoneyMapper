from flask import Flask,request,jsonify
import requests

app = Flask(__name__)

@app.route('/',methods=['POST'])
def index():
    data = request.get_json()
    print(data)
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']

    print("Source Currency : ",source_currency)
    print("Target Currency : ",target_currency)
    cf = fetch_conversion_factor(source_currency,target_currency)
    print("CF : ",cf)
    final_amount = amount * cf
    final_amount = round(final_amount,2)
    response = {
        'fulfillmentText':"{} {} is {} {}".format(amount,source_currency,final_amount,target_currency[0])
    }
    return jsonify(response)

def fetch_conversion_factor(source,destination):

    #url = "http://api.exchangeratesapi.io/v1/convert?access_key=7c237b889dc5b6893fde268394af5066&from={}&to={}&amount={}".format(source,target,amount)
    url = "https://v6.exchangerate-api.com/v6/3a25e6f4f830252fbd3d3cde/latest/{}".format(source)
    response = requests.get(url)
    response = response.json()
    target = response['conversion_rates'][destination[0]]
    print("Response : ",response)
    print("Target : ",target)
    return target
