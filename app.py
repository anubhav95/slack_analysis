#import slack
from slackclient import SlackClient
import requests
from datetime import datetime

slack_token = 'xoxp-735167094370-747474593252-736502788627-c74aa250886772919ced51438b04484c'

slack_client = SlackClient(slack_token)
print(slack_client.api_call("api.test"))

print(slack_client.api_call("auth.test"))


def list_channels():
    channels_call = slack_client.api_call("channels.list")
    if channels_call.get('ok'):
        return channels_call['channels']
    return None


def get_msg_type(channel_name,channel_id):
    #data_type = requests.get("https://slack.com/api/channels.history?token="+slack_token+"&channel="+channel_id+"&pretty=1").json()
    data_type = requests.get("https://slack.com/api/channels.history?token=xoxp-735167094370-747474593252-736502788627-c74aa250886772919ced51438b04484c&channel="+channel_id+"&pretty=1").json()
    attachments = {}
    text_msg = []
    messages = {}
    date_match = {}
    final_list = []
    set1= set()
    u = []
    test = {}
    test2 = {}
    test3 = {}
    print("Channel name: "+channel_name)
    msg = data_type['messages']
    for i in msg:
        for j in i.keys():
            if type(i[j]) == list:
                y= (i[j][0]['filetype'])
                w =str(datetime.fromtimestamp((float(i['ts'])))).split()[0]
                u.append((y,w))

        if (i['text'] != ""):
            text = (i['text'])
            tms = str(datetime.fromtimestamp((float(i['ts'])))).split()[0]
            text_msg.append((text,tms))

    my_dict = {i: u.count(i) for i in u}

    for i in msg:
        dt = str(datetime.fromtimestamp((float(i['ts']))))
        timest= dt.split()[0]
        set1.add(timest)

    for i in set1:
        for j in my_dict.keys():
            if i == j[1]:
                if j[1] in attachments.keys():
                    attachments[i].append({j[0]: my_dict[j]})
                else:
                    attachments[i] = [{j[0]: my_dict[j]}]

        date_match[timest] = final_list

    for i in set1:
        for j in text_msg:
            if j[1]==i:
                if j[1] in messages.keys():
                    messages[j[1]].append(j[0])
                else:
                    messages[j[1]] = [j[0]]

    for i in set1:
        for j in u:
            if j[1]==i:
                if j[1] in test2.keys():
                    test2[j[1]].append(j[0])
                else:
                    test2[j[1]] = [j[0]]

    return messages, attachments



if __name__ == '__main__':
    channels = list_channels()
    if channels:
        print("Channels: ")
        for c in channels:
            messages,attachments = get_msg_type(c['name'],c['id'])
            print("Total Messages :",messages)
            print("Total attachments :", attachments)
            print("---------------------")
    else:
        print("Unable to authenticate.")








