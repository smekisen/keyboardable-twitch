import asyncio
from twitchAPI.oauth import refresh_access_token, revoke_token
from twitchAPI.helper import first
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope
import os
FILE = "tokens"
CLIENT_ID = str(os.environ["TWITCH_CLIENT_ID"])
CLIENT_ID2 = str(os.environ["TWITCH_CLIENT_ID2"])
CLIENT_SECRET = str(os.environ["TWITCH_CLIENT_SECRET"])
TARGET_SCOPE = [AuthScope.USER_READ_FOLLOWS]

async def authenticate(twitch):
        try:
            with open(FILE,"x+") as f:
                auth = UserAuthenticator(twitch,TARGET_SCOPE,force_verify=False)
                result = await (auth.authenticate()) 
                if type(result) == tuple:
                        token,refresh_token = result
                        f.write("{}\n{}".format(token,refresh_token))
                else:
                    return "0"
        except FileExistsError:
            with open(FILE,"r+") as f:
                try:
                    data = f.read().split(sep='\n')
                    token,refresh_token = data
                    await  (twitch.set_user_authentication(token,TARGET_SCOPE,refresh_token))
                    token = twitch.get_user_auth_token() 
                    f.seek(0)
                    f.write("{}\n{}".format(token,refresh_token))
                except:
                    auth = UserAuthenticator(twitch,TARGET_SCOPE,force_verify=False)
                    result = await (auth.authenticate()) 
                    if type(result) == tuple:
                            token,refresh_token = result
                            print(8)
                            print(token)
                            f.seek(0)
                            f.write("{}\n{}".format(token,refresh_token))
                    else:
                        return "0"
        return "1" 

async def get_streams_async(twitch):
        if twitch != "0":
            user = await first(twitch.get_users())
            if user != None:
                streams = twitch.get_followed_streams(user.id)
                stream_list = []
                async for stream in streams:
                    stream_list.append(stream)
                return stream_list
            else:
                return "0"
            
        else: 
            return "0"


class twitch_helper:
    def __init__(self):
        try: 
            twitch = Twitch(CLIENT_ID,CLIENT_SECRET)
        except TypeError:
            return("0")
        asyncio.run(authenticate(twitch))
        self.twitch = twitch
    def get_streams(self):
        if self.twitch.get_user_auth_token() == None:
            asyncio.run(authenticate(self.twitch))
        return asyncio.run(get_streams_async(self.twitch))
