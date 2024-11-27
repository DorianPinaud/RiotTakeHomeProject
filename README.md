# Riot Take-Home challenge
--------------------------

*Project's statement defined here: [tryriot/take-home](https://github.com/tryriot/take-home)*

## Core features summarize

Implementing an REST API exposing four endpoints:

### /Encrypt
encrypt every **value** of an object at the depth of **one**. Output result as **JSON**. 

> [!NOTE]
>  the input format is not speficied. By default we will first assume that only json is accepted.

> [!IMPORTANT] 
> Use base64 encryption algorithm by default, but the application should be able to handle other by design.

### **/decrypt** 

**Detects** encrypted string and decrypt them. return **JSON**.

> [!NOTE]
> The statement explicit a detection stage. If the string in input is not encrypted, send an error.

### /sign and /verify

Implement an **HMAC** signature and verification mecanism

## Additional features implemented

- Add a mecanism to select a different encryption algorithm. (new endpoints or add parameters in urls)
- Add a mecanism to select another cryptographic function for signature (new endpoints or add parameters in urls).

## Run Project

> [!IMPORTANT]
> Python 3.x.y should be installed

Install dependencies.

```powershell

python -m venv ./env

.\env\Scripts\activate # activate the python environment on windows powershell

pip install -r requirements.txt

```


## Going Live

### Rate limit