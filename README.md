# Intelligence Task Manager 


## Part 1 - Day 1 - The Data Base
------
### Project description
the `Intelligence Task Manager` manage agents and missions, and allow crate, update, and read data in organize way using MySql as the main data base.
------
### Folder Structure
```
intelligence-task-manager/
├── database/
│   ├── db_connection.py
│   ├── agent_db.py
│   └── mission_db.py
├── README.md
├── requirements.txt
└── .gitignore
```
----
### Tables Structure

our tables contain all the data we need to manage the `Intelligence Task Manager`, this is the fields we use in each table:

***Agents TABLE***
|field|type|
|-|-|
|id|INT PRIMARY KEY AUTO_INCREMENT|
|name|VARCHAR(50) NOT NULL|
|specialty|VARCHAR(100) NOT NULL|
|is_active|BOOLEAN DEFAULT TRUE|
|completed_missions|INT DEFAULT 0|
|failed_missions|INT DEFAULT 0|
|agent_rank|ENUM['Junior','Senior','Commander']|

***Missions TABLE***
|field|type|validation required |
|-|-|-|
|id|INT PRIMARY KEY AUTO_INCREMENT||
|title|VARCHAR(50) NOT NULL||
|description|TEXT NOT NULL||
|location|VARCHAR(255) NOT NULL||
|difficulty|INT  NOT NULL|must be <=10 and >=1|
|importance|INT  NOT NULL|must be <=10 and >=1|
|status|VARCHAR(50) DEFAULT 'NEW'|must be ['NEW','ASSIGNED','IN_PROGRESS', 'COMPLETED', 'FAILED','CANCELLED'] #note: I think it was better to use ENUM but I've followed the project instructions|
|risk_level|VARCHAR(50) NOT NULL|must be ['LOW','MEDIUM','HIGH','CRITICAL'] #note: I think it was better to use ENUM but I've followed the project instructions|
|assigned_agent_id|INT||

----
### Tables and Database Managers - `MissionDB` , `AgentDB`, `ConnectionDB`

those classes (each class in a file inside `database` folder) are managing the connection and taking with out data base.

***ConnectionDB***
this class manage the connection to the database and define tables and database

*class methods*
- __init__()
define all of the params that the class needs.
(connection details and tables and database details)
- get_connection()->mysql.connector
return a connection to the data bases
- create_database()-> None
create a database if not exists
- create_tables() -> None
create the tables if not exists yet

**AgentDB**
manage all of the action needed with the table `agents`

*note* this class DOES NOT responsible for Validation and Error handling 


*class methods*
- __init__()
define all of the fields needs for managing this class methods
(table name, connection function)

- create_agent(data:dict)->dict

create (save to database) an agent and return its object [its data dict as its in the data base] 

(*note* since we did NOT asked for represent the agents as class objects when we load from database, I assume that 'agent object' refer to the dict of data that we save and load from database)

- get_all_missions()->list[dict]

return all of the agents dicts 

- get_agent_by_id(id)->dict|None

return an agent dict by id, if not exists return None

- update_agent(id:int, data:dict)-> str

