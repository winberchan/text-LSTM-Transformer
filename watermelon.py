# 原则：不碰八卦无聊视频，只关注有意义的话题
# from http.cookiejar import Cookie
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
# 设置等待执行语句
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime
# enable multi-thread download
from concurrent.futures import ThreadPoolExecutor,wait,ALL_COMPLETED
import urllib.request
import re
import sys
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
import requests
import json
import random
import zlib


window_first = None
window_second = None
CHANNEL_BAN_NAME = "笑|幽默|娱|综艺|剧|影|视|台|片|戏|史|资讯|新闻|网|报|社|故事|精选|解说|情感|档案|正能量|科普|公安|策划|游戏|竞技|体育|球|棋|帮|纪实|财经|思维|教育|音乐"

# TITLE_BAN_WORDS="史|剧|M国|米国|老美|美方|加国|美帝|霸权|游戏|守国门|对抗路|歪果仁|外挂|纪实|欢乐|童星|国足|中超|宣传片"\
# "|英军|法军|比利时|荷兰|捷克|瑞典|挪威|芬兰|波兰|亚洲|欧洲|拉美|美洲|非洲|多地暴雨|直击|什么信号|遏制炒作|塞尔维亚|惊爆价"\
# "|罗马尼亚|奥地利|斯洛伐克|匈牙利|希腊|瑞士|卢森堡|丹麦|保加利亚|阿尔巴尼亚|赴美|军武|军事|玩法|四家银行|露营|穷游|西藏"\
# "|爱沙尼亚|西班牙|立陶宛|克罗地亚|拉脱维亚|葡萄牙|摩纳哥|摩洛哥|爱尔兰|梵蒂冈|冰岛|波黑|欢度|佳节|气急败坏|大快人心|务必"\
# "|澳大利亚|澳洲|新西|以色列|台海|菲律宾|巴西|印军|尼泊尔|金星|火星|亚美尼亚|阿塞拜疆|阿联酋|北极|探房|价格便宜|以案说法|外围市场"\
# "|巴拿马|南非|阿根廷|哥伦比亚|智利|洪都拉斯|海地|秘鲁|乌拉圭|巴拉圭|厄瓜多尔|玻利维亚|汉奸|日料店|专家|致敬|公知|宇航|间谍|航母|老外|短线|同床共枕"\
# "|柬埔寨|老挝|马来西亚|新加坡|印尼|阿富汗|巴基斯坦|沙特|埃及|喀麦隆|动画|动漫|非诚勿扰|嘉宾|牵手|刘涛|力压|王思聪|假如"\
# "|任正非|孟晚舟|曹德旺|郭台铭|唐湘龙|郑强|陈翔|林生斌|祖国|叛国|爱国|伊朗|哈萨克|解放军|横店大姐|破坏力|北海道|基辅|911"\
# "|美日|美欧|日美|美韩|美印|美、日|日、美|美台|美加|美俄|英美|美英|美好|祈福|祈祷|魅力|粉丝|新闻|温暖|良心债|百年名校|面试题|新思路|伊拉克|足协|男足"\
# "|改编|大国|反制裁|感人|感动|加油|挺住|雄起|点赞|深情|情深|田园|传奇|振奋人心|机型|折扣|白菜处理|男篮|长钢筋|假如"\
# "|背水一战|纪录|记录片|秘诀|走俏|好物|清单|保价|优美|黑粉|七仙女|公主|巴铁|异国|日入|北漂生活|真实生活|日常|牢记|一定要"\
# "|塔克拉玛干|土豪|赊刀|吉隆坡|多可怕|绿野|脱口秀|哥斯拉|金刚|星爵|沙雕|调解|泪点|多国|暴毙|烂尾了怎么办|奖励|三大保险"\
# "|武警|军民|官民|灵异|防洪|抗洪|抢险|抗灾|官兵|飞行员|爆笑|剪辑|配音|手写|直播间|省钱|值得购买|最佳方案|自研芯片|小生意"\
# "|缅甸|大盘|横盘|板块|人有情|比赛|赵川|包住|股海|淘金|午评|低开|创业板|会员|套餐|主持人|同花顺|期价|加州|收藏|经济学|车型"\
# "|孟加拉|大四|正能量|蒙古国|黑手|惊喜|双碳|官媒|碳中和|碳达峰|古人|玩家|软饭|活不下去|律师|曼联|哈登|工人急诊|视频播放"\
# "|搞笑|娱乐|综艺|资讯|故事|精选|解说|情感|档案|王千源|超燃|科普|上集|下集|哪料|魔兽|哇塞|哇噻|佛祖|房车|军情|空军|法治进行时"\
# "|只买国产|支持国货|抵制洋货|欧亚|爱了|温哥华|纽约|洛杉矶|旧金山|悉尼|墨尔本|伦敦|迪拜|仙境|崇洋媚外|慕洋犬|要还么|贤妻|洪水的破坏力|人死后"\
# "|发薪灵活|无套路|小品|相声|光鲜|起死回生|日入斗金|白手起家|荒废学业|不可怕|死神|表态|剁手|好方法|秘籍|骄傲|感悟|还清|翻身|逆风|翻盘"\
# "|新一轮|调整|哪些|中考|数学|嗨起来|或影响|局部|局地|不要怕|不用怕|不要慌|不用慌|没必要慌|不用害怕|别慌|不慌|多严重|劲爆|营销"\
# "|普吉岛|首选|道士|巨龙|英雄|法海|石敢当|牛皮糖|帮忙讨|老农民|探盘|暴雪公司|商业逻辑|赚钱机会|乱选|名嘴|赛场|创造营|奇迹|型号"\
# "|生活大爆炸|地主|凤姐|华智冰|节目|戚薇|惊天大秘密|郑恺|人设|今天玩|托卡|和平精英|王者荣耀|惬意|夜游神|名人|源头工厂|新模式"\
# "|丑恶|嘴脸|美元危机|沙漠|华为旗舰|极具特点|NBA|CBA|私人衣物|央视|董卿|传说中|万年前|上|金币|抗日|三国|盘点|亿年前|万年前|千年前|百年前"\
# "|炖|真香|晚餐|午餐|早餐|猫|狗|煮|食材|炒一盘|厨艺|素菜|闷酒|锅盖|吃|黄油|蛋卷|麻辣|早饭|午饭|晚饭|鸡腿|烧鸡|解馋|味道|土豆|牛肉|蛋糕"\
# "|字幕|公考|邪门|玩闹|小舅子|一车难求|惨淡收场|怎么做到的|难得|左宗棠|梦幻西游|复刻|令人唏嘘|母爱|所罗门|王天一|吕钦|发大财|苏梅岛|岛国|作文"\
# "|人间有爱|西瓜视频|视频计划|婚后男人|鉴赏|钟南山|终南山|取暖方式|强势反弹|荣耀|新优势|一帮到底|全民帮帮|围着打|血洗|大阪|埃尔克森|穆里奇|梅开二度"\
# "|古玩|老货|汉代|陶玲|火爆|张捷|新款|男友|女友|仿鞋|鞋贩|神操作|迪士尼|流浪大姐|唐老鸭|喜羊羊|灰太狼|郭德纲|监理|捡钱|每天进账|二手机|张学友"\
# "|夏威夷|李嘉诚|马云|马未都|曼谷|精装修|董事长|陈亚男|隔离生活|感恩|制作|直招|笑而不语|函数|EXCEl|拳王|拳击|指甲|私处|减肥|三大|教程"\
# "|恐怖片|怪物|全民负债|能不能买|精灵|版本|心得|深夜独白|出手|千万不|千万别|售价|马帅|杨紫|天王|玩火|自焚|公公|欧冠|C罗|复制粘贴"\
# "|完整版|戏曲|绿巨人|奥特曼|高龄|宋美龄|鬼宅|传说|结局烂尾|幽游白书|新秀|霸气|补漏帮|丘比特|王牌|部队|督导|强调|必胜|散户|第一期|闹鬼"\
# "|凌杰|推射|破门|谭凯元|比分|选手|报名|蒋介石|陈亚楠|总理|小蒋|疯玩|大雄|小鲜肉|情趣|总裁|三峡大坝|老戏骨|谢娜|Apink|恭喜"\
# "|运营方案|经营模式|伟人|毛泽东|吴京|高光时刻|欧阳娜娜|黄磊|仪式|出轨|中医|攻略|高考|张柏芝|沈腾|杨幂|江南皮革厂|果然视频"\
# "|面食|卤子|茶|养生|零食|饼|做饭|油条|豆腐|一荤一素|营养|喝一杯|包子|菜馅|肉夹馍|海带|美味|一日三餐|寿司|拌饭|酒|红烧|饺子"\
# "|要注意|补仓|商业模式|案例|冯巩|牛莉|纪晓岚|人“弃|人弃|切记|一本万利|好丽友|手游|励志语录|拜登|普京|宋祖英|香港街头|厂房出租"\
# "|彩票|印钞厂|帝师|蘑菇头|笑疯|年纪轻轻|年级|很满足|董明珠|司马南|涂磊|抖音|#工厂实拍视频|中视频|头条|斯里兰卡|总统|小国"

