# Yaklient
![Docs](https://img.shields.io/badge/docs-latest-brightgreen.svg "Docs")
![License](https://img.shields.io/badge/license-MIT-blue.svg "License")
![PEP8](https://img.shields.io/badge/PEP8-100%25-brightgreen.svg "PEP8")

Yaklient is an intuitive Python library for interacting with Yik Yak's API.

![Logo](https://raw.githubusercontent.com/akashlevy/Yaklient/master/ext/yaklient-logo.png "Logo")

### Example Usage

```python
# Import client classes from Yaklient
from yaklient import *

# Specify location of University of Exeter on a map
exeter = Location(50.7365, -3.5344)

# Create user object at University of Exeter with given userid
user = User(exeter, "21C6CA60E3AA43C4B8C18B943394E111")

# Get yaks, iterate through them, and print them
for yak in user.get_yaks():
    print yak
```
    
### More things

View doc/index.html to see the class structure and how to use each class. Email me if you have any questions.

### Dependencies

- [Python 2.7](https://www.python.org/downloads/)
- [requests](https://github.com/kennethreitz/requests)
- [requests-oauthlib](https://github.com/requests/requests-oauthlib)

### Things you can and should do with this library:
- Do analytics on Yaks posted at any location in the world!
- Change your basecamp!
- Post/read Yaks anywhere in the world!
- Port this library to another programming language and make a Yik Yak clone!

### Things you could but shouldn't do with this library:
- Create a bunch of users (a Yakarmy) and take over Yik Yak (upvote your own Yaks to the top, downvote others' Yaks to oblivion, etc.)
- Spam Yik Yak
