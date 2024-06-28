#!/usr/bin/python3

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from vote import check_all, gen_classes, Game, Player

app = Flask(__name__)
app.config["SECRET_KEY"] = "stoppeeking"
app.config['host'] = '0.0.0.0'
socketio = SocketIO(app)

games_map = {}
my_room = {}
my_room['preferences'] = {}

@app.route('/', methods=["POST", "GET"])
def home():
	#return render_template("home.html", games = list(games_map.keys()))
	return render_template("home.html", games=games_map)

@socketio.on("nominate")
def nominate(game_data):
	# could stand to do an error check here
	games_map[game_data["name"]] = {"min":game_data["mini"], "max":game_data["maxi"]}
	print(games_map)
	# then emit a call to reload the voting table
	socketio.emit("refresh", games_map)

# Save a list of votes and generate a solution
@socketio.on("vote")
def vote(vote_list):
	print(vote_list)
	preferences = {}
	votes = vote_list['votes']
	for game in votes:
		preferences[game] = int(votes[game])
	print(preferences)
	name = vote_list['name']

	my_room['games'] = list(games_map.keys())
	my_room['preferences'][name] = preferences
	socketio.emit("updateRoom", my_room)
	socketio.emit("solution", ["Calculating..."])
	try:
		assign()
	except Exception as e:
		print(e)
		socketio.emit("solution", ["no solution found"])
	# socketio.emit("refresh", games_map) # why was this here?

def assign():
	print("games_map")
	print(games_map)
	print("my_room")
	print(my_room)
	games, players = gen_classes(my_room, games_map)
	print("games")
	print(games)
	print("players")
	print(players)
	result = check_all(games, players)
	print("result")
	print(result)
	ret = dict.fromkeys([result.happiness_rating])
	string = ""
	for assign_game in result.assignments:
		if len(string) > 0:
			string += ". "
		string += assign_game.name + ": "
		for assign_player in result.assignments[assign_game]:
			string += assign_player.name + " "
	ret[result.happiness_rating] = string
	print("ret")
	print(ret)
	socketio.emit("solution", ret)

if __name__ == "__main__":
	socketio.run(app, host='0.0.0.0', debug=True)