TITLE_BAN_WORDS="史|剧|M国|米国|老美|美方|加国|美帝|霸权|游戏|守国门|对抗路|歪果仁|外挂|纪实|欢乐|童星|国足|中超|宣传片|暴打"

SEARCH_KEY_DICT={
# ################################民生三板斧
# "倒闭":"","失业":"","负债":"",
# ################################极端天气
# "暴雨":"","冰雹":"","洪水":"",
# ################################疫情
# "北京 封":"","上海 封":"","小区 封":"",
# 這個頻道一直搬運視頻對其他誠實創作者公平嗎
}
# 常规热点 TOP 20
SEARCH_KEY_DICT_SLOW={
# Elastic 7
"我股票亏钱":"","我贷款炒股":"","A股割我韭菜":"","折叠机质量差":"","美领馆":"","浦东机场":"","火车站流浪汉":"",
# stable 13
"倒闭":"","失业":"","负债":"","欠薪":"","降薪":"","裁员":"","冷清":"","生意 难":"",
"外贸 难":"","实体难":"","电商 亏":"","闭店":"","停业":"",
}
# special keys, maximum to 66
SEARCH_KEY_DICT_COLD={
# 中国制造
"厂 没订单":"","厂 关":"","厂 撤":"","厂 停":"","撤离中国":"",
"义乌 没订单":"","富士康 撤":"","厂 没事做":"","厂 倒闭":"",
"停工":"","停产":"","车间 停":"","返乡潮":"","废弃":"",
"惨淡":"实|城|镇|街|生意|车|市|场|店|商|地|货|行|厂|业",
"荒废":"厦|城|镇|酒店|别墅群|宅|工业|科技|馆|厂|景|车",
"华为质量差":"","比亚迪质量差":"",
# 中国金融
"银行 封":"","我取不出钱":"","银行 限":"","爆雷":"","投资 亏":"",
"发不出工资":"","破产":"","拖欠":"","涨价":"","集体维权":"","萧条":"",
"我失业":"","我负债":"","房 亏":"","房 降":"","工资低":"","待业":"","停招":"",
"房 断供":"","房 租不出":"","商铺空置":"","房 悔":"","写字楼空置":"","没收入":"",
"北京失业":"","上海失业":"","北京倒闭":"","上海倒闭":"","找不到工作":"","找工作 难":"",
}
# FROZEN
# #-------------------------------------------------------工厂外贸类
# "厂 没订单":"","厂 没事做":"","厂 没活干":"","厂 拆":"","工厂搬离":"","厂 迁":"","厂 停":"","厂 撤离":"","厂 关":"",
# "厂里没班加":"","不招工":"","厂 没发工资":"","厂房出租":"","停厂":"","工厂放假":"","厂 废弃":"","义乌 没订单":"",
# "厂 没生意":"","工厂撤离":"","工人聚集":"","厂房 空":"","厂 倒闭":"","厂 搬越南":"",
# "接不到订单":"","停工":"","停产":"","搬离深圳":"","机器 停":"","车间 停":"","机床 停":"","比亚迪 坑":"",
# "富士康 撤":"","订单":"","工厂惨淡":"","服装厂":"","工业园":"","外资撤离":"","订单萎缩":"","订单转移":"",
# "工人聚集":"","拉横幅":"","工人维权":"","撤离中国":"","倒闭":"",