get id and a dict of keys and values to update and update the data (all data available to change except id).
return 'succeeded' if all went well and 'failed' if no change has happened (id not exists).
(# *note* its much better to return 'true' or 'false' because the end user does not call this function. I return string due the instructions and might change it in day 2 due the end-user platform)


- deactivate_agent(id:int)->str:

update agent status to False

return 'succeeded' if all went well and 'failed' if no change has happened (id not exists).
(# *note* its much better to return 'true' or 'false' because the end-user does not call this function. I return string due the instructions and might change it in day 2 due the end-user platform)


- increment_completed(id:int)->str:
update completed_missions =+ 1
return 'succeeded' if all went well and 'failed' if no change has happened (id not exists).
(# *note* its much better to return 'true' or 'false' because the end user does not call this function. I return string due the instructions and might change it in day 2 due the end-user platform)


- increment_failed(id:int)->str:
update failed_mission += 1
return 'succeeded' if all went well and 'failed' if no change has happened (id not exists).
(# *note* its much better to return 'true' or 'false' because the end user does not call this function. I return string due the instructions and might change it in day 2 due the end-user platform)


- get_agent_performance(id:int)->dict
return a dict with those key and values-
total: the agent total missions (***note*** a responsible problem, if we want to get all of the missions of an agent, we must connect with the table of `missions` , its better to do it a third class that response for buisness logic and can connect with the two classes or adding to the agent a field of `total_missions`)
failed: the failed missions
completed: the completed missions
success_rate: (completed/total) * 100 (***note*** logic problem, if we use total to calculate the all missions, even the ones the agent did not finish, we will treat them as 'failed', I'll follow the instructions, but it's better to calc (completed/(completed+failed)) * 100 )

- count_active_agents()->int
return the number of the active agents


**MissionDB**
manage all of the action needed with the table `missions`

*note* this class DOES NOT responsible for Validation and Error handling 


*class methods*
- __init__()
define all of the fields needs for managing this class methods
(table name, connection function)

- create_mission(data:dict)->dict:
gets a dict of keys and values for create an object, and create it (saves to data base).
return the new dict of data of the missions

- get_all_missions()->list[dict]
return list of the all missions dicts

- get_mission_by_id(id)->dict|None
return an mission dict by id, if not exists return None

- assign_mission(m_id, a_id)-str:
update the assigned_agent_id of m_id to a_id
return 'succeeded' if all went well and 'failed' if no change has happened (id not exists (m_id)).
(# *note* its much better to return 'true' or 'false' because the end-user does not call this function. I return string due the instructions and might change it in day 2 due the end-user platform)

- update_mission_status(id, status)->str:
update the mission status by id

update the assigned_agent_id of m_id to a_id
return 'succeeded' if all went well and 'failed' if no change has happened (id not exists).
(# *note* its much better to return 'true' or 'false' because the end-user does not call this function. I return string due the instructions and might change it in day 2 due the end-user platform)


- get_open_missions_by_agent(id)->list[dict]

return list of all of the missions dict that assign for agent id

- count_all_missions()-> int
return how many missions are

- count_by_status(status)->int
return how many mission with given status

- count_open_missions()-> int
return how many missions with 'NEW' / 'ASSIGNED' / 'IN_PROGRESS'

- count_critical_missions() -> int
return how many mission with risk_level  = 'critical'


-get_top_agent()->dict |None
return the agent with the max complicated missions.
note a :if there are  tow with same number, return the first
note b : if there are no mission that completed return None

### Business Logic (use for the end-user platform)
when ever a user want to crate or update a agent or a mission, the end-user platform must make *validations* to make sure the data is correct, otherwise, raise an error.

here are the ten rules:

1	rank חייב להיות Junior / Senior / Commander — כל ערך אחר זורק שגיאה.
2	difficulty ו-importance חייבים להיות בין 1 ל-10 — אחרת שגיאה.
3	risk_level מחושב אוטומטית בעת יצירת משימה — המשתמש לא שולח אותו.
4	סוכן עם is_active=False לא יכול לקבל משימות.
5	סוכן לא יכול להחזיק יותר מ-3 משימות פתוחות (ASSIGNED / IN_PROGRESS) במקביל.
6	אם risk_level=CRITICAL — רק סוכן בדרגת Commander יכול לקבל את המשימה.
7	ניתן לשייך רק משימה בסטטוס NEW. לאחר שיוך: status=ASSIGNED.
8	ניתן להתחיל רק משימה בסטטוס ASSIGNED. לאחר: status=IN_PROGRESS.
9	ניתן לסיים רק משימה. IN_PROGRESS  ולשנות לסטטוס failed or completed
10	ניתן לבטל רק משימה בסטטוס NEW או ASSIGNED — אחרת שגיאה.


note: in day onw we did not do the Business Logic.


### Additional Files 

to make sure everything works, I'll add some extra files.

- ***initialize.py***
this file makes sure to create the tables and database.
(*note*, when we will design the end-user platform, we will make this better and make suer to use it when a server is on)


### Run this Project

make sure you have on your computer those programs before run any command:
`docker` and `python 3.14` and `git`

***how to run this project**

**note** for *day one* we still did not make the end user platform, so you will
must to import and run the function yourself. 

**run those commands**

````
git clone https://github.com/ShlomoShoov/intelligence-task-manager
```

```
docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 
  -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0
```

```
docker start intelligence-mysql
```

***now, you can use the data base layer***

*simple example for agent db*

python file

```
import initializer
from database.agent_db import AgentDB

initializer.init()
agent_db = AgentDB()
print(agent_db.get_all_agents())

```


