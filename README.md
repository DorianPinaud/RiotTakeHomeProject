# Riot Take-Home challenge
--------------------------

# Project statement

*Project's statement is defined here: [tryriot/take-home](https://github.com/tryriot/take-home)*

Additionnaly the user can choose which algorithm to use for encryption and decryption. For now, only two algorithms are implemented: base64 and hexadecimal (hex).

```bash
curl -X 'POST' \
  'http://localhost:8000/encrypt/?algo=hex' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-CSRFTOKEN: aqlI8ZMqqlA2nOx7SDTsxPs9Fj8JUhoswZW8R8yOSJH8tjGc6my0UW9wqlpE3kt1' \
  -d '{
  "additionalProp1": "string",
  "additionalProp2": "string",
  "additionalProp3": "string"
}'
```

## Test online version

The project is already deployed online, you can access it through this IP address: 
http://52.86.10.135:8000. Here the swagger interface to interact with it: http://52.86.10.135:8000/api/schema/swagger-ui/

> [!CAUTION]
> The rate limit by user ip address is of **60 request per second** otherwise you will received an 429 HTTP response.

## Test in your local environment

> [!IMPORTANT]
> Python 3.x.y should be installed

Here the different steps to install and run the project on a local debug environement (not suitable for production)

```powershell

git clone https://github.com/DorianPinaud/RiotTakeHomeProject.git

cd RiotTakeHomeProject

python -m venv ./env

# activate the python environment on windows powershell
.\env\Scripts\activate 
# activate the python environment on windows linux
./env/bin/activate

pip install -r requirements.txt

python manage.py runserver
```

You can then test the api through the Swagger interface with your browser.

> Here the Swagger link: localhost:8000/api/schema/swagger-ui/