# # -------------------------------------------------------工作工资类
# "找不到工作":"","打工难":"","北漂":"","没工作":"","下岗":"","北京失业":"","欠薪":"","降薪":"","我 失业":"","裁员":"",
# "工资减少":"","工资低":"","找工作 难":"","停招":"","上海失业":"","没收入":"","拖欠工资":"","待业":"","失业":"","负债":"",


# # ------------------------------------------------------实体生意类
# "生意 难":"","实体难":"","关门":"","电商 亏":"","关店":"","创业 亏":"","投资 亏":"","萧条":"","冷清":"",
# "惨淡":"实|城|镇|街|生意|车|市|场|店|商|地|货|行|厂","闭店":"","停业":"",


# #-------------------------------------------------------房产债务类
# "房 断供":"","房 亏":"","房 降":"","后悔买房":"","房 卖不出":"","空置":"","废弃":"","人去楼空":"",
# "暴雷":"","破产":"","烂尾":"","荒废":"厦|城|镇|酒店|别墅群|宅|工业|科技|馆|厂|景","法拍房":"","房 租不出":"",


# #-------------------------------------------------------银行金融类
# "银行 取钱":"","银行 封":"","银行冻结":"","银行拒绝交易":"","银行不营业":"","银行 异常":"","取不出钱":"",
# "银行":"","银行 限":"","ATM取不出钱":"","银行 扣":"","银行卡不能用":"","银行不营业":"","柜员机用不了":"","银行 停":"","银行 关":"","取钱":"",
# "银行证明本人":"","ATM用不了":"","银行排队":"","信用卡":"","数字人民币":"","银行卡":"","ATM":"","储蓄卡":"","非柜面交易":"","断卡行动":"",
# "银行不能支付":"","不能转账":"","银行预约":"","取钱 出问题":"","银行存钱变少":"","对公账户":"","取款机":"","限制存取款":"",


# #-------------------------------------------------------物价开支类
# "水果贵":"","物价贵":"","物价涨":"","菜 贵":"","猪肉 贵":"","菜价 涨":"",
# "开支大":"","消费高":"","开销大":"","物价":"","油价 涨":"","水泥 贵":"","原物料 涨":"","煤炭涨价":"","取暖 难":"","煤 贵":"",


# #-------------------------------------------------------其他话题类
# "工业软件":"","不生孩子":"","压力大":"",
# "出境":"","出海关":"","机场 没人":"","港口":"","美领馆":"","现状":"","移民":"","实拍":"","人民公社":"","国产 差":"","录音":"",
# "保险 亏":"","山姆超市":"","华为坑":"","口岸":"","机场":"","火车站":"","深圳北站":"","虹桥火车站":"","浦东机场":"",



