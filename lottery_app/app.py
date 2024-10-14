from flask import Flask, render_template, request, jsonify
from web3 import Web3
import json

app = Flask(__name__)

# Connect to Ganache
ganache_url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Contract ABI and Address
contract_address = ""  ####
with open('../build/contracts/Lottery.json') as f:
    contract_abi = json.load(f)['abi']

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enter', methods=['POST'])
def enter():
    account = request.form['account']
    name = request.form['name']
    players = contract.functions.getPlayers().call()
    if len(players) >= 3:
        return jsonify({"success": False, "message": "Lottery is full!"})
    tx_hash = contract.functions.enter(name).transact({'from': account, 'value': web3.to_wei(1, 'ether')})
    web3.eth.wait_for_transaction_receipt(tx_hash)
    return jsonify({"success": True, "message": f"{name} has been registered for the lottery!"})

@app.route('/get_players', methods=['GET'])
def get_players():
    players = contract.functions.getPlayers().call()
    return jsonify([{"address": player[0], "name": player[1]} for player in players])

@app.route('/pick_winner', methods=['POST'])
def pick_winner():
    account = request.form['account']
    tx_hash = contract.functions.pickWinner().transact({'from': account})
    web3.eth.wait_for_transaction_receipt(tx_hash)
    
    winner_addr, winner_name = contract.functions.getWinner().call()
    
    return jsonify({
        "success": True,
        "message": "Winner picked and prize transferred!",
        "winnerName": winner_name
    })

if __name__ == '__main__':
    app.run(debug=True)