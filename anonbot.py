import telebot
import os
import sqlite3
import time
import random
from decimal import Decimal, ROUND_HALF_UP
import threading
import schedule

dir = "/path/to/directory"
bot_token = "your_bot_token"
monitor_group_id = "monitor_group_id"

bot = telebot.TeleBot(bot_token, parse_mode=None, num_threads=10)
btn = telebot.types.InlineKeyboardButton
escape = telebot.formatting.escape_markdown
os.makedirs(dir,exist_ok=True)

lang = {
    "en":{
        "welcome":"Hey there! I'm your message mule. I can connect you and an another person with a thin red line, So you'll have a super private chat. From now let's go with the name *{anon_name}* for now. Click /match and have fun chatting!",
        "welcome_again":"Welcome back *{anon_name}*. What's up. Wanna change your gender?",
        "gender_ask":"Now. Tell me are you a man?",
        "male":"Yes. I'm a male",
        "female":"No. I'm a female",
        "alldone":"All done.",
        "notbond":"You're not bond with anyone right now. Please /match and bond with someone first.",
        "bond_msg":"`{bonder}` {flag}{active_notification}\n`Reputation: {soulmate_score}`\nHas bonded with you. Now you can chat with him or her.\nSupported: text, video, photo, gif, voice, sticker, round video",
        "bond_nofound":"Unfortunately, Didn't found any matchable person for you. Poor thing. Maybe try again later.",
        "searching":"Searching a match for you...",
        "bond_already":"You're already bonded with *{soulmate}*",
        "cutbond":"`{anon_name}` Cut the bondation with you. Sad...",
        "bondrate":"What do you think about `{anon_name}`, rate him.",
        "he_cool":"😊He's cool.",
        "he_nocool":"😡He's not cool.",
        "bond_like":"You liked him. Hope you can match him again next time.",
        "bond_dislike":"Let's hope not going to match this guy again.😆",
        "disbond_msg":"Are you sure disconnect the bondation with `{soulmate_anonname}` ?",
        "disbond_confirm":"Yup. Just disconnect",
        "disbond_keep":"No. Keep connect",
        "disbond_success":"You're successfully disconnected with {soulmate_anonname}.",
        "disbond_cancel":"You canceled it. Yey.",
        "info_msg":"`{anon_name}`\n*Reputation:* {stars}\n*Total match:* {total_match_personal}\n*Join time:* {join_time} days ago.{current_match}\n\n`Server Information`\n*Total users:* {total_users}\n*Banned users:* {banned_users}\n*Total match:* {total_match}\n*Matchable users:* {matchable_users}",
        "current_match":"\n*Current match:* `{soulmate_anonname}`",
        "last_match":"\n*Last match:* `{soulmate_anonname}`",
        "banned_bot":"*{anon_name}* left the match.",
        "youre_banned":"`System: You're banned from sending Media.`",
        "hes_banned":"`System: {sender_anonname} is banned from sending Media.`",
        "active_before_sec":"secs ago",
        "active_before_min":"minutes ago",
        "active_before_hour":"hours ago",
        "active_before_day":"days ago",
        "active_notification":"_🕓 Online {tail} {active_before}_",
        "deactive_notification":"{anon_name} is not talking to you for two days. You should disbond the connection with him."
    },
    "zh":{
        "welcome":"你好！我是你的消息小骡子，我的工作就是来回传达你的消息和别人发给你的消息。我用月老的红线将你和别的匿名人士绑定起来，让你们聊个够。全过程匿名，现在起我给你起个名字就叫 *{anon_name}* 吧。点击 /match 开始匹配吧",
        "welcome_again":"哈喽！欢迎回来 *{anon_name}*，你是想更改性别吗？",
        "gender_ask":"告诉我你是个男人吗？",
        "male":"我是纯爷们儿",
        "female":"人家是小公举",
        "alldone":"设置完毕",
        "notbond":"你还没有与任何人匹配呢。点击 /match 开始匹配吧",
        "bond_msg":"`{bonder}` {flag}{active_notification}\n`声望: {soulmate_score}`\n他与你连接上了，你们可以聊了.\n支持发送文字、视频、照片、动图、语音、贴纸、圆视频哦",
        "bond_nofound":"可悲啊，没有找到能与你匹配的人，稍后再试吧",
        "searching":"正在为你匹配中...",
        "bond_already":"你当前已经与 *{soulmate}* 匹配着呢",
        "cutbond":"`{anon_name}` 切断了与你的连线，惨啊",
        "bondrate":"你觉得 `{anon_name}` 怎么样？给他打分吧",
        "he_cool":"😊他不错呢",
        "he_nocool":"😡这人没劲",
        "bond_like":"看来你挺喜欢他的，期待下次还能匹配到他",
        "bond_dislike":"哈，希望下次别再匹配到他😆",
        "disbond_msg":"你确定要和 `{soulmate_anonname}` 切断连线吗？",
        "disbond_success":"你成功切断了与 {soulmate_anonname} 的连线",
        "disbond_confirm":"是的,我确定",
        "disbond_keep":"不了，我在跟他聊聊",
        "disbond_cancel":"哈，就知道你舍不得",
        "info_msg":"`{anon_name}`\n*声望：* {stars}\n*总共匹配：* {total_match_personal}\n*注册时间：* {join_time} 天前{current_match}\n\n`系统信息`\n*总用户数：* {total_users}\n*封禁用户：* {banned_users}\n*总匹配数：* {total_match} 次\n*可匹配用户：* {matchable_users}",
        "current_match":"\n*当前匹配：* `{soulmate_anonname}`",
        "last_match":"\n*上次匹配：* `{soulmate_anonname}`",
        "banned_bot":"*{anon_name}* 断开了连线",
        "youre_banned":"`系统消息： 你已被禁止发送媒体`",
        "hes_banned":"`系统消息： {sender_anonname} 已被禁止发送媒体`",
        "active_before_sec":"秒前在线",
        "active_before_min":"分钟前在线",
        "active_before_hour":"小时前在线",
        "active_before_day":"天前在线",
        "active_notification":"_🕓 {active_before} {tail}_",
        "deactive_notification":"{anon_name} 已经两天不理你了呢，这边建议你跟他解除连接呢，亲"
    }
}