CHANNEL_BLACKLIST=["农村一浪","希望骑士","和大家分享","李子真还传","社会时分秒","大辉在南方的流浪生活","飞鸟夕阳红","生意优加思维","大胖日记666",
"青蜂侠","湖北小勇","意外警示录","地三代","幸运儿杨淼","雷哥创业(重启人生路)","演绎大都市","纪实生活馆","市场敬畏者","不咋老司机","小戈美景","郑谊",
"那年的下雨天","小友职场","墨尔本杰夫说","发小光体基顿","贵阳风景宗哥","吕延钊","北漂小鱼儿","未知学堂","文哥负债前行","唐探","深度研究院1","永远奔跑的蜗牛",
"河南都市频道","谭天才Tim","关老弟辅拍信息咨询","辉哥闲聊7k8q","洞悉天下","GRT今日关注","夕阳无限美8I5E","骚骚骚骚骚","喝酒干哈风格","大美丽的休闲生活",
"大湾区看楼","小冉超可爱ya","看我的","春秋吧主农民公","老宋快评","王小敢日记","哲哥体育","远见卓识的小帅","Xi说经管","萨沙之光","车一圈","文明天下",
"雪纳瑞","芝麻梦蝶","回娘家开会","车库创业记","翰逸神飞","刘导问市.","简单的糊涂涂","华数爱豆应试指南","当代青年小草","云中探月","磐石之心","甘肃农民娃",
"第三人名","最美的期待a","把生活过成了一地鸡毛","青年时代说","辉哥聊","星辉前沿","励志姐在上海","云南老黄","刘总杂谈","憨憨的叮叮咚咚锵","大浣熊v",
"琴声悠扬6788","素时光","风行闪闪的岁月","DV现场","开心黑眼熊","大方神","川贝VLOG","大城小巷vlog","老垄","苏州女婿闯王","孤凉地方很多","毛毛虫vlog",
"江湖油条","小品相声大联欢","优质读书会","职位多丽丽","夏馋馋爱次","翰宝宝的妈","商业模式设计重构创新","认真的柳叶花","倒霉聚集地","智慧清枫","钱普贵",
"老胡梦游记","bu许song手","天气观","乐田围军仔","心向大自然","80后堂主聊创业","达文Bw","新科学集锦","摇啊摇啊尧","回看","金日油条","辽宁都市红绿灯",
"大范甘迪几个","小贝贝说","王者说娱","筑意","只要好运","保德全","大参考","免受批评","小年观上岸","WIN秘斯特吴","阿牛记录","护城河数据","雲淡峰來",
"豆豆妈咪生活录","运筹帷幄赵铁柱","晶莱有料","中国三农发布","邵彩利","西瓜生活图鉴","你哒老弟","San0而已","驰哥走天下","沸闻天下","快闪速息","央央碎碎念",
"大参考","晚间800","西悦说","PP萌说济世录","泰国很哇塞","优雅松原1","茉茉妈Vlog","小贾的幸福vlog","天津港大军说车","月老伟大侠","足智多谋极速加菲尔德",
"北辛观察","相信明天的路依旧如初","7號调茶局","进口车大军说车","智能相对论","羊说羊语","房产一起评","鱼夹子Justin","小武哥聊车","韭菜一家人","姚自由的生活",
"V科技奇趣","砌砖高手司徒","人才龙哥","沃太能源AlphaESS","澎湃眼界","弓立军","潇湘雅士宇轩","卡车玩家","随性自由的辰星MrChen","寻宝道人","小冰赛车",
"alsk","浅吟旧情歌他难听","黟县汪先生","有怪事","山大杰叔","天涯之雁","南瓜午夜厅","旺仔探房","阿庆在努力前行","庞明说房","开怀笑不停","小颖荒野",
"普罗旺斯的狗尾巴草xx","看生活日记","香港豪仔vlogs","假如周杰伦没见过花海","tigergb","香港豪哥Vlog","哦破哦破了","王者荣耀小白BGM","阿吴梦蝶",
"正直最新快讯","富士康人资招聘晓东","追梦人Ricky","荒野部落","米奇沃克斯","兰强君玲看职场","优雅梦想f","专业房参谋","四川观察","房资物语","有机遇呀",
"奥特-别曼","89年粤东小哥","面试官小胡","明日观察室","臧其超生意经","揭录生活","木鸡2021","小脏和Jrny在苏梅岛","李大头zyxp","高臻臻的脑细胞",
"翼龙说事","吃茶的王哥","马文频道","加多宝666","认真听歌的人","三妮聊留学","托哥来了","人力资源小司机","打工人的神秘面纱","靓女爱吃瓜","农民山大叔",
"广西大罗","何有理来了丨栏目","天文商学","乙知经融","阿杰旅行记","粤西小伍","大掌柜在路上","虾逼逼","dyf21yxwidjj","憨憨俩兄弟","店道老赵","虹声天下",
"聊些什麽","农村仨人行","发财哥volg","负债小博","杨阳的vlog","嘟妈VLOG","加油啊一心姐","重庆妹","一一说房产","80后老雷谈生活","小杰话公考",
"健康管理师耿大迎","好吃嘴牛锅锅","吴老梗","一箩筐奇趣","卫星聊地图","霸都包租公","小区的家伙们官方频道","豫洛小陈","小刀的尼泊尔女友","记录HONGKONG",
"工厂圈白老师","大白兔0215","大刘说说","林小宝的负债生活","数据会跳舞","长江号外","北美补锅匠","张兴国谈经营","神都溜达","退休四姐爱旅游","北京小叔",
"余生有你h","小王在河南","普拉斯小姐","甜爸郑大帅","娄哥侃大山","天津韩哥","工厂白老师","湖北丰哥168","强老哥","36岁大龄剩男的人生","小萍在路上",
"康泰房地产刘德","赵瑜伟vlog","房产大象","华致信地产","南哥说异","小郭聊人生","海派娄哥","青藤说品牌","尧涛探房","大志聊负债","惠州伊姐","海海海藻",
"司马看世界","花喵去吃饭","涛弟碎碎念","番茄和小杨","谈古论今说说","大本越洋澳洲","玩名堂主","自媒体博哥","四叔石头记","胡姐儿好好生活吧","咸鱼梦想家vlog",
"云南发哥volg","房产最先知","啡小沫","佩新说","创业研究蔡佰晓","大刘姐说创业","祥哥在广州","小马在努力1990","布丁小心灵","返乡的琪琪","浪子不负",
"二勇在上岸路上前行","鸿雁说","大冰在广州","小宁说事你听听","强老师儿","琢磨女士","雷哥在努力","生煎娘舅","井空","孙婷婷要变成个大瘦子","北漂乔克",
"慕容的vlog日记","王小陌说","强子农村事","陈大琛的","越南旅途生活","光明网","丽姐玩具","丽姐传媒4E6C","揪住学姐的动脉","电视人曾小强","广西肥娟生活日记",
"韩秀云讲经济","远方的小宇","颜值king","勇敢曾队长","聋哑人黄哥","一只奔跑的柠檬","马克CN","云村姚妹","家哥v","大脸小美","五桥老周","虎妈外贸","照理说事",
"不怕服输的建始晓锋","人力-英姐","楠楠家外贸","小王来胡侃","陈小苏","邓碧萝小腰总","五层黑大叔","横漂浪哥","我是都是洞","工厂白老师品德企业","王富海",
"光棍小胖","率真小朱日常","摄影兵工厂小鱼","小铭旅拍记","佩新频道","黄喂喂","未公开的世界","财经主持人周媛","型男行走乡村","布衣商道自媒体","我是都是锅",
"秀秀1978","红岩说","张哥创业","鸿言说","暴走雪木君","楼兰阿宁","在下阿侨","环华十年","老谭纪事","吃饭睡觉逗艾艾","侣行","小叔tv","汤山老王",
"玉酱日本生活","小哥Ricky","麦小兜和钱贝","三千说表","这车值么","丽君de小世界","硅谷吴军","婷大虾","行哥嘚啵嘚","尤黎斗斗","万牛回首","小食光光",
"职场小钢炮","跟着华子去旅行","评论员王攀","峰哥说说事","PP古风武侠集","晓波二手车","老军骨","桃桃财富圈","于航的法商实践课堂","房参谋官方账号",
"子恒海外之旅","春雷加油呀","小兰观民生","大胡子魏","好运平凡人","百姓日常生活记录","黑皮晓洁一起看世界","王大原"]


# check if xigua channel existed in youtube
def youtube_check_channel(driver, channel):
    return False
    channel_existed = False
    driver.switch_to.window(window_first)
    driver.get("https://www.youtube.com/results?search_query="+channel)
    driver.switch_to.window(window_first)
    youtube_result = ""
    try:
        #  //*[@id="text"]                             /html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-channel-renderer[1]/div/div[2]/a/div[1]/ytd-channel-name/div/div/yt-formatted-string
        youtube_result = driver.find_element(By.XPATH,"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-channel-renderer[1]/div/div[2]/a/div[1]/ytd-channel-name/div/div/yt-formatted-string").get_attribute('textContent')
        # youtube_result = driver.find_element_by_id('text').get_attribute('textContent')
    except Exception as e:
        if "Unable to locate element" in str(e):
            print(f"Not found channel {channel} in youtube")
        else:
            print(e)
    if youtube_result != "":
        if youtube_result.strip() == channel.strip():
            channel_existed = True
        print("Found youtube channel:"+youtube_result+" by searching xigua channel:"+channel)
    driver.switch_to.window(window_second)
    return channel_existed

