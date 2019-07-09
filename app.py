# _*_ coding:utf-8 _*_
#
# @Version : 1.0
# @Time    :    
# @Author  : SongZhiBin
from flask import Flask
from flask import request
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import render_template
import json

app = Flask(__name__)

member_dict = {}


@app.route('/chats/<username>')
def chats(username):
    return render_template('group_chat.html', username=username)


@app.route('/group_chat/<username>')
def group_chat(username):
    user_socket = request.environ.get('wsgi.websocket')  # 获得请求数据中我websocket链接
    member_dict[username] = user_socket
    while 1:
        try:
            mes = user_socket.receive()
            for member in member_dict:
                socket = member_dict.get(member)
                if socket != user_socket:
                    socket.send(username + ':' + mes)
        except Exception as e:
            member_dict.pop(username)


@app.route('/one_chats/<username>')
def one_chats(username):
    return render_template('one_chats.html', username=username)


@app.route('/one_to_one/<username>')
def one_to_one(username):
    user_socket = request.environ.get('wsgi.websocket')  # 获得请求数据中我websocket链接
    member_dict[username] = user_socket
    while 1:
        try:
            mes = user_socket.receive()
            data = json.loads(mes)
            to_socket = member_dict.get(data.get('to_user'))
            to_mes = data.get('mes')
            to_socket.send(username + ':' + to_mes)
        except Exception as e:
            print(e)
            member_dict.pop(username)


if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