db_path = f"{dir}/anonbot.db"

def db_execute(query,params=None):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query,params) if params else cursor.execute(query)
        conn.commit()

def db_select(query,params=None,fetch=0):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query,params) if params else cursor.execute(query)
    try:
        result = cursor.fetchone() if fetch == 0 else cursor.fetchall()
    except:
        result = None
    return result

if not os.path.exists(db_path):
    query = "CREATE TABLE users (id INTEGER PRIMARY KEY,user_id INTEGER,full_name TEXT,username TEXT,anon_name INTEGER,gender INTEGER,lang TEXT,is_admin INTEGER,is_banned INTEGER,soulmate_id INTEGER,chatwith_count INTEGER,chat_count INTEGER,like INTEGER,dislike INTEGER,last_seen INTEGER,last_talkwith INTEGER,timestamp INTEGER)"
    db_execute(query)
    query = "CREATE TABLE messages (id INTEGER PRIMARY KEY,user_id INTEGER,text TEXT,file_id TEXT,file_type TEXT,msg_id INTEGER,reply_id INTEGER,chat_room TEXT,soulmate_id INTEGER,timestamp INTEGER)"
    db_execute(query)

def logging(event):
    now = time.time()
    local_time = time.localtime(now)
    date_str = time.strftime("%Y-%m-%d %H:%M:%S", local_time)

    event = f"[{date_str}] {event}"
    log_event = f"{event}\n"
    log_file = f"{dir}/anonbot.log"
    with open(log_file, "a") as f:
        f.write(log_event)
    print(f"{event}")

def adduser(message):
    user_id = message.from_user.id
    lang_code = message.from_user.language_code
    first_name = message.from_user.first_name or ""
    last_name = message.from_user.last_name or ""
    full_name = f"{first_name} {last_name}" if last_name else first_name
    username = message.from_user.username
    timestamp = int(time.time())
    new_user = False

    try:
        anon_name,_ = db_select("SELECT anon_name, timestamp FROM users WHERE user_id=?",(user_id,))
    except:
        anon_name = None

    if not anon_name:
        while True:
            random_num = random.randint(1,9999)
            try:
                anon_name,_ = db_select("SELECT anon_name, timestamp FROM users WHERE anon_name=?",(random_num,))
            except:
                anon_name = None
            if not anon_name:
                anon_name = random_num
                db_execute("INSERT INTO users (user_id,full_name,username,anon_name,lang,timestamp,last_seen) VALUES (?,?,?,?,?,?,?)",(user_id,full_name,username,anon_name,lang_code,timestamp,timestamp))
                logging(f"Anon{anon_name} 新加入")
                break
        new_user = True
    else:
        db_execute("UPDATE users SET full_name=?,username=?,lang=?,last_seen=? WHERE user_id=?",(full_name,username,lang_code,timestamp,user_id))
    return new_user

