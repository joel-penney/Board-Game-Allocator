#!/usr/bin/python3

import itertools
import statistics
from typing import List

# classes include str/repr functions for debugging purposes

class Solution:
	def __init__(self):
		self.happiness_rating = 0
		self.assignments = dict()# dict of games to sets of players
	# Return tiebreaker rating value. Currently, spread the players out as much as possible (negative std. dev.)
	def get_tiebreaker_rating(self):
		return 0 - statistics.stdev([(len(players)) for game, players in self.assignments.items()])
	def __str__(self):
		return str(self.happiness_rating) + ": " + str(self.assignments)
	def __repr__(self):
		return str(self.happiness_rating) + ": " + str(self.assignments)

class Game:
	def __init__(self):
		self.name = "name"
		self.minPlayers = 0
		self.maxPlayers = 0
	def __str__(self):
		return "<name: " + self.name + ", minPlayers: " + str(self.minPlayers) + ", maxPlayers: " + str(self.maxPlayers) + ">"
	def __repr__(self):
		return "<name: " + self.name + ", minPlayers: " + str(self.minPlayers) + ", maxPlayers: " + str(self.maxPlayers) + ">"

class Player:
	def __init__(self):
		self.name = "name"
		self.prefs = dict()
	def __str__(self):
		return self.name + ":" + str(self.prefs)
	def __repr__(self):
		return self.name + ":" + str(self.prefs)

# Generate classes based on array input (from web version)
# to be replaced by proper organization; for dev version
def gen_classes(room_data, game_data):
	print(">>s")
	games = []
	for game_name in game_data:
		game = Game()
		game.name = game_name
		game.minPlayers = int(game_data[game_name]['min'])
		game.maxPlayers = int(game_data[game_name]['max'])
		games.append(game)
	print(">>g")
	players = []
	for player_name in room_data['preferences']:
		print("player_name")
		print(player_name)
		player = Player()
		player.name = player_name
		for pref_name in room_data['preferences'][player_name]:
			pref_name = pref_name.strip()
			print("pref_name")
			print(pref_name)
			pref_value = room_data['preferences'][player_name][pref_name]
			player.prefs[pref_name] = int(pref_value)
		players.append(player)
	print(">>p")
	return games, players

# Read in inpus from file and run calc method
def main():
	games = []
	with open("pref.txt", "r") as pref:
		# read in games
		while line := pref.readline().strip():
			if line == "*":
				break
			items = line.split(":")
			game = Game()
			game.name = items[0]
			game.minPlayers = int(items[1])
			game.maxPlayers = int(items[2])
			games.append(game)

		# read in preferences to players
		players = []
		while line := pref.readline().strip():
			items = line.split("|")
			player = Player()
			player.name = items[0]
			given_prefs = items[1].split(",")
			for game_rating in given_prefs:
				game_to_rating = game_rating.split(":")
				player.prefs[game_to_rating[0].strip()] = int(game_to_rating[1])
			players.append(player)

	# games, players: End file read for inputs; run and print
	result = check_all(games, players)

	pretty_print(result)

# Find best combination of games and players
def check_all(games: List[Game], players: List[Player]):
	#print(games)# get format for dev
	#print(players)# get format for dev
	# build all possible sets of games
	game_sets = []
	for i in range(len(games)):
		game_sets.extend([list(x) for x in itertools.combinations(games, i + 1)])
	
	# find the best solution for each game set and sort to find best outcome
	results = []
	for game_set in game_sets:
		result = find_happiest(game_set, players)
		if result != None:
			results.append(result)
	results.sort(key=lambda x: x.happiness_rating, reverse=True)
	if len(results) > 0:
		return results[0]
	else:
		return None

# For the given players and games, find the Solution of player/game
# combos with the highest happiness rating
def find_happiest(games, players):
	# base case: if we've filled out all games with no players left over,
	# we've reached a valid configuration and return an empty Solution to
	# begin building off of. If number of players remaining does not match
	# the number allowed, return none represting no valid solutions remaining.
	if len(games) == 0:
		if len(players) == 0:
			return Solution()
		else:
			return None
	min_needed = sum([game.minPlayers for game in games])
	max_allowed = sum([game.maxPlayers for game in games])
	if min_needed > len(players):
		return None
	if max_allowed < len(players):
		return None

	# ok here's the alg: for games/players given, check the first game with all sets of
	# players between size minPlayers and maxPlayers. Pass remaining games back into this
	# function for recursively finding the best allotment of the rest. Combine these two
	# halves and check their rating to compare for the highest rated overall solution
	game = games[0]
	best = None
	for i in range(game.minPlayers, game.maxPlayers + 1):
		# create all possible unique combinations of i players for the first game
		first_game_player_sets = list(itertools.combinations(players, i))
		for first_game_player_set in first_game_player_sets:
			# create possible solution for first game with given players
			first_game_soln = gen_solution(game, first_game_player_set) 
			# get all players not assigned to first game
			rest_players = [player for player in players if player not in first_game_player_set]
			# find the best solution for these remaining players and games
			rest_solns = find_happiest(games[1:], rest_players)
			if rest_solns == None:
				continue # no valid solution for rest of list; give up and try next possibility
			# merge halves into overall solution and compare against existing best solution
			to_test = merge_soln(first_game_soln, rest_solns)
			if best == None or to_test.happiness_rating > best.happiness_rating:
				best = to_test
			elif to_test.happiness_rating == best.happiness_rating:# tiebreaker selection
				# choose set made with fewer games
				if len(to_test.assignments) < len(best.assignments):
					best = to_test
				# choose set which does best on tiebreaker
				elif to_test.get_tiebreaker_rating() > best.get_tiebreaker_rating():
					best = to_test
				# else: they're pretty much equal so just stick with original 'best'

	return best

# Generate a new Solution for the given game and players
def gen_solution(game, players):
	soln = Solution()
	soln.assignments[game] = players
	soln.happiness_rating = sum([player.prefs[game.name] for player in players])
	return soln

# Merge the two solutions into one
def merge_soln(soln1, soln2):
	soln = Solution()
	soln.assignments = {**soln1.assignments, **soln2.assignments}
	soln.happiness_rating = soln1.happiness_rating + soln2.happiness_rating
	return soln

# What it says on the tin
def pretty_print(soln):
	print(soln.happiness_rating)
	for game, players in soln.assignments.items():
		players = ", ".join([player.name for player in players])
		print(game.name + ": " + players)

if __name__ == "__main__":
	main()
