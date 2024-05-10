from typing import Generator, Optional
from . import auxiliary, model
import requests
import re
import json

class Ernie:
    def __init__(self, BAIDUID: str, BDUSS_BFESS: str):
        self.BAIDUID = BAIDUID
        self.session = requests.Session()
        self.session.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Content-Type': 'application/json',
            'Cookie': f'BDUSS_BFESS={BDUSS_BFESS};',
            'Host': 'yiyan.baidu.com',
            'Origin': 'https://yiyan.baidu.com',
            'Referer': 'https://yiyan.baidu.com/',
            'Sec-Ch-Ua': '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
        }

    def getAcsToken(self) -> str:
        return requests.get(f'https://api.api.h2oye.com/other/get_ernie_acs_token?BAIDUID={self.BAIDUID}', ).json()['data']

    def checkJson(self, data: str) -> None:
        try:
            data = json.loads(data)
        except:
            raise Exception('请求失败,响应格式错误')

        if data['code'] != 0:
            raise Exception(f'请求失败,{data["msg"]}')

    def request(self, method: str, url: str, data: Optional[dict]=None, stream: bool=False, check: bool=True) -> requests.Response:
        if method == 'get':
            self.response = self.session.get(url, params=data, stream=stream)
        else:
            self.session.headers['Content-Length'] = str(len(data))
            self.response = self.session.request(method, url, data=json.dumps(data), stream=stream)

        if not stream and check:
            self.checkJson(self.response.text)
        return self.response

    def post(self, url: str, data: dict, stream: bool=False, check: bool=True) -> requests.Response:
        return self.request('post', url, data, stream=stream, check=check)

    def getSession(self) -> model.Session:
        top = self.post(
            'https://yiyan.baidu.com/eb/session/top/list',
            {
                'deviceType': 'pc',
                'timestamp': auxiliary.getTimestamp(ms=True)
            }
        ).json()
        normal = self.post(
            'https://yiyan.baidu.com/eb/session/list',
            {
                'deviceType': 'pc',
                'pageSize': 1000,
                'timestamp': auxiliary.getTimestamp(ms=True)
            }
        ).json()
        originalTops = top['data']['sessions']
        originalNormals = normal['data']['sessions'] or []

        resultTops = []
        resultNormals = []
        for session in originalTops + originalNormals:
            conversation = model.SessionBase(sessionId=session['sessionId'], name=session['sessionName'], botModel=session['model'], creationTimestamp=auxiliary.timeToTimestamp(session['createTime']))
            if session in originalTops:
                resultTops.append(conversation)
            else:
                resultNormals.append(conversation)
        return model.Session(tops=resultTops, normals=resultNormals)

    def renameSession(self, sessionId: str, name: str) -> bool:
        self.post(
            'https://yiyan.baidu.com/eb/session/new',
            {
                'deviceType': 'pc',
                'sessionId': sessionId,
                'sessionName': name,
                'timestamp': auxiliary.getTimestamp(ms=True)
            }
        )
        return True

    def deleteSession(self, sessionId: str) -> bool:
        data = self.post(
            'https://yiyan.baidu.com/eb/session/delete',
            {
                'deviceType': 'pc',
                'sessionId': sessionId,
                'timestamp': auxiliary.getTimestamp(ms=True)
            },
            check=False
        ).json()
        return data['code'] == 0

    def deleteSessions(self, sessionIds: list) -> bool:
        data = self.post(
            'https://yiyan.baidu.com/eb/session/delete',
            {
                'deviceType': 'pc',
                'sessionIds': sessionIds,
                'timestamp': auxiliary.getTimestamp(ms=True)
            },
            check=False
        ).json()
        return data['code'] == 0

    def topSession(self, sessionId: str) -> bool:
        data = self.post(
            'https://yiyan.baidu.com/eb/session/top/move',
            {
                'deviceType': 'pc',
                'sessionId': sessionId,
                'timestamp': auxiliary.getTimestamp(ms=True)
            },
            check=False
        ).json()
        return data['code'] == 0

    def cancelTopSession(self, sessionId: str) -> bool:
        data = self.post(
            'https://yiyan.baidu.com/eb/session/top/cancel',
            {
                'deviceType': 'pc',
                'sessionId': sessionId,
                'timestamp': auxiliary.getTimestamp(ms=True)
            },
            check=False
        ).json()
        return data['code'] == 0

    def getSessionDetail(self, sessionId: str) -> Optional[model.SessionDetail]:
        session = self.getSession()
        sessions = session.tops + session.normals
        if not sessions:
            return None
        base = None
        for sessionS in sessions:
            if sessionS.sessionId == sessionId:
                base = model.SessionDetailBase(name=sessionS.name, botModel=sessionS.botModel, creationTimestamp=sessionS.creationTimestamp)
                break
        if not base:
            return None

        history = self.post(
            'https://yiyan.baidu.com/eb/chat/history',
            {
                'deviceType': 'pc',
                'pageSize': 2000,
                'sessionId': sessionId,
                'timestamp': auxiliary.getTimestamp(ms=True)
            }
        ).json()
        chats = history['data']['chats']
        histories = []
        chats = sorted(chats.values(), key=lambda data: data['createTime'])
        for chat in chats:
            histories.append(model.SessionDetailHistory(chatId=chat['id'], role=chat['role'], text=chat['message'][0]['content'], creationTimestamp=auxiliary.timeToTimestamp(chat['createTime'])))
        currentChatId = history['data']['currentChatId']
        return model.SessionDetail(base=base, histories=histories, currentChatId=str(currentChatId))

    def askStream(self, question: str, sessionId: str='', sessionName: str='', parentChatId: str='0', botModel: model.BotModel=model.BotModel.EB3_5) -> Generator[model.AskStreamResponse, None, None]:
        acsToken = self.getAcsToken()
        self.session.headers['Accept'] = 'text/event-stream, application/json'
        self.session.headers['Acs-Token'] = acsToken
        response = self.post(
            'https://yiyan.baidu.com/eb/chat/conversation/v2',
            {
                'code': 0,
                'deviceType': 'pc',
                'file_ids': [],
                'jt': '',
                'model': botModel.value,
                'msg': '',
                'newAppSessionId': '',
                'parentChatId': parentChatId,  # 官方上新会话时为数字0(但为了方便统一,初始为字符串0),之后官方是字符串
                'pluginInfo': [],
                'plugins': [],
                'sessionId': sessionId,
                'sessionName': sessionName or question,
                'sign': acsToken,
                'text': question,
                'timestamp': auxiliary.getTimestamp(ms=True),
                'type': 10
            },
            stream=True,
            check=False
        )

        if 'application/json' in response.headers.get('Content-Type'):
            self.checkJson(response.text)

        imageUrlPattern = r'<img[^>]*\ssrc=[\'"]([^\'"]+)[\'"][^>]*\s/>'
        for line in response.iter_lines(decode_unicode=True):
            if not line:
                continue

            if line.startswith('event:'):
                event = line[6:]
                continue
            elif event == 'state':
                continue
            elif line.startswith('data:'):
                data = line[5:]
                self.checkJson(data)
                data = json.loads(data)

            dataD = data['data']
            if event == 'major':
                sessionId = dataD['createSessionResponseVoCommonResult']['data']['sessionId']
                botChatId = dataD['createChatResponseVoCommonResult']['data']['botChat']['id']
            elif event == 'message':
                done = dataD['is_end']
                if done == 0:
                    answer = dataD['content']
                    urls = re.findall(imageUrlPattern, answer)
                    answer = re.sub(imageUrlPattern, '', answer)
                    answer = answer.replace('<br>', '\n')
                    yield model.AskStreamResponse(answer=answer, urls=urls, sessionId=sessionId, botChatId=botChatId, done=False)
                else:
                    answer = dataD['tokens_all']
                    urls = re.findall(imageUrlPattern, answer)
                    answer = re.sub(imageUrlPattern, '', answer)
                    answer = answer.replace('<br>', '\n')
                    answer = answer.strip()
                    yield model.AskStreamResponse(answer=answer, urls=urls, sessionId=sessionId, botChatId=botChatId, done=True)

    def ask(self, question: str, sessionId: str='', sessionName: str='', parentChatId: str='0', botModel: model.BotModel=model.BotModel.EB3_5) -> model.AskResponse:
        data = list(self.askStream(question, sessionId=sessionId, sessionName=sessionName, parentChatId=parentChatId, botModel=botModel))
        doneData = data[-1]
        return model.AskResponse(answer=doneData.answer, urls=doneData.urls, sessionId=doneData.sessionId, botChatId=doneData.botChatId)