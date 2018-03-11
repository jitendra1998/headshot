# Headshot #

<img width="300" height="200" src="https://github.com/jitendra1998/headshot/blob/master/Head.png" alt="github api logo" />

##### Table of Contents ##### 

* [1. INTRODUCTION](#1-INTRODUCTION)
* [2. INSTALLATION](#2-INSTALLATION)
* [3. END POINT](#3-ENDPOINT)
* [4. SCREENSHOTS ](#4-SCREENSHOTS )

### 1 INT#RODUCTION ### 
Headshot is a collection of 5 independent APIs with easy to integrate RESTful architecture .
These APIs can be used as a open source platform to develope educational, fun and enganing games. A user will be able to register and login with Register and Login API. They will able to use the feature of question generator to generate the question and also hints.  Using this we have implemented a poker based quizzing game in which multiple users can join a game room and start a game.  Many such innovative ideas can be implemented using these API's.

### 2 INSTALLATION ###   
1. Download the repository
Clone the base repository onto your desktop with git as follows:
```ruby
$ git clone https://github.com/jitendra1998/headshot
```
2. Install necessary dependencies
The project has its base on Python tornado frame work. 
Make user you have python install in your computer. Refer this for more information click [here](https://wiki.python.org/moin/BeginnersGuide/Download).
(It is recommended to start a virtual environment before installing all dependencies,
[Read further](https://docs.python.org/3/tutorial/venv.html)	) 

Install necessary Python dependencies as follows:
```ruby
$ pip install -r req.txt
```
3. how to initialize the game

```ruby 
*install tornado, mqsql-server, redis-server
```

4. mysql setup 
```ruby
sudo apt-get update
sudo apt-get install mysql-server
```

5. mysql secure installation
```ruby
/usr/bin/mysql_secure_installation
```

6. start mysql
```ruby
/usr/bin/mysql -u root -p
```

7. create a database quizycash
```ruby
CREATE DATABASE quizycash;
USE quizycash;
```

8. create a user development with pass 12345
```ruby
CREATE USER 'development'@'localhost' IDENTIFIED BY '12345';
GRANT ALL PRIVILEGES ON * . * TO 'development'@'localhost';
```

9. install mysq-db
```ruby
$ sudo apt-get install python-pip python-dev libmysqlclient-dev
pip install MySQL-python
```

10. initialize the database schema
```ruby
/usr/bin/mysql -u development -p quizycash < database_schema.sql
```

11. insert game data (game data for 3 game rooms)
```ruby
INSERT INTO game_room (game_room_name, game_category, max_players, game_theme, min_buy_in, max_buy_in, game_status, created_at, big_blind, small_blind) VALUES ('game1', 'football', 10, 'sports', 20,80,1,'2017-08-03 15:36:45', 2, 1);

INSERT INTO game_room (game_room_name, game_category, max_players, game_theme, min_buy_in, max_buy_in, game_status, created_at, big_blind, small_blind) VALUES ('game2', 'football', 10, 'science', 250,1000,1,'2017-09-13 21:40:05', 40, 20);

INSERT INTO game_room (game_room_name, game_category, max_players, game_theme, min_buy_in, max_buy_in, game_status, created_at, big_blind, small_blind) VALUES ('game3', 'football', 10, 'economics', 100,500,1,'2017-09-20 08:19:32', 40, 20);
INSERT INTO game_room (game_room_name, game_category, max_players, game_theme, min_buy_in, max_buy_in, game_status, created_at, big_blind, small_blind) VALUES ('game4', 'football', 10, 'sports', 25,100,1,'2017-09-20 08:19:32', 4, 2);
```

12. redis-server setup
```ruby
sudo apt-get install redis-server
```

13. check redis by running reddis-cli on terminal
```ruby
redis-cli
```

14. flush redis
```ruby
redis-cli flushall
```

15. insert active_games data in redis (for that on a new terminal run python)
```ruby
import redis
import json
r = redis.StrictRedis(host='localhost', db=4)
r.set('active_games', json.dumps({'game1':'1'}))
```
16.  new redis active_games data 
```ruby
r.set('active_games', json.dumps({"game3": "3", "game2": "2", "game1": "1"}))
```


17. initial check
```ruby
r.get('active_players')
r.get('user_session')
r.get('active_games')
```
### For deployment change host in statrting of file ###
```ruby
admin_func.js - 1
game_room_api.py - 1
 ```

## 3 END POINT ##

### 1. UserLogin API ###

On successful login sets the username in cookie and fetches the user data and appends in user_session redis table and in case of incorrect email or password redirects it to the same webpage asking to provide information again.

Field Name | Description | Value Type | Mandatory|
---|---|---|---|
user_email |	Email of user registered with | String |YES
password |	Password belonging to that email |	String |Yes 

### 2. USERSIGNUP API ###

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


### 3. QUESTION GENERATE API ###

On successful request return a question and its correct answer all four options and its hint according to difficulty level.

Field Name	|Description	|Value Type	|Mandatory|
---|---|---|---|
Game_room_id  	|Id of current game room with users in it.	|Multiple INT|Yes |
theme	|Theme of the question to show.	|String	|Yes |

Sample Json response:- 

```javascript
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
```

### 4. Start_game ###

Start the game of all users connected in the game room.

Field Name	|Description	|Value Type	|Mandatory
---|---|---|---|
Game_room_id  |Id of current game room with users in it.	|Int	|Yes

### 5. Bet ###

Increases the current bet according the amount.

Field Name	|Description|	Value Type|	Mandatory
---|---|---|---|
User_id	|Id of current User loged in.	|Int|	Yes
Game_room_id  |	Id of current game room with users in it.|	Int	|Yes
bet_amount	|Amount to bet 	|Int	|Yes

### 6. Call ###

Match the current amount of the bet made by a previous player in the round .

Field Name	|Description	|Value Type	|Mandatory
---|---|---|---|
User_id	|Id of current User loged in.|	Int	|Yes
Game_room_id  	|Id of current game room with users in it.	|Int	|Yes


### 7. All_in ###

Commits player entire stack(all money).

Field Name|	Description	 |Value Type	|Mandatory
---|---|---|---|
User_id	|Id of current User loged in.	|Int	  |Yes
Game_room_id  |	Id of current game room with users in it.|	Int	 |Yes

### 8. Fold ###

Ending participation in a hand. No more bets are required to go into the pot by someone once they fold.

Field Name	|Description	 |Value Type	|Mandatory
---|---|---|---|
User_id	|Id of current User loged in.	|Int	 |Yes
Game_room_id  	|Id of current game room with users in it.	 |Int	 | Yes

## 4 SCREENSHOTS ###

<img src="https://github.com/jitendra1998/headshot/blob/master/screenshot/Screenshot%20from%202018-03-11%2010-32-56.png" alt="ss" />
<img src="https://github.com/jitendra1998/headshot/blob/master/screenshot/Screenshot%20from%202018-03-11%2010-33-22.png" alt="ss" />
<img src="https://github.com/jitendra1998/headshot/blob/master/screenshot/Screenshot%20from%202018-03-11%2010-33-59.png" alt="ss" />
<img src="https://github.com/jitendra1998/headshot/blob/master/screenshot/Screenshot%20from%202018-03-11%2012-13-48.png" alt="ss" />
<img src="https://github.com/jitendra1998/headshot/blob/master/screenshot/Screenshot%20from%202018-03-11%2012-13-58.png" alt="ss" />
<img src="https://github.com/jitendra1998/headshot/blob/master/screenshot/Screenshot%20from%202018-03-11%2010-33-59.png" alt="ss" />
<img src="https://github.com/jitendra1998/headshot/blob/master/screenshot/Screenshot%20from%202018-03-11%2010-34-13.png" alt="ss" />
<img src="https://github.com/jitendra1998/headshot/blob/master/screenshot/Screenshot%20from%202018-03-11%2012-14-10.png" alt="ss" />
