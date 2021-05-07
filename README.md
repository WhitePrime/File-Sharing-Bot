#### File-sharing-Bot



Telegram Bot to store Posts and Documents and it can Access by Special Links.


#### Features
- Fully customisable.
- Customisable welcome messages.
- More than one Posts in One Link.
- Can be deployed on heroku directly.

### Setup

- Add the bot to channels with admin permission, and thats it!

##
### Installation
#### Deploy on Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/WhitePrime/File-Sharing-Bot)</br>


#### Deploy in your VPS
```
git clone https://github.com/WhitePrime/File-Sharing-Bot
cd File-Sharing-Bot
pip3 install -r requirements.txt
# <Create config.py appropriately>
python3 main.py
```
##

### Admin Commands

```
start -start the bot or get posts

batch -create link for more than one posts

```

### Variables

* `API_HASH` Your API Hash from my.telegram.org
* `API_ID` Your API ID from my.telegram.org
* `TG_BOT_TOKEN` Your bot token from @BotFather
* `OWNER_ID` Must enter Your Telegram Id
* `CHANNEL_ID` Your Channel ID eg:- -100xxxxxxxx
* `ADMINS` A space separated list of user_ids of Admins, they can only create links
* `START_MESSAGE ` Optional: start message of bot, use HTML parsemode format
  
   

### Credits

- Thanks To Dan For His Awsome [Libary](https://github.com/pyrogram/pyrogram)

### Licence
[![GNU GPLv3 Image](https://www.gnu.org/graphics/gplv3-127x51.png)](http://www.gnu.org/licenses/gpl-3.0.en.html)  
