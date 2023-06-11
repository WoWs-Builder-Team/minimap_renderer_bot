## Minimap Renderer Bot

  

A Simple Discord bot wrapper for Minimap Renderer.

![enter image description here](https://github.com/WoWs-Builder-Team/minimap_renderer/blob/master/docs/minimap.gif?raw=true)

### Installation

  

1. Get Python 3.10 or higher

  

A virtual environment can be created with `python3.10 -m venv venv`.

  

2. Clone the repository

  

```
git clone https://github.com/WoWs-Builder-Team/minimap_renderer_bot.git
```

  

3. Install dependencies

  

```
cd minimap_renderer_bot
pip install git+https://github.com/WoWs-Builder-Team/minimap_renderer.git@develop
pip install -U -r requirements.txt
```

  

4. Create a `.env` file. **(Important)**

```
DISCORD_TOKEN=YOUR_DISCORD_BOT_TOKEN
REDIS_HOST=YOUR_REDIS_HOST
REDIS_PORT=YOUR_REDIS_PORT
REDIS_USERNAME=YOUR_REDIS_USERNAME
REDIS_PASSWORD=YOUR_REDIS_PASSWORD
COOLDOWN_TIMER=60
CD_EXEMPT_USERS='[""]'
```
`COOLDOWN_TIMER` can be changed to tweak the cooldown timer that each user must undergo in s, by default it's set to 60, you can lower it if you only have a few users 
or else raise it if you have many.
`CD_EXEMPT_USERS` can be modified to include the Discord User IDs of certain users, such that they bypass the cooldown timer entirely. Additional users can be added like so:
`CD_EXEMPT_USERS='["123456789012345678","876543210987654321"]'` assuming that `123456789012345678` and `876543210987654321` are the Discord User IDs of two people you want to be exempt. 
You can have as many as you like.
  
 
### Usage

  

To start the bot

```
main.py -r bot
```

To start the renderer worker

```
main.py -r worker
```

### License

 
This project is licensed under the GNU AGPLv3 License.

  

### Credits and Links

  

- This project is maintained by `@notyourfather#7816` and `@Trackpad#1234`.

- However, it would not have been possible without Monstrofil's [replays_unpack](https://github.com/Monstrofil/replays_unpack)!

- Another Discord bot wrapper is available [here](https://github.com/padtrack/track).
