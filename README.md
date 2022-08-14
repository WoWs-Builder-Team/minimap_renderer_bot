## Minimap Renderer Bot

  

A Simple Discord bot wrapper for Minimap Renderer

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
```

  
 
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
