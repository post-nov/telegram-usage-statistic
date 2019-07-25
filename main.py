import json
import os
import datetime

os.system('cls' if os.name == 'nt' else 'clear')

with open('result.json', 'r', encoding="utf-8") as json_file:
    data = json_file.read()

data = json.loads(data.encode('cp1251', errors='replace').decode('cp1251'))


USER = data['personal_information']['first_name']


def clean_text(text):
    if isinstance(text, str):
        if text == '':
            return None
        return ' '.join(text.split())
    else:
        refined_text = ''
        for part in text:
            if isinstance(part, str):
                refined_text += part
            else:
                if part['type'] == 'link':
                    return None
                refined_text += part['text']
        return ' '.join(refined_text.split())


def personal_stats(data):
    list_of_len = []
    list_of_dur = []
    year_messages_counter = {
        datetime.date.today()-datetime.timedelta(days=n): 0 for n in range(366)}
    year_calls_counter = {
        datetime.date.today()-datetime.timedelta(days=n): 0 for n in range(366)}

    for chat in data['chats']['list'][1:]:
        for message in chat['messages']:
            date = datetime.datetime.strptime(
                message['date'][:10], '%Y-%m-%d').date()

            if message['type'] == 'message' and 'forwarded_from' not in message.keys() and date in year_messages_counter.keys():
                msg = clean_text(message['text'])
                if message['from'] == USER and msg != None:
                    year_messages_counter[date] += 1
                    list_of_len.append(len(msg))
                    # print(msg, message['id'], date)

            elif message['type'] == 'service' and 'duration_seconds' in message.keys() and date in year_messages_counter.keys():
                year_calls_counter[date] += message['duration_seconds']

    return {
        'total_written_messages': len(list_of_len),
        'daily_number_of_messages': round(sum(year_messages_counter.values())/365),
        'daily_number_of_chars': round(sum(list_of_len)/len(list_of_len)),
        'daily_seconds_of_calls': round(sum(year_calls_counter.values())/365)
    }


def chat_stats(chat):
    stats = {
        'chat_name': chat['name'],
        'total_messages': 0,
        'calls_stats': {
            'total_calls': 0,
            'total_seconds': 0
        },
        'users_stats': {}
    }

    # Dropping empty dialogues
    if len(chat['messages']) < 10:
        return

    for message in chat['messages']:

        if "from" in message.keys():
            if message["from"] in stats['users_stats'].keys():
                stats['users_stats'][message["from"]]['users_messages'] += 1
                stats['users_stats'][message["from"]
                                     ]['users_letters'] += len(message["text"])
            else:
                stats['users_stats'][message["from"]] = {
                    'users_messages': 1,
                    'users_letters': len(message["text"]),
                }

        elif "duration_seconds" in message.keys():
            stats['calls_stats']["total_calls"] += 1
            stats['calls_stats']["total_seconds"] += message["duration_seconds"]

    # Additional dropping empty dialogues
    if USER not in stats['users_stats']:
        return

    # Adding AVERAGE CALL TIME
    if stats['calls_stats']['total_calls'] > 0:
        stats['calls_stats']['avg_call_time'] = round(
            stats['calls_stats']['total_seconds']/stats['calls_stats']['total_calls'])

    # Adidng AVERAGE MESSAGE'S LENGHT and CLEANING
    for user in stats['users_stats'].keys():
        stats['total_messages'] += stats['users_stats'][user]['users_messages']
        stats['users_stats'][user]['av_lenght'] = round(
            stats['users_stats'][user]['users_letters']/stats['users_stats'][user]['users_messages'])

    stats['involvment'] = round(
        stats['users_stats'][USER]['users_messages']/stats['total_messages']*100, 2)

    return stats


def global_stats(data):
    result = []
    for chat in data['chats']['list'][1:]:
        if chat_stats(chat):
            result.append(chat_stats(chat))
    return result


def show_stats(data):
    g_stats = global_stats(data)
    p_stats = personal_stats(data)

    print(f"Hello {USER}! Have you ever wondered about your Telegram statistics? Here it is. ")
    print(
        f"For the last year you have sent exactly {p_stats['total_written_messages']} messages. Not bad..")
    print(
        f"Usually you are sending around {p_stats['daily_number_of_messages']} messages {p_stats['daily_number_of_chars']} characters each. ")
    print(
        f"You seem to be very social person! And you don't forget to call your friends. Every single day you spend around {p_stats['daily_seconds_of_calls']} seconds on phone calls.\n")
    print('Here is another interesting Telegram statistics:')

    print('\nTop 5 dialogues by overall amount of messages:')
    temp = sorted(
        g_stats, key=lambda x: x['total_messages'], reverse=True)
    for chat_num in range(5):
        print(f"  {chat_num+1}. {temp[chat_num]['chat_name']} — ", end='')
        print(f"{temp[chat_num]['total_messages']}", end=' ')
        print(f"({temp[chat_num]['users_stats'][USER]['users_messages']} your's)")

    print('\nTop 5 dialogues by your involvment:')
    temp = sorted(
        g_stats, key=lambda x: x['involvment'], reverse=True)
    for chat_num in range(5):
        print(f"  {chat_num+1}. {temp[chat_num]['chat_name']} — ", end='')
        print(
            f"{temp[chat_num]['involvment']}% ({round(temp[chat_num]['users_stats'][USER]['av_lenght'])} chars per message)")

    print('\nTop 5 dialogues by phone calls:')
    temp = sorted(
        g_stats, key=lambda x: x['calls_stats']['total_seconds'], reverse=True)
    for chat_num in range(5):
        print(f"  {chat_num+1}. {temp[chat_num]['chat_name']} — ", end='')
        h = temp[chat_num]['calls_stats']['total_seconds'] // 3600
        m = (temp[chat_num]['calls_stats']['total_seconds'] - h*3600) // 60
        avg_m = temp[chat_num]['calls_stats']['avg_call_time'] // 60
        avg_s = round(temp[chat_num]['calls_stats']['avg_call_time'] % 60)
        print(f"{h} hours {m} minutes ({avg_m}:{avg_s} minutes on average)")


show_stats(data)
exit = input()