def gettext(lang_code = "zh",keyword=None):
    lang_code = "zh" if lang_code.startswith("zh") else "en"
    if keyword:
        text = lang[lang_code][f"{keyword}"]
        return text

def dbgetlang(user_id):
    try:
        lang,_ = db_select("SELECT COALESCE(lang,'en'),timestamp FROM users WHERE user_id=?",(user_id,))
    except:
        lang = "en"
    return lang

def getflag(user_id):
    lang,_ = db_select("SELECT COALESCE(lang,'unknown'),timestamp FROM users WHERE user_id=?",(user_id,))
    if lang.startswith("vi"):
        flag = "🇻🇳"
    else:
        flag = ""
    return flag

@bot.callback_query_handler(func=lambda call: call.data.startswith("monitor_"))
def start_command(call):
    user_id = call.message.chat.id
    msg_id = call.message.message_id
    command = call.data.split("_")[1]
    target_uid = call.data.split("_")[2]
    file_type = call.data.split("_")[3]

    if command == "ban":
        sender_uid,_ = db_select("SELECT soulmate_id,timestamp FROM users WHERE user_id=?",(target_uid,))
        db_execute("UPDATE users SET is_banned=1 WHERE user_id=?",(sender_uid,))
        edit_message(user_id,"Sender is banned from sending media.",msg_id,file_type)

        langcode = dbgetlang(sender_uid)
        text = gettext(langcode,"youre_banned")
        send_message(sender_uid,text)

        sender_anonname = get_anonname(sender_uid)
        langcode = dbgetlang(target_uid)
        text = gettext(langcode,"hes_banned").format(sender_anonname=sender_anonname)
        send_message(target_uid,text)
        logging(f"{sender_anonname} 被封禁")
    else:
        edit_message(user_id,"Canceled dealing with.",msg_id,file_type)

