# AirBnb Console Project:
## First Step : The console
1. creat data model
2. manage (create, update, destroy, etc..) via the console
3. store and presist objects to (json file)
## description of the project
Serialization and deserialization are two important concepts in programming that allow objects to be easily stored, transmitted, and reconstructed. They’re used in various scenarios, such as storing objects in a database, sending objects over a network, or caching objects in memory
#### Files and Directory 

AirBnB_clone : the main reposotry for the project
	models : directory containt all classes and module files (object/instance)
		- base_model.py : file contain the base class of all our module
			* attributes : id , created_at , update_at
			* methods : save() , to_json()  
	test   : directory contain all unit test file 
	models/engine : diectory will contain all storage class  
		- file_storage.py (only one file for this project)
	
	= console.py >>> file the entry point of our comand interpreter

## description of the command interpreter: 

start console.py so you could manipilate with interpreter
#### What's a command interpreter?

Do you remember the Shell? It's exactly the same but limited to a specific use-case. In our case, we want to be able to manage the objects of our project:

    Create a new object (ex: a new User or a new City)
    Retrieve an object from a file
    Do operations on objects (create, destroy, all, etc...)
    Update attributes of an object

-- you could start your command interpreter in tow way 
1. interactive mode
guillaume@ubuntu:~/AirBnB$ python3 -m unittest discover tests

2. non-interactive mode:
guillaume@ubuntu:~/AirBnB$ echo "python3 -m unittest discover tests" | bash



