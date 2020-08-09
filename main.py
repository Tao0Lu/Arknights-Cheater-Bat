print("黄金蛇皮舰队 v3.5.4")  # 2020.8.9 updated by Tao0Lu forked from GhostStar/Arknights-Armada 
import mitmproxy.http

from mitmproxy import ctx, http
import copy
import json

# 是否全员获得钢铁侠buff
allMight = True
# 自定义黄金舰队干员
customChar = [
'char_2014_nian',
'char_2014_nian',
'char_2014_nian',
'char_2014_nian',
'char_2014_nian'
]

Debug = True
Servers = ["ak-gs.hypergryph.com", "gs.arknights.jp", "ak-gs-localhost.hypergryph.com",
           "ak-as-localhost.hypergryph.com"]


class Armada:
    def __init__(self):
        self.chars = json.loads(open('./character_table.json', 'r', encoding='UTF-8').read())
        self.squadFormation = {}
        self.squadFormationID = 0
        self.customChar = customChar

    def http_connect(self, flow: mitmproxy.http.HTTPFlow):
        print(flow.request.host)
        if flow.request.host not in Servers and False is Debug:
            flow.response = http.HTTPResponse.make(404)
        if flow.request.host == "ak-gs-localhost.hypergryph.com":
            flow.request.host = "ak-gs.hypergryph.com"
            flow.request.port = 8443
        elif flow.request.host == "ak-as-localhost.hypergryph.com":
            flow.request.host = "ak-as.hypergryph.com"
            flow.request.port = 9443

    def request(self, flow):
        if flow.request.host in Servers and flow.request.path.startswith("/quest/battleStart"):
            data = flow.request.get_content()
            print('%s' % (data))
            print('战斗开始 >>>')
            j = json.loads(data)
            for i, d in enumerate(j['squad']['slots']):
                if d is not None:
                    d['skillIndex'] = 0
            flow.request.set_content(json.dumps(j).encode())
        elif flow.request.host in Servers and flow.request.path.startswith("/campaign/battleStart"):
            data = flow.request.get_content()
            print('龙门战斗开始 >>>')
            j = json.loads(data)
            for i, d in enumerate(j['squad']['slots']):
                if d is not None:
                    d['skillIndex'] = 0
            flow.request.set_content(json.dumps(j).encode())
        elif flow.request.host in Servers and flow.request.path.startswith("/quest/squadFormation"):
            data = flow.request.get_content()
            # self.squadFormation = flow.request.headers['uid']

            j = json.loads(data)
            self.squadFormation = {copy.deepcopy(j['squadId']): {'slots': copy.deepcopy(j['slots']),
                                                                 'deleted': {}}}
            for i, d in enumerate(j['slots']):
                if j['slots'][i] is not None:
                    j['slots'][i]['skillIndex'] = 0
            flow.request.set_content(json.dumps(j).encode())
        elif flow.request.host not in Servers and Debug is False:
            flow.response = http.HTTPResponse.make(404)

    def response(self, flow: mitmproxy.http.HTTPFlow):
        if flow.request.host in Servers and flow.request.path.startswith("/account/syncData"):
            text = flow.response.get_text()
            j = json.loads(text)
            print('黄金舰队 ' + j['user']['status']['nickName'] + '#' + flow.request.headers['uid'] + ' 初始化...')
            j['user']['status']['secretary'] = 'char_103_angel'         # 助理
            j['user']['status']['secretarySkinId'] = "char_103_angel#2" # 助理皮肤
            j['user']['status']['iosDiamond']= 114514       # 原石个数
            j['user']['status']['androidDiamond']= 114514   # 原石个数
            j['user']['status']['gold']= 114514             # 龙门币个数
            j['user']['status']['diamondShard']=1919810     # 合成玉个数     
            j['user']['status']['ap']= 810          # 理智
            j['user']['status']['maxAp']= 810       # 理智上限
            j['user']['status']['level']=120        # 等级           
            print(len(j['user']['troop']['chars']))
            for cchar in range(0,len(customChar)):
                if cchar==0:
                    charTemp = getCustomChar(self,customChar[0],str(len(j['user']['troop']['chars'])+1+cchar))[:-1]
                else:
                    charTemp = charTemp+','+getCustomChar(self,customChar[cchar],str(len(j['user']['troop']['chars'])+1+cchar))[1:-1]
            j['user']['troop']['chars'] = json.dumps({**j['user']['troop']['chars'], **json.loads(charTemp+'}')})
            j=json.loads(json.dumps(j).replace('\\','').replace('"{','{').replace('}"','}').replace('\'','"'))
            
            if allMight:
                for lv in j['user']['troop']['chars']:
                    j['user']['troop']['chars'][lv]['potentialRank'] = 5
                    j['user']['troop']['chars'][lv]['mainSkillLvl'] = 7
                    j['user']['troop']['chars'][lv]['favorPoint'] = 240000 #信赖(非200满条)
                    charId = j['user']['troop']['chars'][lv]['charId']
                    rarity = self.chars[charId]['rarity']
                    if rarity == 0:
                        j['user']['troop']['chars'][lv]['level'] = 30
                        j['user']['troop']['chars'][lv]['evolvePhase'] = 0
                        j['user']['troop']['chars'][lv]['defaultSkillIndex'] = 0
                    if rarity == 1:
                        j['user']['troop']['chars'][lv]['level'] = 30
                        j['user']['troop']['chars'][lv]['evolvePhase'] = 0
                        j['user']['troop']['chars'][lv]['defaultSkillIndex'] = 0
                    if rarity == 2:
                        j['user']['troop']['chars'][lv]['level'] = 55
                        j['user']['troop']['chars'][lv]['evolvePhase'] = 1
                        j['user']['troop']['chars'][lv]['defaultSkillIndex'] = 0
                    elif rarity == 3:
                        j['user']['troop']['chars'][lv]['level'] = 70
                        j['user']['troop']['chars'][lv]['evolvePhase'] = 2
                        j['user']['troop']['chars'][lv]['defaultSkillIndex'] = 1
                        j['user']['troop']['chars'][lv]['skin'] = j['user']['troop']['chars'][lv]['charId'] + "#2"
                    elif rarity == 4:
                        j['user']['troop']['chars'][lv]['level'] = 80
                        j['user']['troop']['chars'][lv]['evolvePhase'] = 2
                        j['user']['troop']['chars'][lv]['defaultSkillIndex'] = 1
                        j['user']['troop']['chars'][lv]['skin'] = j['user']['troop']['chars'][lv]['charId'] + "#2"
                    elif rarity == 5:
                        j['user']['troop']['chars'][lv]['level'] = 90   # 等级
                        j['user']['troop']['chars'][lv]['evolvePhase'] = 2  # 精英等级
                        j['user']['troop']['chars'][lv]['defaultSkillIndex'] = 2 # 默认技能
                        j['user']['troop']['chars'][lv]['skin'] = j['user']['troop']['chars'][lv]['charId'] + "#2" # 皮肤

                    for e, skill in enumerate(j['user']['troop']['chars'][lv]['skills']):
                        j['user']['troop']['chars'][lv]['skills'][e]['unlock'] = 1

                    print('%s 号干员 %s' % (lv, self.chars[j['user']['troop']['chars'][lv]['charId']]['name']))
            print('')
            print('')
            flow.response.set_text(json.dumps(j))
        elif flow.request.host in Servers and flow.request.path.startswith("/quest/squadFormation"):
            text = flow.response.get_text()
            print('设置编队 >>>')
            j = json.loads(text)
            j['playerDataDelta']['modified']['troop']['squads'][
                self.squadFormation[copy.deepcopy(j['slots'])]['squadId']]['slots'] = \
                self.squadFormation[copy.deepcopy(j['slots'])]['slots']
            flow.response.set_text(json.dumps(j))
        elif flow.request.host not in Servers and Debug is False:
            flow.response = http.HTTPResponse.make(404)
            
