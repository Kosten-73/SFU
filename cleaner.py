import time

def delete():
    while True:
        import Chat_Bot
        Chat_Bot.clean_schedule()
        print('yes')
        time.sleep(86400)
