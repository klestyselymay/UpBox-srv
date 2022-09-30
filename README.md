# UpBox-srv-1.0
UpBox-srv-1.0 is a server for UpBox-1.0

REQUIREMENTS: you need windows but i will release a linux verision.

python-3.10: https://www.python.org/downloads/release/python-3100/

UpBox-1.0: https://github.com/klestyselymay/UpBox-1.0

HOW TO INSTALL:

step 1: 
```
git clone https://github.com/klestyselymay/UpBox-srv-1.0.git
```

step 2:
```
cd UpBox-srv-1.0-windows
```

step 3:
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

now to use custom commands check the code below

```json
{
    "commands":
    [
        {
            "test": "echo hello from server",
            "command name": "command output"
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
