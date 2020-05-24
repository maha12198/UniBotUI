from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)

app.config[ 'SECRET_KEY' ] = 'jsbcfsbfjefebw237u3gdbdc'
socketio = SocketIO( app )

@app.route( '/', methods=['GET','POST'])
def hello():
  return render_template( './UniBot.html' )

def messageRecived():
  print( 'message was received!!!' )


@socketio.on( 'my eventes' )
def handle_my_custom_event1( json1 ):
  import model
  message = json1['message']
  answer=model.chat(message)
  json1['answer'] = answer
  json1['bot']='UniBot'
  print( 'recived my event: ' + str(json1 ))
  socketio.emit( 'my response', json1, callback=messageRecived )


if __name__ == '__main__':
  socketio.run( app, debug = True, use_reloader=False )