def send_message(user_id,text,file=None,file_id=None,file_type=None,reply_id=None,protect=False,reply_markup=None,parse_mode="MARKDOWN"):

    markup = telebot.types.InlineKeyboardMarkup()
    btn_ban = btn("Ban sender",callback_data=f"monitor_ban_{user_id}_{file_type}")
    btn_cancel = btn("Cancel",callback_data=f"monitor_cancel_{user_id}_{file_type}")
    markup.add(btn_ban,btn_cancel)
    try:
        is_banned,_ = db_select("SELECT is_banned,timestamp FROM users WHERE soulmate_id=?",(user_id,))
    except:
        is_banned=None
    msg_id = None

    try:
        if not file:
            msg_id = bot.send_message(user_id,text,parse_mode=parse_mode,reply_to_message_id=reply_id,protect_content=protect,reply_markup=reply_markup).message_id
        elif file and not is_banned:
            if file_type=="video":
                msg_id = bot.send_video(user_id,file_id,caption=text,parse_mode=parse_mode,reply_to_message_id=reply_id,protect_content=protect,reply_markup=reply_markup).message_id
                bot.send_video(monitor_group_id,file_id,caption=text,parse_mode=parse_mode,reply_markup=markup)
            elif file_type=="audio":
                msg_id = bot.send_audio(user_id,file_id,caption=text,parse_mode=parse_mode,reply_to_message_id=reply_id,protect_content=protect,reply_markup=reply_markup).message_id
                bot.send_audio(monitor_group_id,file_id,caption=text,parse_mode=parse_mode,reply_markup=markup)
            elif file_type=="video_note":
                msg_id = bot.send_video_note(user_id,file_id,reply_to_message_id=reply_id,protect_content=protect,reply_markup=reply_markup).message_id
                bot.send_video_note(monitor_group_id,file_id,reply_markup=markup)
            elif file_type=="animation":
                msg_id = bot.send_animation(user_id,file_id,caption=text,parse_mode=parse_mode,reply_to_message_id=reply_id,protect_content=protect,reply_markup=reply_markup).message_id
                bot.send_animation(monitor_group_id,file_id,caption=text,parse_mode=parse_mode,reply_markup=markup)
            elif file_type=="photo":
                msg_id = bot.send_photo(user_id,file_id,caption=text,parse_mode=parse_mode,reply_to_message_id=reply_id,protect_content=protect,reply_markup=reply_markup).message_id
                bot.send_photo(monitor_group_id,file_id,caption=text,parse_mode=parse_mode,reply_markup=markup)
            elif file_type=="document":
                msg_id = bot.send_document(user_id,file_id,caption=text,parse_mode=parse_mode,reply_to_message_id=reply_id,protect_content=protect,reply_markup=reply_markup).message_id
                bot.send_document(monitor_group_id,file_id,caption=text,parse_mode=parse_mode,reply_markup=markup)
            elif file_type=="voice":
                msg_id = bot.send_voice(user_id,file_id,caption=text,parse_mode=parse_mode,reply_to_message_id=reply_id,protect_content=protect,reply_markup=reply_markup).message_id
            elif file_type=="sticker":
                msg_id = bot.send_sticker(user_id,file_id,reply_to_message_id=reply_id,protect_content=protect,reply_markup=reply_markup).message_id
            else:
                print("trying to send unsupported content.")
                msg_id = None
    except telebot.apihelper.ApiTelegramException as e:
        anon_name = get_anonname(user_id)
        if "bot was blocked by the user" in e.result.text:
            soulmate_id,_ = db_select("SELECT soulmate_id,timestamp FROM users WHERE user_id=?",(user_id,))
            lang_code = dbgetlang(soulmate_id)
            text = gettext(lang_code,"banned_bot").format(anon_name=anon_name)
            send_message(soulmate_id,f"{anon_name} left the match.")
            db_execute("UPDATE users SET soulmate_id=99999999 WHERE user_id=?",(user_id,))
            db_execute("UPDATE users SET soulmate_id=NULL WHERE soulmate_id=?",(user_id,))

            transfer_id = user_id
            markup = telebot.types.InlineKeyboardMarkup()
            text_btn_cool = gettext(lang_code,"he_cool")
            text_btn_nocool = gettext(lang_code,"he_nocool")
            btn_like = btn(text_btn_cool,callback_data=f"rate_like_{transfer_id}")
            btn_dislike = btn(text_btn_nocool,callback_data=f"rate_dislike_{transfer_id}")
            markup.add(btn_like,btn_dislike)

            text = gettext(lang_code,"bondrate").format(anon_name=anon_name)
            send_message(soulmate_id,text,reply_markup=markup)
            logging(f"{anon_name} 封禁了机器人，因此被系统标记")
        else:
            logging(f"向 {anon_name} 发送消息发生奇怪的错误：{e.result.text}")
    return msg_id

def get_filestatus(message):
    if message:
        if message.content_type == "text":
            file_id = None
            file_type = None
            file = False
            text = message.text
        elif message.content_type == "video":
            file_id = message.video.file_id
            file_type = "video"
            text = message.caption or ""
        elif message.content_type == "photo":
            file_id = message.photo[-1].file_id
            file_type = "photo"
            text = message.caption or ""
        elif message.content_type == "document":
            file_id = message.document.file_id
            file_type = "document"
            text = message.caption
        elif message.content_type == "video_note":
            file_id = message.video_note.file_id
            file_type = "video_note"
            text = message.caption or ""
        elif message.content_type == "audio":
            file_id = message.audio.file_id
            file_type = "audio"
            text = message.caption or ""
        elif message.content_type == "voice":
            file_id = message.voice.file_id
            file_type = "voice"
            text = message.caption or ""
        elif message.content_type == "animation":
            file_id = message.animation.file_id
            file_type = "animation"
            text = message.caption or ""
        elif message.content_type == "sticker":
            file_id = message.sticker.file_id
            file_type = "sticker"
            text = message.caption or ""
        
        if message.reply_to_message:
            user_id = message.from_user.id
            msg_uid = message.reply_to_message.from_user.id
            msg_id = message.reply_to_message.message_id
            if user_id == msg_uid:
                reply_id,_ = db_select("SELECT reply_id,timestamp FROM messages WHERE msg_id=?",(msg_id,))
            else:
                reply_id,_ = db_select("SELECT msg_id,timestamp FROM messages WHERE reply_id=?",(msg_id,))
        else:
            reply_id = None
    file = True if file_type else False
    return text,file,file_id,file_type,reply_id

