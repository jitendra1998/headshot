# Headshot #
##### Table of Contents ##### 
##### INTRODUCTION #####
##### INSTALLATION #####
##### SAMPLE REQUEST  #####
##### END POINT #####
##### EXAMPLES #####
##### DEMONSTRATIO #####

## INTRODUCTION ##
This is a website whose API's can be used as a open source platform to connect it features with different sites. A person will be able to register as a user and login with register and login API. They will able to use the feature of question generator to generate the question based on the hints.  Using this we have implemented a poker game in which multiple users can join a game room and start a game. The game will give three hints to every player and will ask to bet call or fold amount. According to preference of user t takes action and then shows the correct answer to everyone and person who selects the correct answer wins all the money. Many innovative ideas can be made using this API;s.

### INSTALLATION ###   
1. Download the repository
Clone the base repository onto your desktop with git as follows:
$ git clone https://github.com/jitendra1998/headshot
2. Install necessary dependencies
The project has its base on Python tornado frame work. 
Make user you have python install in your computer. Refer this for more information https://wiki.python.org/moin/BeginnersGuide/Download.
(It is recommended to start a virtual environment before installing all dependencies.
Read further https://docs.python.org/3/tutorial/venv.html) 
Install necessary Python dependencies as follows:
$ pip install -r req.txt

//more steps

## SAMPLE REQUEST ##
//A sample request to call the api
## END POINT ##
1. ### UserLogin API ###

On successful login sets the username in cookie and fetches the user data and appends in user_session redis table and in case of incorrect email or password redirects it to the same webpage asking to provide information again.

Field Name | Description | Value Type | Mandatory|
---|---|---|---|
user_email |	Email of user registered with | String |YES
password |	Password belonging to that email |	String |Yes 

2.  ### USERSIGNUP API ###

On successful signup redirects to login page and adds the user data in the sql table ‘user’


Field Name | Description |	Value Type  |	Mandatory
---|---|---|---|
avatar	|Email of user registered with.	|String	|Yes
user_name	|Username of the User to be displayed(Must be Unique)	|String	|Yes
user_email	|Email of user  	|String	|Yes
password	|Password for the account.	|String	|Yes
first_name	|First name of the User	|String	|NO
last_name	|Last name of the User	|String	|NO
d_o_b	|Date of birth of the User.	|Date	|NO
gender	|Gender of the User|	String	|NO
country	|Country at which the user belong.	|String	|NO


3. ### QUESTION GENERATE API ###

On successful request return a question and its correct answer all four options and its hint according to difficulty level.

Field Name	|Description	|Value Type	|Mandatory|
---|---|---|---|
Game_room_id  	|Id of current game room with users in it.	|Multiple INT|Yes |
theme	|Theme of the question to show.	|String	|Yes |

Sample Json response:- 

{
   "success": {
       "code": 200,
       "data": {
           "c_ans": [
               2
           ],
           "question": [
               "What continental football federation is Nigeria a member of?"
           ],
           "ans": [
               "CONMEBOL",
               "OFC",
               "CAF",
               "UEFA"
           ],
           "d2": [
               "Sports",
               "Football",
               "National Teams",
               "Nigeria"
           ],
           "d3": [
               null,
               null,
               null,
               null
           ],
           "d1": [
               "Sports",
               "Football",
               "Rules",
               "Governing Bodies"
           ]
       }
   }
}

4. ### Start_game ###

Start the game of all users connected in the game room.

Field Name	|Description	|Value Type	|Mandatory
---|---|---|---|
Game_room_id  |Id of current game room with users in it.	|Int	|Yes

5.  ### Bet ###

Increases the current bet according the amount.

Field Name	|Description|	Value Type|	Mandatory
---|---|---|---|
User_id	|Id of current User loged in.	|Int|	Yes
Game_room_id  |	Id of current game room with users in it.|	Int	|Yes
bet_amount	|Amount to bet 	|Int	|Yes

6. ### Call ###

Match the current amount of the bet made by a previous player in the round .

Field Name	|Description	|Value Type	|Mandatory
---|---|---|---|
User_id	|Id of current User loged in.|	Int	|Yes
Game_room_id  	|Id of current game room with users in it.	|Int	|Yes


7. ### All_in ###

Commits player entire stack(all money).

Field Name|	Description	 |Value Type	|Mandatory
---|---|---|---|
User_id	|Id of current User loged in.	|Int	  |Yes
Game_room_id  |	Id of current game room with users in it.|	Int	 |Yes

8. ### All_in ###

Ending participation in a hand. No more bets are required to go into the pot by someone once they fold.

Field Name	|Description	 |Value Type	|Mandatory
---|---|---|---|
User_id	|Id of current User loged in.	|Int	 |Yes
Game_room_id  	|Id of current game room with users in it.	 |Int	 | Yes

## EXAMPLES ###
Screen Shot and basic example
	
## DEMONSTRATION OF THE SITE ##

// video

