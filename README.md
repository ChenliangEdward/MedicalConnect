# MedicalConnect
This project aims to provide a platform for closer and more efficient communication and monitoring between patients and medical professionals. For example, medical professionals can monitor the measure from devices (sphygmomanometer, Thermometer) of patients. Patients can book appointments with registered professionals.

### Branch Strategy
- This repo is consisted with 3 branches: main, dev, test.
- **main**: The most stable and tested version, will only be updated when fully tested and is always functional. 
- **dev**: This branch will be used to update any minor changes and modifications in the process of development. When complete we will merge it to the test branch.
- **test**: This branch is used to test the product developed from the dev branch. When it is fully tested it will be merged to the main branch.  

### Implementation
- Service Logic : **Python Flask**
-  Server Container: **AWS EC2**
- Database: **SQLAlchemy** and **MongoDB**

### Database Design
Here is a brief description of the database design:
![Module vs DB](https://github.com/ChenliangEdward/PNGDump/blob/master/medicalconnect/DatabaseDesign.png?raw=true)
Here, the database for User, Device, Appointment Modules are located in SQLAlchemy and the Message module is locate on MongoDB server.

### Module APIs:
#### User :
- #### /api/users
- **GET**
	Give basic account information for the user.
	*Data required:* 
	```
	{
		"email" : string, 
		"password" : string
	}
	```
	*Data returned:*
	```
	{  
	  'id': Integer,  
	  'full_name':.String,  
	  'gender': String,  
	  'email': String,  
	  'password': String,  
	  'role': String  
	}
	```
	
- **PUT**
	Used for User registration and assign them into corresponding database models. 
	*Data required:* 
	```
	{
		"gender" : string, 
		"full_name" : string,
		"role": string,
		"email": string,
		"password": string
	}
	```
	Please note: the value for "role" is limited to only three options: [ patients, administrator, doctor ], the email is unique for every user.
	
	*Data returned:*
	```
	Status Code
	```
- #### /api/patients
- **GET**
	Give patient related information
	*Data required:* 
	```
	{
		"email": string,
		"password": string
	}
	```
	
	.
		*Data returned:*
	```
	{  
	  'patient_id': Integer,  
	  'weight':.String,  
	  'address': String,  
	  'email': String,  
	  'symptoms': String
	}
	```
- **Patch**
	Let user modify their information
		*Data required:* 
	```
	{
		"email": string,
		"password": string,
		"weight": float, (not required)
		"address": string, (not required)
		"symptoms": string, (not required)
		"dob": string (not required)
	}
	```
	.
		*Data returned:*
		
	```
	{  
	  'patient_id': Integer,  
	  'weight':.String,  
	  'address': String,  
	  'email': String,  
	  'symptoms': String
	}
	```
- #### /api/mps
- **GET**
	Give medical profession related information
	
	*Data required:* 
	```
	{
		"profession" : string, 
		"email": string
	}
	```
	*Data returned:*	
	```
	{  
	  'mp_id': Integer,  
	  'mp_email':.String,  
	  'mp_available': String,  
	  'mp_profession': String,  
	}
	```
	Please note that the mp_available is a string of Unix epoch integers divided by '-' and ','
- **Patch**
Modify identity data
		*Data required:* 
	```
	{
		"email": string,
		"password": string,
		'mp_available': String, (not required)
		'mp_profession': String (not required)
	}
	```
	*Data returned*
	```
		{  
		  'mp_id': Integer,  
		  'mp_email':.String,  
		  'mp_available': String,  
		  'mp_profession': String,  
		}
	```
#### Device:
- #### /api/devices
- **GET**
	Give the user's the measurements they have taken. 
	*Data required:* 
	```
	{
		"email": string,
		"password": string,
		"role":string
	}
	```
	*Data returned:*	
	```
	{  
	  'reading_id': Integer,  
	  'usage':.String,  
	  'serialNum': String,  
	  'assignedTo': String,  
	  "assignedBy", String
	  "add_date", integer
	}
	```
	Please note that the user needs to specify the role, if the role is 'patient' then the it will return the data of the measurements that is assigned to them. If the role is 'mp', then it will return the measurements that is assigned by them. 
- **PUT**
Modify identity data
		*Data required:* 
	```
	{  
	  'reading_id': Integer,  
	  'usage':.String,  
	  'serialNum': String,  
	  'assignedTo': String,  
	  "assignedBy", String
	  "add_date", integer
	}
	```
	*Data returned*
	```
	Status code
	```
	
#### Appointments:
- #### /api/appointments
- **GET**
	Give the user's the measurements they have taken. 
	*Data required:* 
	```
	{
		"email": string,
		"password": string,
	}
	```
	*Data returned:*	
	```
	{  
	  'email': Integer,  
	  'password':.String,  
	  'patient_email': String,  
	  'mp_email': String,  
	  "timeStart", String,
	  "timeEnd", integer,
	  'message': String,  
	}
	```
- **PUT**
Register an appointment with an MP
		*Data required:* 
	```
	{  
	  'email': Integer,  
	  'password':.String,  
	  'patient_email': String,  
	  'mp_email': String,  
	  "timeStart", String,
	  "timeEnd", integer,
	  'message': String,  
	}
	```
	*Data returned*
	```
	Status code
	```
	
#### Chat:
- ####  /api/messages
- **GET**
	Give the user's the messages they have sent or received. 
	*Data required:* 
	```
	{
		"email": string,
		"password": string,
	}
	```
	*Data returned:*	
	```
	json with dates and messages
	```
- **PUT**
Register an appointment with an MP
		*Data required:* 
	```
	{  
		"from":""
		"to": ""
		"Message":""
		"password":""
	}
	```
	*Data returned*
	```
	Status code
	```
### Module Logic
#### User
![User module logic](https://github.com/ChenliangEdward/PNGDump/blob/master/medicalconnect/Identity%20Module.png?raw=true)

#### Chat
![Chat module logic](https://github.com/ChenliangEdward/PNGDump/blob/master/medicalconnect/Chat%20Module.png?raw=true)