# check if video title existed in youtube
def youtube_check_title(driver, title):
    return False
    title_existed = True
    driver.switch_to.window(window_first)
    driver.get("https://www.youtube.com/results?search_query="+title)
    driver.switch_to.window(window_first)
    youtube_result = ""
    try:
        youtube_result = driver.find_element(By.XPATH,'//*[@id="video-title"]/yt-formatted-string').get_attribute('textContent')
    except Exception as e:
        if "Unable to locate element" in str(e):
            title_existed = False
        else:
            print(f"{title} -------------> {e}")
    if youtube_result !="":
        if len(youtube_result)>=10 and title[:10] != youtube_result[:10]:
            title_existed = False
        else:
            print(f"youtube title search result:{youtube_result}, xigua_title:{title}")
    driver.switch_to.window(window_second)
    return title_existed

# search by key word
def xigua_search(driver, main_key, sub_keys, previous_urls, in_download_urls, future_tasks, executor, running_mode):
    # video struct: (url,title)
    try:
        page_array = driver.window_handles
        if len(page_array) == 1:
            global window_first
            window_first= page_array[0]  
        try:
            if len(driver.window_handles) >1:
                driver.get("https://www.ixigua.com/search/"+main_key)
            else:
                input_box = WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.CLASS_NAME,'input')))
                input_box.clear()
                input_box.send_keys(main_key)
                driver.find_element(By.CLASS_NAME,'search-btn').click()
            sleep(2)
        except Exception as e:
            print("input box failed! Try again!")
            print(e)
            if len(driver.window_handles) >1:
                driver.get("https://www.ixigua.com/search/"+main_key)
            else:
                driver.refresh()
                sleep(3)
                input_box = driver.find_element(By.XPATH,'//*[@id="App"]/div/header/div/div/div[2]/div/div[1]/div[2]/input')
                input_box.clear()
                input_box.send_keys(main_key)
                driver.find_element(By.CLASS_NAME,'search-btn').click()
        #switch to new page
        if len(page_array) == 1:
            global window_second
            window_second = driver.window_handles[1]
        # print(f"window first:{window_first}, window second:{window_second}")
        driver.switch_to.window(window_second)
        # click 筛选 to filter,  this element cannot be found in headless mode
        try:
            # filter_BTN = WebDriverWait(driver,60).until(EC.visibility_of_element_located((By.CLASS_NAME,'search-show-con__categories')))
            filter_BTN = driver.find_element(By.XPATH,'//*[@id="App"]/div/main/div/div/div[1]/div/div[1]/div/div/span/span')
        except Exception as e:
            print("筛选 button click failed! Try again!")
            print(e)
            driver.save_screenshot('filter_BTN_click_error.png')
            driver.refresh()
            sleep(3)
            filter_BTN = driver.find_element(By.XPATH,'//*[@id="App"]/div/main/div/div/div[1]/div/div[1]/div/div/span/span')
        # 点击移除通知对话框
        sleep(3)
        ActionChains(driver).move_by_offset(1842,90).click().perform()
        sleep(2)
        ActionChains(driver).move_by_offset(-1842,-90).perform()
        filter_BTN.click()
        # click 最新 to order by newest
        driver.find_element(By.XPATH,"//li[contains(text(),'最新')]").click()
        # get search-result DIVs
        # items_DIV = driver.find_elements_by_css_selector('.HorizontalFeedCard__rich__media')
        items_DIV = WebDriverWait(driver,30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.HorizontalFeedCard__rich__media')))
        duration_list = driver.find_elements(By.CLASS_NAME,'HorizontalFeedCard__coverContainer')
        div_size = len(items_DIV)
        duration_size = len(duration_list)
        print(f"itemsDIV length {len(items_DIV)}, duration_list length {len(duration_list)}")
        real_size = min(div_size,duration_size)
        if real_size == 0:
            print("items is empty")
        # filter results by time,sub_keys,channel
        for i in range(real_size):
            # print(item_DIV.text)
            item_DIV = items_DIV[i]
            # print(f"successfully got the {i}th item of items_DIV: {item_DIV.text}")
            title = str(item_DIV.find_element(By.TAG_NAME,"a").get_attribute("title"))
            played_info = item_DIV.find_element(By.CLASS_NAME,"HorizontalFeedCard-accessories-bottomInfo__statistics").text
            url = item_DIV.find_elements(By.TAG_NAME,"a")[0].get_attribute("href")
            channel = item_DIV.find_elements(By.TAG_NAME,"a")[1].text

            # choose recent videos  分钟 小时
            if running_mode == "fast":
                if not re.search("分钟前|刚刚",played_info):
                    continue
                else:
                    print(f"video {title}, played_info: {played_info}")
            elif running_mode == "slow":
                if not re.search("分钟前|小时前|刚刚",played_info):
                    continue
                else:
                    if "小时前" in played_info:
                        release_time = int(re.findall(r"\d+",played_info)[1])
                        if release_time>2:
                            continue
            elif running_mode == "mix":
                if not re.search("刚刚|分钟前|小时前|天前",played_info):
                    continue
            elif running_mode == "cold":
                if not re.search("刚刚|分钟前|小时前",played_info):
                    continue
                else:
                    if "小时前" in played_info:
                        release_time = int(re.findall(r"\d+",played_info)[1])
                        if release_time>12:
                            continue
            # deduplicate for video
            if previous_urls is not None and url in previous_urls:
                print(f"video {url} existed in previous set")
                continue
            if url in in_download_urls:
                print(f"video {url} 是重复搜索结果，忽略！")
                continue
            if len(title)<5:
                print(f"标题过短:[{title}]PASS")
                continue
            # filter title by ban words and sub keys
            if re.search(TITLE_BAN_WORDS,title) or (sub_keys != "" and re.search(sub_keys,title)==None):
                continue
            # restrict video duration between 1 to 20 minutes
            duration_text = duration_list[i].find_element(By.TAG_NAME,'span').text
            duration_parse_list = duration_text.split(":")
            min_part = int(duration_parse_list[-2])
            if len(duration_parse_list)!=2:
                print(f"video {title} duration {duration_text} longer than 1 hour")
                continue
            if min_part>18:
                print(f"video {title} duration {duration_text} out of range")
                continue
            # filter channel by ban name and blacklist and youtube check
            print(f"video {title} , channel {channel} is about to check in youtube...")
            if re.search(CHANNEL_BAN_NAME,channel) or channel in CHANNEL_BLACKLIST or youtube_check_channel(driver,channel) == True:
                continue
            if youtube_check_title(driver,title) == True:
                continue
            #免下载记录
            if running_mode in ["cold","mix"]:
                with open('Shoted_urls.txt','a') as f:
                    f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+":"+title+"\n")
                    f.write(url)
                    f.write('\n')
                in_download_urls.add(url)
                with open('previous.txt','a') as f:
                    f.write(url)
                    f.write('\n')
                continue
            #解析视频真实下载地址
            real_v_url = ""
            try:
                # get real_video url on 3rd download website
                driver.switch_to.window(window_first)
                # Load balancing for 3rd download website, videoclick.cn share 1/2, videofk.com share 1/2
                website = ''
                try:
                    raise Exception("go to the second method immediately")
                    # ----------------try the first download website
                    website = 'https://www.videofk.com/index-video-download/search?url='+url
                    driver.get(website)
                    sleep(2)
                    #打开网站可能引发窗口转移，务必还原位置
                    driver.switch_to.window(window_first)
                    # input_box = driver.find_element_by_id("link")     
                    # input_box.clear()
                    # input_box.send_keys(url)
                    # driver.find_element_by_xpath("//input[@type='button']").click()
                    #广告页面弹出，务必还原位置
                    # sleep(5)
                    # driver.switch_to.window(window_first)
                    # item_a = driver.find_element_by_xpath('//*[@id="wrap"]/div[2]/div/div[1]/div/div/div/a') invalid since 2021-11-21
                    # print("current pages: "+str(driver.window_handles))
                    # print(f"current window handler is : {driver.current_window_handle}")

                    # item_a = driver.find_element_by_class_name('download')
                    item_a = driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/div/div[1]/div/div[2]/div[2]/div/a')
                    video_src = item_a.get_property("href")
                    # driver.switch_to.default_content()
                except Exception as e:
                    try:
                        print(e)
                        print(f"the FIRST download website {website} collapsed, try SELF PARSE now")
                        driver.get(url)
                        cookie_list = driver.get_cookies()
                        cookie_dic = {}
                        for cookie_item in cookie_list:
                            name = cookie_item.get("name")
                            value = cookie_item.get("value")
                            cookie_dic[name]=value
                        print("COOKIE饼干："+str(cookie_dic))
                        driver.get("https://www.ixigua.com")
                        cookie = "; ".join([str(x)+"="+str(y) for x,y in cookie_dic.items()])
                        video_src = parseXigua(url,cookie)
                    except Exception as e:
                    # ----------------try the second download website---------------------
                        print("SELF PARSE ERROR: "+e)
                        website = 'https://www.6qq.cn/xigua.html'
                        print(f"the SELF PARSE failed, try SECOND download website {website} now")
                        driver.get(website)
                        driver.switch_to.window(window_first)              
                        driver.execute_script(f"document.getElementById('url').value = '{url}'")
                        sleep(2)
                        driver.find_element(By.XPATH,'//*[@id="news"]/div[1]/fieldset/div[2]/form/li[2]/button').click()
                        sleep(3)
                        driver.switch_to.window(window_first)
                        item_source = driver.find_element(By.XPATH,'//*[@id="chakan"]')
                        video_src = item_source.get_property('href')
                        print("备用网站下载成功了")
                real_v_url = video_src.split("?")[0]
                if len(driver.window_handles)>1:
                    driver.switch_to.window(window_second)
            except Exception as e:
                # print(e)
                driver.save_screenshot('watermelon_download.png')
                print(f"terrible! all 3rd download websites error occured: {url}")
                with open('Failed_urls.txt','a') as f:
                    f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+":"+title+"\n")
                    f.write(url)
                    f.write('\n')
                # for local use
                if running_mode == "mix":
                    try:
                        # 西瓜视频解析
                        import urllib3
                        urllib3.disable_warnings()
                        import base64
                        print("I will try to parse video by myself now  :)")
                        driver.get(url)
                        cookie_list = driver.get_cookies()
                        cookie_dic = {}
                        for cookie_item in cookie_list:
                            name = cookie_item.get("name")
                            value = cookie_item.get("value")
                            cookie_dic[name]=value
                        print("COOKIE饼干："+str(cookie_dic))
                        driver.get("https://www.ixigua.com")
                        cookie = "; ".join([str(x)+"="+str(y) for x,y in cookie_dic.items()])
                        headers={
                            "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
                            "cookie":cookie
                        }
                        response = requests.get(url, verify=False, headers=headers).text
                        audioUrl=''
                        videoUrl=''
                        #分别解析视频和音频地址，通过指定开始和结束字符串进行正则匹配
                        pattern = re.compile('(?<=window._SSR_HYDRATED_DATA=).*?(?=</script>)')
                        jsonResult = pattern.findall(response)[0]
                        #解析视频地址
                        video_pattern = re.compile('(?<=1080p).*?(?=backup_url_1)')
                        videoResult = []
                        videoResult = video_pattern.findall(jsonResult)
                        if len(videoResult) >0:
                            videoResult = videoResult[0]
                        else:
                            videoResult = re.compile('(?<=720p).*?(?=backup_url_1)').findall(jsonResult)[0]
                        print("视频地址解析结果："+str(videoResult))
                        video_url_pattern = re.compile('(?<="main_url":").*?(?=",)')
                        videoUrl = video_url_pattern.findall(videoResult)[0]
                        #解析音频地址
                        audio_pattern = re.compile('(?<=dynamic_audio_list").*?(?="backup_url_1)')
                        audioResult = audio_pattern.findall(jsonResult)[0]
                        audio_url_pattern = re.compile('(?<="main_url":").*?(?=",)')
                        audioUrl = audio_url_pattern.findall(audioResult)[0]
                        video_url = base64.b64decode(videoUrl).decode('ISO-8859-1').replace(".ÓM","?")
                        audio_url = base64.b64decode(audioUrl).decode('ISO-8859-1').replace(".ÓM","?")
                        print("打印视频地址："+video_url)
                        print("打印音频地址："+audio_url)
                        #着手下载
                        print("开始下载："+title)
                        in_download_urls.add(url)
                        urllib.request.urlretrieve(video_url.split("?")[0], title+".mp4")
                        urllib.request.urlretrieve(audio_url.split("?")[0], title+".mp3")
                    except Exception as e:
                        print(e+"\nfailed url: "+url)
                    
                    #合并视频和音频
                    # import moviepy.editor
                    # start_time = datetime.now()
                    # file = title+"WIN"+".mp4"
                    # video = moviepy.editor.VideoFileClip(title+".mp4").set_fps(24)
                    # audio = moviepy.editor.AudioFileClip(title+".mp3")
                    # new_video = video.set_audio(audio)
                    # new_video.write_videofile(file)
                    # end_time = datetime.now()
                    # costed_time = (end_time-start_time).seconds
                    # # specify the dir to move downloaded video
                    # directory = os.getcwd()+"/uploading/"
                    # os.replace(os.getcwd()+"/"+file,directory+file)
                    # current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    # print(f"""merge {title} -----> {file} 
                    # costed {costed_time} seconds, timestamp:{current_timestamp},
                    # xigua_url:{url},\nsearch_key:{main_key},mode:{running_mode}""")
                    # os.remove(title+".mp4")
                    # os.remove(title+".mp3")
                    # if not os.path.isfile('./uploading/'+file):
                    #     with open('Failed_urls.txt','a') as f:
                    #         f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+":"+title+"\n")
                    #         f.write(url)
                    #         f.write('\n')
                    # else:
                    #     with open('previous.txt','a') as f:
                    #         f.write(url)
                    #         f.write('\n')
                #merge in backend
                # if video_url != "" and audio_url !="":
                #     future_tasks.append(executor.submit(merge_video,url+"WATER六MELON"+title+"WATER六MELON"+main_key))

            # download in backend        
            if real_v_url != '':
                print(f"ready to download video ========> url:{url},\nreal_video_url:{real_v_url},\nname:{title}, duration:{min_part}mins, LUCKY KEY {main_key}")
                in_download_urls.add(url)
                future_tasks.append(executor.submit(download_video,real_v_url+"WATER六MELON"+title+"WATER六MELON"+url+"WATER六MELON"+main_key+"WATER六MELON"+running_mode+"WATER六MELON"+channel))            
    except Exception as e:
        driver.save_screenshot('watermelon_items.png')
        error_msg = str(e)
        if "element not interactable" in error_msg:
            driver.save_screenshot('element_not_interactable.png')
        elif "Unable to locate element" in error_msg:
            driver.save_screenshot('Unable_to_locate_element.png')
        elif "list index out of range" in error_msg:
            driver.save_screenshot('list_index_out_of_range.png')
        elif "element is not attached" in error_msg:
            driver.save_screenshot('element_is_not_attached.png')
        elif "Timed out receiving message" in error_msg:
            driver.save_screenshot('Timed_out_receiving_message.png')
        print("process items_DIV error: " + error_msg)
        print("Search stage pages during exception: "+str(driver.window_handles))
    finally:
        # print(driver.window_handles)
        if len(driver.window_handles)>1:
            driver.switch_to.window(window_second)
        # should refresh page here especially when page crash
        driver.refresh()

