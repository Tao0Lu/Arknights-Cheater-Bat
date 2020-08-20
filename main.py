print("黄金蛇皮舰队 v3.5.4")  # 2020.8 updated by Tao0Lu forked from GhostStar/Arknights-Armada 
import mitmproxy.http

from mitmproxy import ctx, http
import copy
import json
entryGame=True
# 是否全员获得钢铁侠buff
allMight = True
# 自定义黄金舰队干员
customChar = []
isCustomChar = True
favorPointList = [0, 8, 16, 28, 40, 56, 72, 92, 112, 137, 162, 192, 222, 255, 288, 325, 362, 404, 446, 491, 536, 586, 636, 691, 746, 804, 862, 924, 986, 1052, 1118, 1184, 1250, 1316, 1382, 1457, 1532, 1607, 1682, 1757, 1832, 1917, 2002, 2087, 2172, 2257, 2352, 2447, 2542, 2637, 2732, 2840, 2960, 3080, 3200, 3320, 3450, 3580, 3710, 3840, 3970, 4110, 4250, 4390, 4530, 4670, 4820, 4970, 5120, 5270, 5420, 5575, 5730, 5885, 6040, 6195, 6350, 6505, 6660, 6815, 6970, 7125, 7280, 7435, 7590, 7745, 7900, 8055, 8210, 8365, 8520, 8675, 8830, 8985, 9140, 9295, 9450, 9605, 9760, 9915, 10070, 10225, 10380, 10535, 10690, 10845, 11000, 11155, 11310, 11465, 11620, 11775, 11930, 12085, 12240, 12395, 12550, 12705, 12860, 13015, 13170, 13325, 13480, 13635, 13790, 13945, 14100, 14255, 14410, 14565, 14720, 14875, 15030, 15185, 15340, 15495, 15650, 15805, 15960, 16115, 16270, 16425, 16580, 16735, 16890, 17045, 17200, 17355, 17510, 17665, 17820, 17975, 18130, 18285, 18440, 18595, 18750, 18905, 19060, 19215, 19370, 19525, 19680, 19835, 19990, 20145, 20300, 20455, 20610, 20765, 20920, 21075, 21230, 21385, 21540, 21695, 21850, 22005, 22160, 22315, 22470, 22625, 22780, 22935, 23090, 23245, 23400, 23555, 23710, 23865, 24020, 24175, 24330, 24485, 24640, 24795, 24950, 25105, 25260, 25415, 25570]
with open('chatList.txt','r') as f:
    for line in f:
        customChar.append(line.strip('\n'))
        if customChar[0]=='noCustomChar':
            isCustomChar = False
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
            print('战斗开始 >>>')
            j = json.loads(data)
            if not j['squad']==None:
                for i, d in enumerate(j['squad']['slots']):
                    if d is not None:
                        d['skillIndex'] = 0
            flow.request.set_content(json.dumps(j).encode())
        elif flow.request.host in Servers and flow.request.path.startswith("/campaign/battleStart"):
            data = flow.request.get_content()
            print('龙门战斗开始 >>>')
            j = json.loads(data)
            if not j['squad']==None:
                for i, d in enumerate(j['squad']['slots']):
                    if d is not None:
                        d['skillIndex'] = 0
            flow.request.set_content(json.dumps(j).encode())
        elif flow.request.host in Servers and flow.request.path.startswith("/quest/squadFormation"):
            data = flow.request.get_content()
            # self.squadFormation = flow.request.headers['uid']
            j = json.loads(data)
            self.squadFormation = {copy.deepcopy(j['squadId']): {'slots': copy.deepcopy(j['slots'])}}
            for i, d in enumerate(j['slots']):
                if j['slots'][i] is not None:
                    j['slots'][i]['skillIndex'] = 0
            flow.request.set_content(json.dumps(j).encode())
        elif flow.request.host not in Servers and Debug is False:
            flow.response = http.HTTPResponse.make(404)

    def response(self, flow: mitmproxy.http.HTTPFlow):
        global entryGame
        if flow.request.url.startswith("https://ak-fs.hypergryph.com/announce/Android/preannouncement.meta.json") or flow.request.url.startswith("https://ak-fs.hypergryph.com/announce/IOS/preannouncement.meta.json"):
            entryGame=True
        if flow.request.url.startswith("https://ak-as.hypergryph.com:9443/online/v1/ping"):
            j=json.loads(flow.response.get_text())
            if entryGame:
                flow.response.set_text('{"result":0,"message":"OK","interval":5400,"timeLeft":-1,"alertTime":600}')
                entryGame=False
            else:
                flow.response = http.HTTPResponse.make(404)
            if j['message'][:6]=='您已达到本日':
                print('明日方舟防沉迷破解: 您已达到本日在线时长上限或不在可游戏时间范围内，破解后仍可以继续游戏，但请合理安排游戏时间。')
            else:
                s = j['timeLeft']
                h = int(s/3600)
                m = int((s-h*3600)/60)
                ss = int(s-h*3600-m*60)
                print('明日方舟防沉迷破解: 游戏剩余时间 '+str(h)+'小时'+str(m)+'分钟' + str(ss)+'秒 修改为 不限制，但请合理安排游戏时间。')
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
            j['user']['status']['level']= 120       # 等级           
            print(len(j['user']['troop']['chars']))
            
            if isCustomChar:
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
                    j['user']['troop']['chars'][lv]['favorPoint'] = favorPointList[200] #信赖(非200满条)
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
                        j['user']['troop']['chars'][lv]['level'] = 90           # 等级
                        j['user']['troop']['chars'][lv]['evolvePhase'] = 2      # 精英等级
                        j['user']['troop']['chars'][lv]['defaultSkillIndex'] = 2    # 默认技能
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
            j = json.loads(text)
            squadId=str(j['playerDataDelta']['modified']['troop']['squads'])[2:3]
            j['playerDataDelta']['modified']['troop']['squads'][squadId]= self.squadFormation[squadId]
            flow.response.set_text(json.dumps(j))
        if flow.request.host not in Servers and Debug is False:
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
