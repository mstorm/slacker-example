import json

from slacker import Slacker
from websocket import create_connection

TOKEN = 'CHANGE ME TO SLACK TOKEN'


class Echo:
    def __init__(self):
        self.slacker = Slacker(TOKEN)

    def run(self):
        rtm = self.slacker.rtm.start()
        connect = create_connection(rtm.body['url'])
        bot = rtm.body['self']

        while True:
            response = connect.recv()
            obj = json.loads(response)

            if obj['type'] == 'hello':
                print('{}({}) connected.'.format(bot['name'], bot['id']))

            if 'bot_id' in obj:
                continue

            try:
                if obj['type'] == 'message':
                    if obj['text'] == 'exit':
                        break

                    self.slacker.chat.post_message(obj['channel'], obj['text'], as_user=True)

            except Exception as e:
                print(e)


if __name__ == "__main__":
    Echo().run()
