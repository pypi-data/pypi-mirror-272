# How To Install This Module

You can install this module using pip:

```commandline
pip install -U HusBot
```

# How To Use It

1. Import the `HClient` class from the module:

```python
from HusBot.TeleBuisness import HClient
```

2. Create a client for your business bot:

```python
Bot_Token = "123456:ABCDF" # Here Put Your Token Bot 
bot = HClient(Bot_Token)
```

3. Now you can use message handlers.

# Examples

- In this example, we used `message_handler` for new messages and we put `message=True` to make it fetch all the messages that arrive after it. You can do whatever you want with this message:

```python
@bot.message_handler(message=True)
def NewMessage(business_connection_id, chat_id, message,other):
    if message.startswith('hi'):
        print(True)
        bot.send_message(business_connection_id, chat_id, 'hi bro , how are you today')
    else:
    	print(False)
```

- If you need to handle a specific message in the message handler, you can put the `str` in the var `message`. For example:

```python
@bot.message_handler(message="Hello")
def NewMessage(business_connection_id, chat_id, message,other):
    bot.send_message(business_connection_id,chat_id,"hello")
```

- In this example, we used `edited_message` for new messages that were edited. Use this if you need to add a feature to know the modified messages:

```python
@bot.edited_message()
def NewEditedMessage(business_connection_id, chat_id, message,message_id,other):
    print(f"Message {message_id} was edited to {message}")
```

- In this example, we used `deleted_message` for new messages that were deleted. Use this if you need to add a feature to know the deleted messages:

```python
@bot.deleted_message()
def NewDeletedMessage(business_connection_id, chat_id, message_ids,other):
    print(f"Message {message_ids} Was Deleted.")
```

# In This Module

There are only important functions for sending messages in various formats, such as: Text, Photos, Video, Voice, Documents, Stickers. 

Examples:

```python
send_message(business_connection_id,chat_id,"hello")
send_document(business_connection_id,chat_id,'Document URL') # .zip And Other Extensions
send_photo(business_connection_id,chat_id,"Image URL") # .png , .jpg And Other Extensions
send_sticker(business_connection_id,chat_id, "ID Sticker")
send_video(business_connection_id,chat_id,"Video URL") # .mp4 And Other Extensions
```

# Notes

1. In the latest update to the Telegram bot API, they added a feature for inline buttons in their version (7.3). If you need to put a button in your message, you can use the function `send_message_button`. For example:

```python
bot.send_message_button(business_connection_id,chat_id,"hello", keyboard)
```

The `keyboard` is a variable in which the buttons are located. 

Examples for use:

```python
keyboard = {"inline_keyboard": [[{"text": '• Press Here •', "url": 'https://t.me/t_4_z'}]]}
```

This example shows how to add two buttons or more in the message, where each button is in a column:

```python
keyboard = {"inline_keyboard": [[{"text": '• Dev •', "url": 'https://t.me/t_4_z'},{"text": '• Dev •', "url": 'https://t.me/t_4_z'}]]}
```

This example shows how to add two buttons or more in the message, where each button is in a row:

```python
keyboard = {"inline_keyboard": [[{"text": '• Dev •', "url": 'https://t.me/t_4_z'}],[{"text": '• Dev •', "url": 'https://t.me/t_4_z'}]]}
```

# Finally, you must add the following code to run your bot:

```python
bot.RunHClient()
```

# Thanks for your use, my first module in my programming career.

# Dev: [Hussam Fawzi](https://t.me/t_4_z)
```