def edit_message(user_id,text,msg_id,file_type=None,reply_markup=None,parse_mode="MARKDOWN"):
    try:
        if not file_type:
            msg_id = bot.edit_message_text(text,user_id,msg_id,parse_mode=parse_mode,reply_markup=reply_markup).message_id
        elif file_type:
            msg_id = bot.edit_message_caption(text,user_id,msg_id,parse_mode=parse_mode,reply_markup=reply_markup).message_id
    except:
        pass
    return msg_id

def get_anonname(user_id):
    try:
        anon_num,gender,is_admin,is_banned,timestamp,chat_count = db_select("SELECT anon_name,gender,is_admin,is_banned,timestamp,COALESCE(chat_count,0) FROM users WHERE user_id=?",(user_id,))
        gender = gender or 3
        is_admin = is_admin or False
        is_banned = is_banned or False
        if is_banned:
            avatar = "🤡"
        elif is_admin and gender == 1:
            avatar = "🐭"
        elif is_admin and gender == 2:
            avatar = "🐹"
        elif is_admin and gender == 3:
            avatar = "🐶"
        elif gender == 1:
            avatar = "👨"
        elif gender == 2:
            avatar = "👩"
        else:
            avatar = "🧔‍♀️"
        if timestamp <= int(time.time()) - 48*60*60 and chat_count == 0:
            avatar = "☠️"
    except:
        avatar = "🤡"
        anon_num = 9527
    anon_name = f"{avatar}Anon{anon_num}"

    return anon_name

def get_rating(user_id):
    like,dislike = db_select("SELECT COALESCE(like,1),COALESCE(dislike,1) FROM users WHERE user_id=?",(user_id,))
    total_rating = like + dislike
    like_percentage = (like / total_rating) * 100
    rating = (like_percentage / 100) * 5
    rating = Decimal(rating)
    rating = int(rating.quantize(Decimal('1'),rounding=ROUND_HALF_UP))
    star = []
    for i in range(rating):
        star.append("🌕")
    for i in range(5 - rating):
        star.append("🌑")
    stars = "".join(star)
    return stars

@bot.callback_query_handler(func=lambda call: call.data.startswith("start_"))
def start_command(call):
    user_id = call.message.chat.id
    msg_id = call.message.message_id
    lang_code = dbgetlang(user_id)
    command = call.data.split("_")[1]
    gender = 2 if command == "female" else 1
    db_execute("UPDATE users SET gender=? WHERE user_id=?",(gender,user_id))
    text = gettext(lang_code,"alldone")
    edit_message(user_id,text,msg_id)

@bot.message_handler(commands=["start"])
def handle_start(message):
    user_id = message.from_user.id
    lang_code = message.from_user.language_code
    is_private = True if not message.chat.title else False
    if is_private:
        new_user = adduser(message)
        anon_name = get_anonname(user_id)
        if new_user:
            text = gettext(lang_code,"welcome").format(anon_name=anon_name)
            logging(f"新增一个用户 {anon_name} 点了 /start")
        else:
            text = gettext(lang_code,"welcome_again").format(anon_name=anon_name)
            logging(f"{anon_name} 又点了一次 /start")
        send_message(user_id,text)

        markup = telebot.types.InlineKeyboardMarkup()
        text_male = gettext(lang_code,"male")
        text_female = gettext(lang_code,"female")
        btn_male = btn(text_male, callback_data="start_male")
        btn_female = btn(text_female, callback_data="start_female")
        markup.add(btn_male)
        markup.add(btn_female)
        text = gettext(lang_code,"gender_ask")
        send_message(user_id,text,reply_markup=markup)

