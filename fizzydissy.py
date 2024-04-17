import requests as req
import datetime
import re

TOKEN_REGEX = r"(mfa\.[\w-]{84}|[\w-]{24}\.[\w-]{6}\.[\w-]{27})"
BASE_URL = "https://discord.com/api/v10/"
suclist = (200,201,204) 

class Change:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": self.token
        }
    def globalName(self, new_username):
        url = f"{BASE_URL}users/@me"
        payload = {
            "global_name": new_username
        }
        r = req.patch(url, json=payload, headers=self.headers)
        if r.status_code == 200:
            return True
        return r.json()
    def username(self, username, password):
        url = f"{BASE_URL}users/@me"
        payload = {
            "username": username,
            "password": password
        }
        r = req.patch(url, json=payload, headers=self.headers)
        if r.status_code == 200:
            return True
        return r.json()
    def bio(self, new_bio):
        url = f"{BASE_URL}users/@me/profile"
        payload = {
            "bio": new_bio
        }
        r = req.patch(url, json=payload, headers=self.headers)
        if r.status_code == 200:
            return True
        return r.json()
    def theme(self, theme):
        url = f"{BASE_URL}users/@me/settings"
        payload = {
            "theme": theme
        }
        if theme not in ("light", "dark"):
            return {"message": "Invalid theme"}
        r = req.patch(url, json=payload, headers=self.headers)
        if r.status_code in suclist:
            return True
        return r.json()
    def avatar(self, new_avatar_link):
        url = f"{BASE_URL}users/@me"
        payload = {
            "avatar": new_avatar_link
        }
        r = req.patch(url, json=payload, headers=self.headers)
        if r.status_code == 200:
            return True
        return r.json()
    def banner(self, new_banner_link):
        url = f"{BASE_URL}users/@me/profile"
        payload = {
            "banner": new_banner_link
        }
        r = req.patch(url, json=payload, headers=self.headers)
        if r.status_code == 200:
            return True
        return r.json()

class Delete(Change):
    def __init__(self, token):
        super().__init__(token)
    def message(self, channelId, messageId):
        url = f"{BASE_URL}channels/{channelId}/messages/{messageId}"
        r = req.delete(url, headers=self.headers)
        if r.status_code in suclist:
            return True
        return r.json()
    def friend(self, userId):
        url = f"{BASE_URL}users/@me/relationships/{userId}"
        r = req.delete(url, headers=self.headers)
        if r.status_code in suclist:
            return True
        return r.json()
    def server(self, serverId):
        url = f"{BASE_URL}users/@me/guilds/{serverId}"
        r = req.delete(url, headers=self.headers)
        if r.status_code in suclist:
            return True
        return r.json()
    def channel(self, channelId):
        url = f"{BASE_URL}channels/{channelId}"
        r = req.delete(url, headers=self.headers)
        if r.status_code in suclist:
            return True
        return r.json()

class Get(Change):
    def __init__(self, token):
        super().__init__(token)

    def friends(self, FullJson=False) -> dict:
        url = f"{BASE_URL}users/@me/relationships"
        r = req.get(url, headers=self.headers)
        if r.status_code in suclist:
            if FullJson:
                return r.json()
            friends = {}#username, global_name
            for friend in r.json():
                friends[friend['user']['username']] = [friend['user']['global_name'], int(friend['user']['id'])]
            return friends
        else:
            return r.json()
    def messages(self, channel_id, limit: int = 1) -> dict:
        url = f"{BASE_URL}/channels/{channel_id}/messages?limit={limit}"
        r = req.get(url,headers=self.headers)
        if r.status_code in suclist:
            messages = {}
            for message in r.json():
                messages[message['id']] = (message['content'], message['author']['username'], message['timestamp'])
            return messages
        else:
            return r.json()
    
    def servers(self, FullJson=False):
        #Server ID : [Server Name, Permissions]
        url = f"{BASE_URL}users/@me/guilds"
        r = req.get(url, headers=self.headers)
        servers = {}
        if r.status_code in suclist:
            if FullJson:
                return r.json()
            for server in r.json():
                servers[int(server['id'])] = (server['name'], int(server['permissions']))
            return servers
        return r.json()
    
    def isNitro(self, FullJson=False):
        url = f"{BASE_URL}users/@me/billing/subscriptions"
        r = req.get(url, headers=self.headers)
        data = r.json()[0]
        nitro_end_date = datetime.datetime.fromisoformat(data['current_period_end'][:-6])
        if r.status_code in suclist:
            if FullJson:
                return data
            elif nitro_end_date < datetime.datetime.now() or not nitro_end_date:
                return False
            else:
                return True
        return r.json()

class Query(Get):
    def __init__(self, token):
        super().__init__(token)
    def friend(self, username_or_id) -> tuple:
        friends = self.friends()
        if not friends:
            return friends
        for username, dataList in friends.items():
            if username == username_or_id or int(dataList[1]) == username_or_id:
                return dataList
    def server(self, servername_or_id) -> tuple:
        servers = self.servers()
        if not servers:
            return servers
        for id, dataList in servers.items():
            if dataList[0] == servername_or_id or int(id) == servername_or_id:
                return dataList
            
    def message(self, channel_id, content_or_id, show_similar_content=False, search_limit=50) -> tuple:
        messages = self.messages(channel_id, search_limit)
        if not messages:
            return messages
        found_messages = []
        for id, dataList in messages.items():
            if show_similar_content:
                if str(content_or_id).lower() in str(dataList[0]).lower() or int(id) == content_or_id:
                    found_messages.append(dataList)
                else: continue
            elif str(dataList[0]).lower() == str(content_or_id).lower() or int(id) == content_or_id:
                found_messages.append(dataList)
        return tuple(found_messages)

class Add(Get):
    def __init__(self, token):
        super().__init__(token)

    def message(self, channel_id, content):
        url = f"{BASE_URL}/channels/{channel_id}/messages"
        payload = {
            "content": content
        }
        r = req.post(url, json=payload, headers=self.headers)
        if r.status_code in suclist:
            return True
        return r.json()
    
    def server(self, invite_code):
        url = BASE_URL + f"/invites/{invite_code}"
        r = req.post(url, headers=self.headers)
        if r.status_code in suclist:
            return True
        return r.json()

        
class FizzyDissy:
    sentMessages = {}
    deletedMessages = []
    def __init__(self, token):
        isValid = re.match(TOKEN_REGEX, token)
        if not isValid:
            raise Exception("Invalid token")
        self.token = token
        self.headers = {
            "Authorization": self.token
        }
        self.change = Change(token)
        self.get = Get(token)
        self.delete = Delete(token)
        self.query = Query(token)
        self.add = Add(token)
    
    def __str__(self) -> str:
        return self.token
