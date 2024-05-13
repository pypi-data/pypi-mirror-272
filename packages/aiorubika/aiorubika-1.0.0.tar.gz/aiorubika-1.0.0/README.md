# aiorubika

Python-based asynchronous framework for Rubika messenger API

## Install
```bash
pip install aiorubika
```


## Quik Start
```python
from aiorubika import Client, filters, utils

bot = Client(name='bot')
@bot.on_message_updates(filters.is_private)
async def updates(update):
    print(update)
    await update.reply(utils.Code('hello') + utils.Underline('from') + utils.Bold('aiorubika'))

bot.run()
```

