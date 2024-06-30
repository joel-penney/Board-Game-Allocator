#!/usr/bin/python3

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from vote import check_all, gen_classes, Game, Player

app = Flask(__name__)
app.config["SECRET_KEY"] = "stoppeeking"
app.config['host'] = '0.0.0.0'
socketio = SocketIO(app)

games_map = {}
all_data = {}
all_data['preferences'] = {}

@app.route('/', methods=["POST", "GET"])
def home():
	return render_template("home.html", games=games_map)

@socketio.on("nominate")
def nominate(game_data):
	# could stand to do an error check here
	games_map[game_data["name"]] = {"min":game_data["mini"], "max":game_data["maxi"]}
	print(games_map)
	# then emit a call to reload the voting table
	socketio.emit("refreshVoteOptions", games_map)

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

	all_data['games'] = list(games_map.keys())
	all_data['preferences'][name] = preferences
	socketio.emit("updateRoom", all_data)
	socketio.emit("solution", ["Calculating..."])
	try:
		assign()
	except Exception as e:
		print(e)
		socketio.emit("solution", "No solution found (error)")

# Generate solution and return string form to client for direct output
def assign():
	print("games_map")
	print(games_map)
	print("all_data")
	print(all_data)
	games, players = gen_classes(all_data, games_map)
	print("games")
	print(games)
	print("players")
	print(players)
	result = check_all(games, players)
	print("result")
	print(result)

	if result == None:
		socketio.emit("solution", "No solution found")
		return

	assignments = ""
	for assign_game in result.assignments:
		list_names = [assign_player.name for assign_player in result.assignments[assign_game]]
		assignments += assign_game.name + ": " + ", ".join(list_names) + "."

	print("assignments")
	print(assignments)
	socketio.emit("solution", assignments)

if __name__ == "__main__":
	socketio.run(app, host='0.0.0.0', debug=True)