def getCustomChar(self,charId,charNum):
    skills = self.chars[charId]['skills']
    rarity = self.chars[charId]['rarity']
    
    if rarity >= 3 and allMight:
        spLv=str(3)
        skinId=str(2)
    else:
        spLv=str(0)
        skinId=str(1)
        
    modChar='{"'+charNum+'":{"instId":'+charNum+',"charId":"'+charId+'","favorPoint":0,"potentialRank":0,"mainSkillLvl":1,"skin":"'+charId+'#'+skinId+'","level":1,"exp":0,"evolvePhase":0,"defaultSkillIndex":0,"gainTime":1556654400,"skills":[]}}'
    jsonModChar=json.loads(modChar)
    skillId = []
    modSkPart1='{"skillId":"'
    modSkPart2='","unlock":1,"state":0,"specializeLevel":'
    modSkPart3=',"completeUpgradeTime":-1}'
    modSkills=''
    
    for id in range(0,len(skills)):
        skillId.append(''.join(skills[id]['skillId']))  
    if (len(skills)) == 1:
        modSkills = modSkPart1+skillId[0]+modSkPart2+spLv+modSkPart3
    elif (len(skills)) == 2:
        modSkills = modSkPart1+skillId[0]+modSkPart2+spLv+modSkPart3+','+modSkPart1+skillId[1]+modSkPart2+spLv+modSkPart3
    elif (len(skills)) == 3:
        modSkills = modSkPart1+skillId[0]+modSkPart2+spLv+modSkPart3+','+modSkPart1+skillId[1]+modSkPart2+spLv+modSkPart3+','+modSkPart1+skillId[2]+modSkPart2+spLv+modSkPart3
    jsonModChar[charNum]['skills']="["+modSkills.replace('"','\'')+"]"
    return json.dumps(jsonModChar).replace('"[','[').replace(']"',']').replace('\'','"')
    
addons = [
    Armada()
]
