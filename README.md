# Tunkgon-Discord-Bot
 Tunkgon Discord Bot Documentation

PLANNING
Implementing a Discord bot that works with API and Database
-League API
	-Implemented displaying player's information and In Game status
		-Cases:
			-Player has rank information
			-Player has no rank games availble
			-Player does not exist
   -If a player with their summoner name added to the database enters a game, the bot will annouce the a designated channel that the player is in game
-Youtube API (in progress)
	-Implemented playing youtube videos through voice chat in discord


ENVIRONMENTAL SETUP
-Server
	-Placed the python script in a Synology NAS where the script will be ran at with a bash sciript at 3:05 AM everyday after the server's daily reboot
	-Attempted using Virtual Environment (venv) on python to prevent installing python packages into the whole server
-League
	-Placed an application into Riot and obtained a developer's api key such that the bot is able to use riot's apis
-Discord
  -Created a personal server to use the bot
  
 OPERATION
  - $tunkgon - the bot sends a message saying hi
  - $add name - adds the summoner name to the database
  - $remove name - will remove the summoner from the list
  - $list - shows the list of summoners that are in the database
  - $summoner name - shows the stats of the player
  - $live - will send a message to the server stating whether the player is in game or not


