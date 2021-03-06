import os
from flask import request
import json

from flask_restful import Resource
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    TextSendMessage, ImageSendMessage
)


class LineGroupController(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        payload = request.get_json(force=True)

        line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
        handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
        event = payload['events'][0]
        token = event['replyToken']
        message = event['message']['text']
        line_type = event['source'].get('type')
        group = event['source'].get('groupId')
        room = event['source'].get('roomId')
        user = event['source'].get('userId')

        if message == '你走吧':
            if line_type == 'group':
                line_bot_api.reply_message(token, TextSendMessage(text='走了88'))
                line_bot_api.leave_group(group_id=group)
            elif line_type == 'room':
                line_bot_api.reply_message(token, TextSendMessage(text='走了88'))
                line_bot_api.leave_room(room_id=room)
            else:
                line_bot_api.reply_message(token, TextSendMessage(text='為什麼不是你走？'))

        elif line_type == 'group':
            if message == '群組資訊':
                count = line_bot_api.get_group_members_count(group_id=group)
                summary = line_bot_api.get_group_summary(group_id=group)
                text = f'群組名稱➡️ {summary.group_name}\n當前群組人數為➡️ {count}'
                line_bot_api.reply_message(
                    token, messages=[
                        TextSendMessage(text=text),
                        ImageSendMessage(
                            original_content_url=summary.picture_url,
                            preview_image_url=summary.picture_url,
                        )]
                )
            elif message == '我是誰':
                profile = line_bot_api.get_group_member_profile(group_id=group, user_id=user)
                text = f'你是➡️ {profile.display_name}\nID➡️ {profile.user_id}'
                line_bot_api.reply_message(
                    token, messages=[
                        TextSendMessage(text=text),
                        ImageSendMessage(
                            original_content_url=profile.picture_url,
                            preview_image_url=profile.picture_url,
                        )]
                )

            line_bot_api.reply_message(token, TextSendMessage(text=message))

        elif line_type == 'room':
            if message == '聊天室資訊':
                count = line_bot_api.get_room_members_count(room_id=room)
                text = f'聊天室人數為: {count}'
                line_bot_api.reply_message(token, TextSendMessage(text=text))
            elif message == '我是誰':
                profile = line_bot_api.get_room_member_profile(room_id=room, user_id=user)
                text = f'你是➡️ {profile.display_name}\nID➡️ {profile.user_id}'
                line_bot_api.reply_message(
                    token, messages=[
                        TextSendMessage(text=text),
                        ImageSendMessage(
                            original_content_url=profile.picture_url,
                            preview_image_url=profile.picture_url,
                        )]
                )

            line_bot_api.reply_message(token, TextSendMessage(text=message))

        else:
            line_bot_api.reply_message(token, TextSendMessage(text=message))

        response = {
            "statusCode": 200,
            "body": json.dumps({"message": 'ok'})
        }

        return response