# search by key word
def douyin_search(driver, main_key):
    dou_url = "https://www.douyin.com/search/{}?publish_time=7&sort_type=2&source=tab_search&type=video".format(main_key)
    driver.get(dou_url)
    sleep(5)
    driver.switch_to.window(window_second)
    items_a = driver.find_elements(By.TAG_NAME,'a')
    pattern = re.compile("https://www.douyin.com/video/[0-9]*$")
    for item in items_a:
        url = item.get_attribute("href")
        # print("在这里：", url)
        title = ''
        if url is not None and pattern.match(url):
            divs = item.find_elements(By.TAG_NAME,'div')
            for div in divs:
                texts = div.text
                for text in texts.split('\n'):
                    if text and text[0] != '@' and len(text)>len(title):
                        title = text
        if title != '' and not title[0].isdigit() and url not in in_download_urls:
            with open('Shoted_urls.txt','a') as f:
                f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+":"+title+"\n")
                f.write(url)
                f.write('\n')
                in_download_urls.add(url)
                with open('previous.txt','a') as f:
                    f.write(url)
                    f.write('\n')

# self parse xigua video
def parseXigua(url, cookie):
    pc_headers={
        "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "referer":url,
        "cookie":cookie
    }
    responseHtml = requests.get(url, headers=pc_headers, allow_redirects=True).content.decode('UTF-8')
    # 获取vid
    vid = responseHtml.split('"vid":"')[1].split('","')[0]
    # 生成签名
    parseUrl = "/video/urls/v/1/toutiao/mp4/" + vid + "?r=" + str(random.randint(1000000,9999999))
    print("parseUrl:"+parseUrl)
    crc_code = str(zlib.crc32(parseUrl.encode('utf8')))
    # 请求接口
    mResponse = requests.get("http://i.snssdk.com" + parseUrl + "&nobase64=true&s=" + crc_code, headers=pc_headers).content.decode('UTF-8')
    mJson = json.loads(mResponse)
    return mJson['data']['video_list']['video_3']['main_url']

