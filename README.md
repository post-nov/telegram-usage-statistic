# Telegram usage statistic

## Description

This small script analyzes telegram usage data and calculates interesting
conclusions about user's telegram behavior for the last year.

Right now it can tell:

1. User's chat activity (total user's messages, average amount of messages 
per day, average amount for characters per message)
2. User's phone call activity (seconds per day)
3. Some "TOP 5"s (Top 5 dialogues by overall amount of messages, Top 5 dialogues
by user's involvment, Top 5 dialogues by duration of phone calls)

## Usage

1. Open Telegram desktop
2. Go to Settings > Advanced > Export Telegram data
3. Choose "Account information", "Contacts list", "Personal chats", "Private
groups" and deactivate everything else.
4. As for "Location and format" choose "Machine-readble JSON" and press EXPORT
5. After finishing export process move your results.json to directory with
_telegram-usage-statistic_ and run main.py
6. ???
7. Enjoy!

## Plans

1. Add functionality to visualize data
2. Add new statistics
3. Сorrect grammatical errors :)
