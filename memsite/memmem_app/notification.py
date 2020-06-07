import requests
import json


def invitation_fcm(ids, name):
    # fcm 푸시 메세지 요청 주소
    url = 'https://fcm.googleapis.com/fcm/send'

    # 인증 정보(서버 키)를 헤더에 담아 전달
    headers = {
        'Authorization': 'key=',
        'Content-Type': 'application/json; UTF-8',
    }


    # 보낼 내용과 대상을 지정
    content = {
        'registration_ids': ids,
        'notification': {
            'title': '공유 저장소 초대',
            'body': name + '에서 초대합니다'
        },
        'data':
            {
                'sharing': name
            }
    }

    # json 파싱 후 requests 모듈로 FCM 서버에 요청
    requests.post(url, data=json.dumps(content), headers=headers)


def scrap_fcm(ids, name):
    url = 'https://fcm.googleapis.com/fcm/send'

    headers = {
        'Authorization': 'key=',
        'Content-Type': 'application/json; UTF-8',
    }


    content = {
        'registration_ids': ids,
        'notification': {
            'title': '새 글 알림',
            'body': '멤버가 스크랩을 공유했습니다.'
        },
        'data':
            {
                'sharing': name
            }
    }

    requests.post(url, data=json.dumps(content), headers=headers)