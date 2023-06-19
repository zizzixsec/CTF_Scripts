import requests
 
def sendMessage(token, channel_id, message):
    url = 'https://discord.com/api/v8/channels/{}/messages'.format(channel_id)
    data = {"content": message}
    header = {"authorization": token}
 
    r = requests.post(url, data=data, headers=header)
    print(r.status_code)
 
 
def createDmChannel(token, user_id):
    data = {"recipient_id": user_id}
    headers = {"authorization": token}
 
    r = requests.post(f'https://discord.com/api/v9/users/@me/channels', json=data, headers=headers)
    print(r.status_code)
 
    channel_id = r.json()['id']
 
    return channel_id
 
if __name__=='__main__':
    with open('token.txt','r') as fh:
        data = fh.readline()
    token = data

    #Change these variables
    user_id = ''
    message = ''
    
    channel_id = createDmChannel(token, user_id)
    sendMessage(token, channel_id, message)