# download the video specified by url
def download_video(video_url_and_name):
    str_list = video_url_and_name.split("WATER六MELON")
    video_url = str_list[0]
    real_video_name = str_list[1]
    xigua_url = str_list[2]
    search_key = str_list[3]
    running_mode = str_list[4]
    channel = str_list[5]
    video_name = real_video_name.replace('.','。')
    video_name = video_name.replace('-','至')
    file_name = video_name[7:10]+video_name[5:7]+search_key+video_name[3:5]+video_name[0:3]
    file = re.sub('[^\u4e00-\u9fa5]+','',file_name)
    if running_mode in ['fast','slow']:
        file = video_name+".mp4"
    elif running_mode == 'cold':
        # file = f"${search_key}$"+video_name+".mp4"
        file = video_name+f"@{channel}"+".mp4"
    elif running_mode == 'mix':
        file = f"${search_key}$"+video_name+".mp4"
    start_time = datetime.now()
    try:
        urllib.request.urlretrieve(video_url, file)
    except Exception as e:
        with open('Failed_urls.txt','a') as f:
            f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"::"+real_video_name+"\n")
            f.write(xigua_url)
            f.write('\n')
        print("URLRETRIEVE ERROR:"+video_url_and_name)
        print(e)
        return f"视频{xigua_url}下载失败"
    end_time = datetime.now()
    costed_time = (end_time-start_time).seconds
    # specify the dir to move downloaded video
    directory = os.getcwd()+"/uploading/"
    os.replace(os.getcwd()+"/"+file,directory+file)
    current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"""download {video_name} -----> {file} 
    costed {costed_time} seconds, timestamp:{current_timestamp},
    xigua_url:{xigua_url},\nsearch_key:{search_key},mode:{running_mode}""")
    with open('previous.txt','a') as f:
        f.write(xigua_url)
        f.write('\n')

