from http.client import HTTPSConnection 
from sys import stderr 
from json import dumps 
from time import sleep 
import random
import json

#Load Config
with open('./config.json') as f:
  data = json.load(f)
  for c in data['Config']:
        print('Loading...')
#Load Message
with open('./message.json') as f:
  data = json.load(f)
  message = data['Message'] #modify this in message.json

channelid = c['channelid'] #modify this in config.json
token = c['token'] #modify this in config.json
timer = c['timer'] #modify this in config.json
autodel = c['auto_delete'] #modify this in config.json
header_data = { 
	"content-type": "application/json", 
	"user-agent": "discordapp.com", 
	"authorization": token
} 
 
def get_connection(): 
	return HTTPSConnection("discordapp.com", 443) 
 
def del_message(conn, channel_id, message_id):
	try: 
		conn.request("DELETE", f"/api/v7/channels/{channel_id}/messages/{message_id}", headers = header_data) 
		resp = conn.getresponse() 
		 
		if 199 < resp.status < 300: 
			print("     - Deleted!")
			pass 
 
		else:
			stderr.write(f"HTTP {resp.status}: {resp.reason}\n")
			pass
 
	except: 
		stderr.write("Error\n")
 
def send_message(conn, channel_id, message_data): 
    ids = ''
    try: 
        conn.request("POST", f"/api/v7/channels/{channel_id}/messages", message_data, header_data) 
        resp = conn.getresponse() 
         
        if 199 < resp.status < 300: 
            print("     - Message Sent!")
            rs = json.loads(resp.read())
            ids = rs['id']
            pass 
 
        else: 
            stderr.write(f"HTTP {resp.status}: {resp.reason}\n") 
            pass 
 
    except: 
        stderr.write("Error\n")

    return ids
 
def main(): 
	message_data = { 
		"content": random.choice(message), 
		"tts": "false"
	} 
 
	idx = send_message(get_connection(), channelid, dumps(message_data))
	if (autodel == True):
		del_message(get_connection(), channelid, idx)
 
if __name__ == '__main__': 
	i = 1
	while True:    
		print(f"{i}| Start")
		main()
		print()
		sleep(timer) #How often the message will be sent (in seconds), every 1 hour = 3600
		i+=1