@bot.message_handler(commands=["match"])
def handle_match(message):
    user_id = message.from_user.id
    lang_code = message.from_user.language_code
    is_private = True if not message.chat.title else False
    timestamp = int(time.time())
    adduser(message)
    if is_private:
        text = gettext(lang_code,"searching")
        edit_later = send_message(user_id,text)
        db_execute("UPDATE users SET last_seen=? WHERE user_id=?",(timestamp,user_id))
        soulmate_id,_ = db_select("SELECT soulmate_id,timestamp FROM users WHERE user_id=?",(user_id,)) or None

        if not soulmate_id or soulmate_id == 99999999:
            is_success = True
            num = 0
            while True:
                time_limit = timestamp - 60*5*(num+1)
                try:
                    soulmate_ids = db_select("SELECT user_id,last_seen FROM users WHERE (user_id IS NOT ? AND last_talkwith IS NOT ?) AND (soulmate_id IS NULL AND soulmate_id IS NOT 99999999 AND last_seen >= ?) ORDER BY last_seen DESC LIMIT 5",(user_id,user_id,time_limit),1)
                    soulmate_id,last_seen = random.choice(soulmate_ids)
                    bonder = get_anonname(user_id)
                    soulmate_score = get_rating(user_id)
                    soulmate_lang = dbgetlang(soulmate_id)
                    flag = getflag(user_id)
                    text = gettext(soulmate_lang,"bond_msg").format(bonder=bonder,flag=flag,soulmate_score=soulmate_score,active_notification="")
                    try:
                        pinit = send_message(soulmate_id,text)
                        bot.pin_chat_message(soulmate_id,pinit)
                        break
                    except:
                        db_execute("UPDATE users SET soulmate_id=99999999 WHERE user_id=?",(soulmate_id,))
                        db_execute("UPDATE users SET soulmate_id=NULL WHERE soulmate_id=?",(soulmate_id,))
                        continue
                except:
                    num += 1
                    if num >= 100:
                        text = gettext(lang_code,"bond_nofound")
                        edit_message(user_id,text,edit_later)
                        is_success = False
                        break
                    continue

            if is_success:
                active_before_second = int(time.time()) - last_seen
                if active_before_second <= 60:
                    active_before = active_before_second
                    tail = gettext(lang_code,"active_before_sec")
                elif active_before_second <= 60*60:
                    active_before = round(active_before_second/60)
                    tail = gettext(lang_code,"active_before_min")
                elif active_before_second <= 60*60*24:
                    active_before = round(active_before_second/60/60)
                    tail = gettext(lang_code,"active_before_hour")
                else:
                    active_before = round(active_before_second/60/60/24)
                    tail = gettext(lang_code,"active_before_day")

                active_notification = gettext(lang_code,"active_notification").format(active_before=active_before,tail=tail)

                db_execute("UPDATE users SET soulmate_id=?,last_talkwith=?,chatwith_count=COALESCE(chatwith_count,0)+1 WHERE user_id=?",(soulmate_id,soulmate_id,user_id))
                db_execute("UPDATE users SET soulmate_id=?,last_talkwith=? WHERE user_id=?",(user_id,user_id,soulmate_id))
                soulmate = get_anonname(soulmate_id)
                soulmate_score = get_rating(soulmate_id)
                text = gettext(lang_code,"bond_msg").format(bonder=soulmate,flag=getflag(soulmate_id),soulmate_score=soulmate_score,active_notification=active_notification)
                try:
                    pinit = edit_message(user_id,text,edit_later)
                    bot.pin_chat_message(user_id,pinit)
                    logging(f"{bonder} 与 {soulmate} 开始了配对")

                except:
                    pass
        else:
            soulmate = get_anonname(soulmate_id)
            text = gettext(lang_code,"bond_already").format(soulmate=soulmate)
            edit_message(user_id,text,edit_later)

@bot.callback_query_handler(func=lambda call: call.data.startswith("rate_"))
def dismatch_command(call):
    user_id = call.message.chat.id
    msg_id = call.message.message_id
    lang_code = dbgetlang(user_id)
    command = call.data.split("_")[1]
    soulmate_id = call.data.split("_")[2]
    if command == "like":
        db_execute("UPDATE users SET like=COALESCE(like,0)+1 WHERE user_id=?",(soulmate_id,))
        text = gettext(lang_code,"bond_like")
        edit_message(user_id,text,msg_id)
    else:
        db_execute("UPDATE users SET dislike=COALESCE(dislike,0)+1 WHERE user_id=?",(soulmate_id,))
        text = gettext(lang_code,"bond_dislike")
        edit_message(user_id,text,msg_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("dismatch_"))
