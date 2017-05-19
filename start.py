from flask import Flask,render_template, request, jsonify
from flask_socketio import SocketIO, send, emit
from operator import itemgetter
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.debug = True
socketio = SocketIO(app)



@app.route("/saavuda")
def hello():
	return render_template("dash.html")

#get method to start and stop
@app.route("/contro", methods=['GET'])
def contro():
	a = request.args.get('a', 0, type=int)
	if a==1:
		socketio.emit('my response', 'hello there')
	else:
		print "game shld stop here"
	return jsonify(result="done")


@app.route("/<plid>")
def plid(plid):
	#show the high score list from mongodb in descending order
	"""
	hihli = []
	for each in db.player.find():
		det = {}
		det['name'] = each['name']
		det['score'] = each['score']
		hihli.append(det)
	newlist = sorted(hihli, key=itemgetter('score'), reverse=True)
	"""

	return render_template("index.html",plid=plid)

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    try:
	    scroo = int(json['Score'])/40
	    json['Score'] = scroo
	    #insert into db
	    #check for existing player
	    """
	    sto = db.player.update({'name': json['Player']}, {'$set': {'score': scroo}})
	    #checking for the updatedExisting flag
	    if sto['updatedExisting'] == False:
	    	#this means this guy is a new player, so insert him/her
	    	db.player.insert({'name': json['Player'], 'score': scroo})
	    """
    except:
	    print 'not this guy'
    socketio.emit('results', str(json))


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0',port=5000)
