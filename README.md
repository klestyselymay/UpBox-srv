# UpBox-srv-1.0
UpBox-srv-1.0 is a server for UpBox-1.0

REQUIREMENTS: you need windows but i will release a linux verision.

python-3.10: https://www.python.org/downloads/release/python-3100/

HOW TO INSTALL:

step 1: 
```
git clone https://github.com/klestyselymay/UpBox-srv-1.0.git
```
step 2:
```
pip install -r requirements.txt
```

HOW TO USE:

on 
```
server.json
```
it should look like this

```json
{
    "commands":
    [
        {
            "test": "echo hello from server"
        }
    ],

    "colors":
    [
        {
            "color": "green"
        }
    ]
}
```