def dismatch_command(call):
    user_id = call.message.chat.id
    msg_id = call.message.message_id
    lang_code = dbgetlang(user_id)
    command = call.data.split("_")[1]
    timestamp = int(time.time())
    if command == "yes":
        soulmate_id,_ = db_select("SELECT soulmate_id,timestamp FROM users WHERE user_id=?",(user_id,))
        db_execute("UPDATE users SET soulmate_id=NULL WHERE user_id=?",(user_id,))
        db_execute("UPDATE users SET soulmate_id=NULL WHERE user_id=?",(soulmate_id,))

        soulmate_anonname = get_anonname(soulmate_id)
        text = gettext(lang_code,"disbond_success").format(soulmate_anonname=soulmate_anonname)
        edit_message(user_id,text,msg_id)

        anon_name = get_anonname(user_id)
        soulmate_lang = dbgetlang(soulmate_id)
        text = gettext(soulmate_lang,"cutbond").format(anon_name=anon_name)
        send_message(soulmate_id,text)

        bot.unpin_all_chat_messages(user_id)
        bot.unpin_all_chat_messages(soulmate_id)

        logging(f"{anon_name} 解除了 {soulmate_anonname} 的配对")

        transfer_id = soulmate_id
        markup = telebot.types.InlineKeyboardMarkup()
        text_btn_cool = gettext(lang_code,"he_cool")
        text_btn_nocool = gettext(lang_code,"he_nocool")
        btn_like = btn(text_btn_cool,callback_data=f"rate_like_{transfer_id}")
        btn_dislike = btn(text_btn_nocool,callback_data=f"rate_dislike_{transfer_id}")
        markup.add(btn_like,btn_dislike)
        text = gettext(lang_code,"bondrate").format(anon_name=soulmate_anonname)
        send_message(user_id,text,reply_markup=markup)
        db_execute("UPDATE users SET last_seen=? WHERE user_id=?",(timestamp,user_id))

        time.sleep(1)

        transfer_id = user_id
        soulmate_lang = dbgetlang(soulmate_id)
        text = gettext(soulmate_lang,"bondrate").format(anon_name=anon_name)
        send_message(soulmate_id,text,reply_markup=markup)
        db_execute("UPDATE users SET last_seen=? WHERE user_id=?",(timestamp,soulmate_id))
    else:
        text = gettext(lang_code,"disbond_cancel")
        edit_message(user_id,text,msg_id)

@bot.message_handler(commands=["info"])
def handle_dismatch(message):
    user_id = message.from_user.id
    lang_code = message.from_user.language_code
    anon_name = get_anonname(user_id)
    now = int(time.time())
    stars = get_rating(user_id)
    total_users,_ = db_select("SELECT max(id),timestamp FROM users")
    banned_users,_ = db_select("SELECT count(user_id),timestamp FROM users WHERE is_banned > 0 OR soulmate_id = 99999999")
    total_match,_ = db_select("SELECT sum(chatwith_count),timestamp FROM users")
    matchable_users,_ = db_select("SELECT count(user_id),timestamp FROM users WHERE soulmate_id IS NULL")
    total_match_personal,join_timestamp,soulmate_id,last_talkwith = db_select("SELECT chatwith_count,timestamp,soulmate_id,last_talkwith FROM users WHERE user_id=?",(user_id,))
    join_time = round((now - join_timestamp)/60/60/24)
    if soulmate_id:
        soulmate_anonname = get_anonname(soulmate_id)
        current_match = gettext(lang_code,"current_match").format(soulmate_anonname=soulmate_anonname)
    elif last_talkwith:
        soulmate_anonname = get_anonname(last_talkwith)
        current_match = gettext(lang_code,"last_match").format(soulmate_anonname=soulmate_anonname)
    else:
        current_match = ""

    text = gettext(lang_code,"info_msg").format(anon_name=anon_name,stars=stars,total_match_personal=total_match_personal,join_time=join_time,current_match=current_match,total_users=total_users,banned_users=banned_users,total_match=total_match,matchable_users=matchable_users)
    send_message(user_id,text)

    event = f"{anon_name} 查看了 /info"
    logging(event)

# For testing purpose
# @bot.message_handler(commands=["deactive"])
# def handle_dismatch(message):
#     auto_disbond()

