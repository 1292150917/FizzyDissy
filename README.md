
# FizzyDissy Discord API library

## A very easy library for using Discord APIs.
###
<img align="right" width="229px" src="logo.png">
### Basic parameter

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `TOKEN` | `string` | **Necessary**. Your Discord bearer token. |

## Usage/Examples

```Python
import fizzydissy

TOKEN="<YOUR_TOKEN>"

api=FizzyDissy(TOKEN)
```

## All functions and their parameters

## Change Class Functions
```Python
api.change.<Function>
```
| Function |  Changes                |
| :--------| :------------------------- |
| `.globalName(new_username)` | Your global name. |
| `.username(username, password)` | Your username.(Isn't working!) |
| `.bio(new_bio)` | Your your bio. |
| `.theme(theme)` | Your discord theme. |
| `.avatar(new_avatar_link)` | Your avatar. |
| `.banner(new_banner_link)` | Your banner. |

## Delete Class Functions
```Python
api.delete.<Function>
```
| Function |  Delete                |
| :--------| :------------------------- |
| `.message(channelId, messageId)` |Message based on the information you sent. |
| `.friend(userId)` | Your friend(Dude, are you sure you want this ): ?). |
| `.server(serverId)` | Your discord server. |
| `.channel(channelId)` | Discord channel. |

## Get Class Functions
```Python
api.get.<Function>
```
| Function |  Description                |
| :--------| :------------------------- |
| `.friends(FullJson)` | Returns all friends in Discord. |
| `.messages(channel_id, limit)` |It returns the messages on the channel you write as much as the limit you give.|
| `.servers(FullJson)` | Returns all servers you have joined. |
| `.isNitro(FullJson)` | Returns whether nitro is present. |

**NOTE:** By making ```FullJson=True```, you can get the information from the API in raw form without simplifying it. This data will be much more detailed, but it can be a bit complicated to process.

## Query Class Functions
```Python
api.query.<Function>
```
| Function |  Query                |
| :--------| :------------------------- |
| `.friend(username_or_id)` |Queries a friend by name or id. |
| `.server(servername_or_id)` |Queries a server by name or id. |
| `.message(channel_id,content_or_id,show_similar_content=False,search_limit)`|Queries the message according to its content or id. You can customise your query with extra parameters.|

## Add Class Functions
```Python
api.add.<Function>
```
| Function |  Send/Add/Join             |
| :--------| :------------------------- |
| `.message(channel_id, content)` |It sends a message to the channel you specify.|
| `.server(invite_code)` | It will join the server where you typed the invitation code. (Isn't working!) |

# LOOK HERE
**NOTE:** Some functions may not work due to hCaptcha. But it will be fixed in the future.