# clear browser cache to speed up processing
def clear_cache(driver):
    driver.switch_to.window(window_first)
    driver.get('chrome://settings/clearBrowserData')
    driver.switch_to.window(window_first)
    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB * 2 + Keys.ENTER)
    sleep(1)
    actions.perform()
    actions.send_keys(Keys.DOWN * 4 + Keys.ENTER)
    sleep(1)
    actions.perform()
    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB * 5 + Keys.ENTER) # confirm
    sleep(2)
    actions.perform()
    driver.switch_to.window(window_second)

# slice dictionary
def dict_slice(adict, start, end):
    keys = adict.keys()
    slice_dict = {}
    for k in list(keys)[start:end]:
        slice_dict[k] = adict[k]
    return slice_dict

if __name__ == "__main__":
    print(f"execute program {sys.argv[0]} now!")
    init_time = datetime.now()
    print(" TASK INIT TIME IS : " +  init_time.strftime('%Y-%m-%d %H:%M:%S'))
    if len(sys.argv) != 2:
        # fast and slow mode for production environment, mix mode for local test
        print("please type running mode: fast slow mix cold fire")
        sys.exit()
    running_mode = sys.argv[1]
    previous_urls = None
    if os.path.isfile('./previous.txt'):
        previous_urls = set(line.strip() for line in open('previous.txt'))
        if running_mode == "cold" and os.path.isfile('./previous_racknerd.txt'):
            racknerd_urls = set(line.strip() for line in open('previous_racknerd.txt'))
            previous_urls = previous_urls.union(racknerd_urls)
    # create a set to de-duplicate for videos
    in_download_urls = set()
    try:
        # open display to avoid headless running
        from pyvirtualdisplay import Display
        disp = Display(visible=0, size=(1920,1080)).start()
        chrome_options = uc.ChromeOptions()
        chrome_options.headless = False
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument('--disable-javascript')
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        chrome_options.add_argument('--hide-scrollbars')
        # 将window.navigator.webdriver特征值去除
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        # setting no-sandbox for headless mode or cli-server without real screen
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        # settings for prod environment , specify port and browser
        chrome_options.add_argument('--remote-debugging-port=9222')
        chrome_options.binary_location = "/snap/bin/chromium"
        driver = uc.Chrome(executable_path="/usr/bin/chromedriver",options=chrome_options,version_main=128)
        # anti-crawlerdetection
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",{
            "source":"""
                Object.defineProperty(navigator,'webdriver',{
                    get: () => undefined
                    })
            """
        })
        driver.set_page_load_timeout(518) 
        driver.implicitly_wait(15)
        # open ixigua front page
        driver.get('https://www.ixigua.com')
        # execute by 
        # disp = Display(visible=0, size=(1920,1080)).start()multi-thread
        executor = ThreadPoolExecutor(max_workers=3)
        future_tasks = []
        if running_mode == 'slow':
            SEARCH_KEY_DICT = SEARCH_KEY_DICT_SLOW
        elif running_mode == 'mix':
            SEARCH_KEY_DICT.update(SEARCH_KEY_DICT_SLOW)
            SEARCH_KEY_DICT.update(SEARCH_KEY_DICT_COLD)
        elif running_mode == 'cold':
            hour_part = datetime.now().hour
            count_number = hour_part%6
            amount = len(SEARCH_KEY_DICT_COLD)
            unit_amount = int(amount/6)
            print(f"current cold keys total amount is {amount}, unit amount is {unit_amount}")
            if count_number != 5:
                start = count_number*unit_amount
                end = (count_number+1)*unit_amount
            else:
                start = 5*unit_amount
                end = amount
            print(f"sliced cold keys from {start} to {end}")
            SEARCH_KEY_DICT = dict_slice(SEARCH_KEY_DICT_COLD,start,end)
        # iterite SEARCH KEYS to target object
        key_counter = 1 
        for k,v in SEARCH_KEY_DICT.items():
            # if key_counter%5 == 0:
            #     clear_cache(driver)
            print(f"PROCESS THE {key_counter}th KEY: " + k)
            xigua_search(driver,k,v,previous_urls,in_download_urls,future_tasks,executor,running_mode)
            if running_mode in ['cold','mix']:
                try:
                    douyin_search(driver,k)
                    # pass
                except Exception as douyin_error:
                    print("DOUYIN ERROR: ",douyin_error)
                # print("do nothing in doyin***************************************************************")
            key_counter = key_counter+1
        print(future_tasks)
        wait(future_tasks,return_when=ALL_COMPLETED)
    except Exception as e:
        print("serious error occured:")
        print(e)
        driver.save_screenshot('watermelon_error.png')
    finally:
        print(f"window first:{window_first}, window second:{window_second}")
        print("final pages: "+str(driver.window_handles))
        driver.save_screenshot('watermelon_final.png')
        # clear cache before quit
        clear_cache(driver)
        quit_time = datetime.now()
        print("CHROMEDRIVER QUIT TIME IS : " +  quit_time.strftime('%Y-%m-%d %H:%M:%S'))
        chrome_time = (quit_time-init_time).seconds
        print(f"chrome total-running-time is {chrome_time} seconds")
        print("in_download_urls: "+str(in_download_urls))
        driver.quit()
        disp.stop()