def auto_disbond():
    time_before = int(time.time()) - 48 * 60 * 60
    deactive_users = db_select("SELECT user_id,soulmate_id FROM users WHERE last_seen <= ? AND soulmate_id IS NOT NULL AND soulmate_id != 99999999",(time_before,),1)
    num = 0
    for deactive_user in deactive_users:
        user_id,soulmate_id = deactive_user
        num += 1
        anon_name = get_anonname(user_id)
        text = gettext(dbgetlang(soulmate_id),"deactive_notification").format(anon_name=anon_name)
        send_message(soulmate_id,text)
        dismatch(soulmate_id)
        soulmate_anonname = get_anonname(soulmate_id)
        event = f"因为两天不活跃，向 {soulmate_anonname} 建议了解除与 {anon_name} 的链接"
        logging(event)

def dismatch(user_id, lang_code=None):
    lang_code = dbgetlang(user_id) if not lang_code else lang_code
    markup = telebot.types.InlineKeyboardMarkup()
    text_disbond = gettext(lang_code,"disbond_confirm")
    text_keep = gettext(lang_code,"disbond_keep")
    btn_dismatch = btn(text_disbond,callback_data="dismatch_yes")
    btn_cancel = btn(text_keep,callback_data="dismatch_no")
    markup.add(btn_dismatch)
    markup.add(btn_cancel)
    try:
        soulmate_id,_ = db_select("SELECT soulmate_id,timestamp FROM users WHERE user_id=?",(user_id,))
        soulmate_anonname = get_anonname(soulmate_id)
        text = gettext(lang_code,"disbond_msg").format(soulmate_anonname=soulmate_anonname)
        send_message(user_id,text,reply_markup=markup)
    except:
        text = gettext(lang_code,"notbond")
        send_message(user_id,text)

@bot.message_handler(commands=["dismatch","disconnect","leave"])
def handle_dismatch(message):
    user_id = message.from_user.id
    lang_code = message.from_user.language_code
    
    dismatch(user_id,lang_code)

@bot.edited_message_handler(content_types=["text","video","photo","document","video_note","audio","voice","animation","sticker"],func=lambda message:message.chat.type in ["private"])
def handle_edited_message(message):
    user_id = message.from_user.id
    msg_id = message.message_id
    if message.text:
        text = message.text
        file = None
    else:
        text = message.caption
        file = True
    try:
        reply_id,soulmate_id,_ = db_select("SELECT reply_id,soulmate_id,max(timestamp) FROM messages WHERE msg_id=?",(msg_id,))
        db_execute("UPDATE messages SET text=? WHERE msg_id=?",(text,msg_id))
    except:
        msg_id = None
    if msg_id:
        edit_message(soulmate_id,text,reply_id,file)
        sender = get_anonname(user_id)
        soulmate_anon = get_anonname(soulmate_id)
        event = f"{sender} 对 {soulmate_anon} 修改了文本：{text}"
        logging(event)
    else:
        pass

@bot.message_handler(content_types=["text","video","photo","document","video_note","audio","voice","animation","sticker"],func=lambda message:message.chat.type in ["private"])
def handle_messages(message):
    user_id = message.from_user.id
    lang_code = message.from_user.language_code
    adduser(message)
    timestamp = int(time.time())

    try:
        soulmate_id,_ = db_select("SELECT soulmate_id,timestamp FROM users WHERE user_id=?",(user_id,))
    except:
        soulmate_id = None
    if soulmate_id:
        text,file,file_id,file_type,reply_id = get_filestatus(message)

        send_id = send_message(soulmate_id,text,file,file_id,file_type,reply_id,parse_mode=None)
        db_execute("INSERT INTO messages (user_id,text,file_id,file_type,msg_id,reply_id,soulmate_id,timestamp) VALUES (?,?,?,?,?,?,?,?)",(user_id,text,file_id,file_type,message.message_id,send_id,soulmate_id,timestamp))
        db_execute("UPDATE users SET chat_count=COALESCE(chat_count,0)+1 WHERE user_id=?",(user_id,))

        anon_name = get_anonname(user_id)
        soulmate_anonname = get_anonname(soulmate_id)
        logging(f"{anon_name} 对 {soulmate_anonname} 说：{text}") if not file_id else logging(f"{anon_name} 向 {soulmate_anonname} 发送了一个文件")
    else:
        text = gettext(lang_code,"notbond")
        send_message(user_id,text)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

schedule.every(2).days.at("11:15").do(auto_disbond)
schedule_thread = threading.Thread(target=run_schedule)
schedule_thread.start()

bot.infinity_polling(timeout=10, long_polling_timeout=5)
