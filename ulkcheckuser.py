import subprocess
import typing as t
from flask import Flask, jsonify
import argparse

app = Flask(__name__)



def get_user(username: str) -> t.Optional[str]:
    command = 'check %s 1' % username
    result = subprocess.getoutput(command)
    final = result.strip()
    return final


def cont_online(username: str) -> t.Optional[str]:
    command = 'check %s 2' % username
    result = subprocess.getoutput(command)
    final = result.strip()
    return final


def limiter_user(username: str) -> t.Optional[str]:
    command = 'check %s 3' % username
    result = subprocess.getoutput(command)
    final = result.strip()
    return final


def check_data(username: str) -> t.Optional[str]:
    command = 'check %s 4' % username
    result = subprocess.getoutput(command)
    final = result.strip()
    return final


def check_dias(username: str) -> t.Optional[str]:
    command = 'check %s 5' % username
    result = subprocess.getoutput(command)
    final = result.strip()
    return final


@app.route('/checkuser/<usuario>')
def check_user(usuario):
    try:
        username = get_user(usuario)
        user = get_user(username)
        if user == "Not exist":
            return jsonify({
                "usuario": user,
                "conectados": "Null",
                "expira_em": "Null",
                "dias_restantes": "Null",
                "limite": "Null"
            })
        else:
            return jsonify({
                "usuario": username,
                "conectados": cont_online(username),
                "expira_em": check_data(username),
                "dias_restantes": check_dias(username),
                "limite": limiter_user(username)
            })
    except Exception as e:
        return jsonify({'error': str(e)})



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-port', dest='port', type=int, help='Porta do checkuser')
    args = parser.parse_args()
    port = args.port if args.port else 5000
    
    app.run(host='0.0.0.0', port=port)