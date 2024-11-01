from telebot.types import InlineKeyboardButton as Button, ReplyKeyboardMarkup as Mr
from telebot import TeleBot
from kvsqlite.sync import Client
from bs4 import BeautifulSoup
from datetime import datetime
import json,redis,os,yt_dlp,requests,requests,re

user_db = Client('ids.sqlite', 'users')
bann = Client('ban.sqlite', 'ban_users')
d_b = Client('message.sqlite', 'messages')
TOKEN = "7063185650:AAE1MjqP85J-nhvDGtXSMUhgZOOwJyjFA3k"
bot = TeleBot(TOKEN)
admin = [6875754996]
ch = ['@py_files']
msg_r = (
    ''
    ) 	
@bot.message_handler(commands=['admin'])
def dev(message):
    idd = message.from_user.id
    if idd in admin:
        mk = Mr(row_width=2, resize_keyboard=True)
        s1 = Button('⦗ الاحصائيات ⦘')
        s2 = Button('⦗ حظر مستخدم ⦘')
        s3 = Button('⦗ الغاء حظر مستخدم ⦘')
        s4 = Button('⦗ ارسال تخزين ⦘')
        s5 = Button('⦗ اذاعة ⦘')
        s6 = Button('قسم كليشة ⦗ start ⦘')
        s7 = Button('⦗ قسم الادمنية ⦘')
        s8 = Button('⦗ نقل البوت ⦘')
        s9 = Button('⦗ قسم الاشتراك الاجباري ⦘')
        mk.row(s1,s5)
        mk.row(s4)
        mk.row(s2,s3)
        mk.row(s7,s6)
        mk.row(s9)
        mk.row(s8)
        bot.reply_to(message, 'مرحباً عزيزي الأدمن،\n إليك لوحة التحكم:', reply_markup=mk)        
if not d_b.exists('welcome'):
    d_b.set('welcome', msg_r)
@bot.message_handler(commands=['start'])
def start(msg):
    from datetime import datetime

    join_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    global notice
    notice = True
    name = msg.chat.first_name
    user_id = msg.from_user.id
    username = msg.from_user.username
    if bann.exists(f'user_{user_id}'):
        bot.reply_to(msg, 'عذراً، لقد تم حظرك من استخدام البوت.')
        return
    if not user_db.exists(f'user_{user_id}'):
        user_info = {
            'id': user_id,
            'username': username,
            'devs': False
        }
        user_db.set(f'user_{user_id}', user_info)
        if notice:
            developer_chat_id = admin
            bot.send_message(
                developer_chat_id,
                f'- New User -\n'
                f'₪ : Name : {name}\n'
                f'₪ : ID : {user_id}\n'
                f'₪ : Username : {f"@{username}" if username else "nothing"}\n'
                f'₪ : Join Date : {join_date}'
            )
    notY = []
    for channel in ch:
        cin = bot.get_chat(channel)
        chat_m = bot.get_chat_member(chat_id=cin.id, user_id=user_id)
        if chat_m.status not in ['creator', 'member', 'administrator']:
            notY.append(channel)
    if notY:
        channels_list = "\n".join(notY)
        bot.reply_to(
            msg,
            f"عذرا عزيزي المستخدم، عليك الاشتراك في قنوات البوت لتتمكن من استخدامه:\n{channels_list}\n- - - - - - - - - - \nاشترك ثم ارسل /start"
        )
    else:
        bot.reply_to(msg, d_b.get('welcome'))
       
class DP:
    def __init__(self, username: str, chat_id: int):
        self.username = username
        self.chat_id = chat_id
        self.json_data = None

        if "@" in self.username:
            self.username = self.username.replace("@", "")
        self.admin()
    def admin(self):
        self.send_request()
        self.output()
    def send_request(self):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0"
        }
        r = requests.get(f"https://www.tiktok.com/@{self.username}", headers=headers)
        try:
            soup = BeautifulSoup(r.text, 'html.parser')
            script_tag = soup.find('script', {'id': '__UNIVERSAL_DATA_FOR_REHYDRATION__'})
            script_text = script_tag.text.strip()
            self.json_data = json.loads(script_text)["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]
        except Exception as e:
            bot.send_message(self.chat_id, "❌ خطأ: لم يتم العثور على اسم المستخدم.")
            return
    def get_user_id(self):
        try:
            return str(self.json_data["user"]["id"])
        except KeyError:
            return "Unknown"
    def get_name(self):
        try:
            return self.json_data["user"]["nickname"]
        except KeyError:
            return "Unknown"
    def is_verified(self):
        try:
            return "نعم" if self.json_data["user"]["verified"] else "لا"
        except KeyError:
            return "Unknown"
    def is_private(self):
        try:
            return "نعم" if self.json_data["user"]["privateAccount"] else "لا"
        except KeyError:
            return "Unknown"
    def followers(self):
        try:
            return self.json_data["stats"]["followerCount"]
        except KeyError:
            return "Unknown"
    def following(self):
        try:
            return self.json_data["stats"]["followingCount"]
        except KeyError:
            return "Unknown"
    def heart_count(self):
        try:
            return str(self.json_data["stats"]["heart"])
        except KeyError:
            return "Unknown"
    def video_count(self):
        try:
            return self.json_data["stats"]["videoCount"]
        except KeyError:
            return "Unknown"
    def open_favorite(self):
        try:
            return "نعم" if self.json_data["user"]["openFavorite"] else "لا"
        except KeyError:
            return "Unknown"
    def see_following(self):
        try:
            return "نعم" if str(self.json_data["user"]["followingVisibility"]) == "1" else "لا"
        except KeyError:
            return "Unknown"
    def language(self):
        try:
            return str(self.json_data["user"]["language"])
        except KeyError:
            return "Unknown"
    def user_create_time(self):
        try:
            url_id = int(self.get_user_id())
            binary = "{0:b}".format(url_id)
            i = 0
            bits = ""
            while i < 31:
                bits += binary[i]
                i += 1
            timestamp = int(bits, 2)
            dt_object = datetime.fromtimestamp(timestamp)
            return dt_object
        except Exception:
            return "Unknown"
    def last_change_name(self):
        try:
            time = self.json_data["user"]["nickNameModifyTime"]
            check = datetime.fromtimestamp(int(time))
            return check
        except KeyError:
            return "Unknown"
    def account_region(self):
        try:
            country_code = self.json_data["user"]["region"]
            return self.get_country_name(country_code)
        except KeyError:
            return "Unknown"
    def get_country_name(self, country_code):
        try:
            country = pycountry.countries.get(alpha_2=country_code.upper())
            return country.name if country else "Unknown"
        except Exception:
            return "Unknown"

    def get_avatar_url(self):
        try:
            return self.json_data["user"]["avatarLarger"]
        except KeyError:
            return None
    def output(self):
        user_info = (
            f"- معرف المستخدم: {self.get_user_id()}\n"
            f"- اسم المستخدم: {self.get_name()}\n"
            f"- موثق: {self.is_verified()}\n"
            f"- حساب خاص: {self.is_private()}\n"
            f"- متابعين: {self.followers()}\n"
            f"- متابع: {self.following()}\n"
            f"- عدد الإعجابات: {self.heart_count()}\n"
            f"- عدد الفيديوهات: {self.video_count()}\n"
            f"- المفضلة مفتوحة: {self.open_favorite()}\n"
            f"- يمكن رؤية قائمة المتابعين: {self.see_following()}\n"
            f"- لغة المستخدم: {self.language()}\n"
            f"- وقت إنشاء الحساب: {self.user_create_time()}\n"
            f"- آخر مرة تغيير الاسم: {self.last_change_name()}\n"
            f"- منطقة الحساب: {self.account_region()}\n"
            f"— — — — — — — —\nBY : @vuup04"
        )
        avatar_url = self.get_avatar_url()
        if avatar_url:
            bot.send_photo(self.chat_id, avatar_url, caption=user_info)
        else:
            bot.send_message(self.chat_id, user_info)

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    mt = message.chat.id
    m = message.text
    if mt in admin:
        if m == '⦗ حظر مستخدم ⦘':
            v = bot.send_message(mt, 'الرجاء ارسال الايدي لـ حظر المستخدم:')
            bot.register_next_step_handler(v, bannd)
        elif m == '⦗ الغاء حظر مستخدم ⦘':
            v = bot.send_message(mt, 'الرجاء ارسال الايدي لـ الغاء حظر المستخدم:')
            bot.register_next_step_handler(v, unbannd)
        elif m == 'اضافة ADMIN':
            v = bot.send_message(mt, 'الرجاء ارسال ايدي الادمن الجديد:')
            bot.register_next_step_handler(v, add_admin)
        elif m == 'حذف ADMIN':
            v = bot.send_message(mt, 'الرجاء ارسال ايدي الادمن لـ حذفه:')
            bot.register_next_step_handler(v, delete_admin)
        elif m == 'قسم كليشة ⦗ start ⦘':
            started(message)
        elif m == '⦗ قسم الادمنية ⦘':
            v = bot.send_message(mt, 'قسم الادمنيه:')
            bot.register_next_step_handler(v, ads)
        elif m == 'رجوع إلى الافتراضي':
            v = bot.send_message(mt, 'تم العودة الى الكليشة الاساسية 👾')
            bot.register_next_step_handler(v, reset_msg)
        elif m == 'تغيير الكليشة':
            v = bot.send_message(mt, 'الرجاء ارسال الكليشة الجديدة:')
            bot.register_next_step_handler(v, set_new_msg)
        elif m == 'حذف الكليشة':
            v = bot.send_message(mt, 'تم حذف الكليشة الحالية، ارسل الجديدة:')
            bot.register_next_step_handler(v, delete_msg)
        elif m == '⦗ الاحصائيات ⦘':
            status(message)
        elif m == '⦗ اذاعة ⦘':
            v = bot.send_message(mt, 'ارسل ماتريد اذاعته:')
            bot.register_next_step_handler(v, cast)
        elif m == '⦗ ارسال تخزين ⦘':
            files(message)
        elif m == 'رجوع 🔙':
            go_back(message)
        elif m == '⦗ قسم الاشتراك الاجباري ⦘':
            set_ch(message)
        elif m == 'اضافة قناة':
            v = bot.send_message(mt, 'قم بارسال معرف القناة مع @')
            bot.register_next_step_handler(v, addch)
        elif m == 'حذف قناة':
            v = bot.send_message(mt, 'قم بارسال معرف القناة مع @')
            bot.register_next_step_handler(v, delch)
        elif m == 'عرض القنوات':
        	showch(message)
    if 'tiktok.com' in m:
        download_tiktok_video(message)
    else:
        get_info(message)
        
def bannd(msg):
    try:
        user_id = int(msg.text)
        bann.set(f'user_{user_id}', {'id': user_id})
        bot.reply_to(msg, 'تم حظره')
    except ValueError:
        bot.reply_to(msg, 'خطأ في الايدي')
        
def unbannd(msg):
    try:
        user_id = int(msg.text)
        if bann.exists(f'user_{user_id}'):
            bann.delete(f'user_{user_id}')
            bot.reply_to(msg, 'تم إلغاء حظر المستخدم.')
        else:
            bot.reply_to(msg, 'المستخدم غير محظور.')
    except ValueError:
        bot.reply_to(msg, 'خطأ في الايدي')

def files(msg):
    with open('ids.sqlite', 'rb') as file:
        bot.send_document(msg.chat.id, file)
    with open('ban.sqlite', 'rb') as file_bannd:
        bot.send_document(msg.chat.id, file_bannd)

def status(message):
    members = user_db.keys()
    band = bann.keys()
    userrs = len(members) if members is not None else 0
    banned = len(band) if band is not None else 0
    iL = f"مستخدمين البوت : {userrs}\n"
    iL += f"المحظورين : {banned}"
    bot.reply_to(message, iL)
    
def started(msg):
    iL = Mr(row_width=3, resize_keyboard=True)
    i1 = Button('تغيير الكليشة')
    i2 = Button('رجوع إلى الافتراضي')
    i3 = Button('حذف الكليشة')
    i4 = Button('رجوع 🔙')    
    iL.add(i1)
    iL.add(i2,i3)
    iL.add(i4)
    bot.reply_to(msg, 'قسم كليشة (start)', reply_markup=iL)

def ads(msg):
    keyboard = Mr(resize_keyboard=True)
    btn_add = Button(text='اضافة ADMIN')
    btn_delete = Button(text='حذف ADMIN')
    btn_back = Button(text='رجوع 🔙')
    keyboard.row(btn_add, btn_delete)
    keyboard.row(btn_back)
    bot.reply_to(msg, 'اختر ما تريد:', reply_markup=keyboard)

def set_ch(msg):
    iL = Mr(row_width=3, resize_keyboard=True)
    i1 = Button('اضافة قناة')
    i2 = Button('حذف قناة')
    i3 = Button('عرض القنوات')
    i4 = Button('رجوع 🔙')    
    iL.add(i1, i2)
    iL.add(i3)
    iL.add(i4)
    bot.reply_to(msg, 'قسم الاشتراك الاجباري:', reply_markup=iL)    
def add_to_admin(message):
    idd = message.from_user.id
    if idd in admin:
        bot.reply_to(message, 'من فضلك أرسل الأيدي الجديد للأدمن لإضافته:')
        bot.register_next_step_handler(message, add_new_admin_id)
    else:
        bot.reply_to(message, 'لاتمتلك الصلاحيات لاستعامل الأوامر !')
def add_admin(message):
    new_admin_id = message.text.strip()
    try:
        new_admin_id = int(new_admin_id)
    except ValueError:
        bot.reply_to(message, 'الرجاء إدخال أيدي صحيح.')
        return    
    admin.append(new_admin_id)
    bot.reply_to(message, f'تم إضافة الأيدي الجديد للأدمن بنجاح: {new_admin_id}')           
def reset_msg(msg):
    d_b.set('welcome', msg_r)        
def set_new_msg(msg):
    new_msg = msg.text
    d_b.set('welcome', new_msg)
    bot.reply_to(msg, 'تم تحديث الرسالة بنجاح!')
def delete_admin(message):
    remove_id = message.text.strip()
    try:
        remove_id = int(remove_id)
    except ValueError:
        bot.reply_to(message, 'الرجاء إدخال أيدي صحيح.')
        return    
    if remove_id in admin:
        admin.remove(remove_id)
        bot.reply_to(message, f'تم حذف الأيدي {remove_id} من قائمة الأدمن بنجاح.')
    else:
        bot.reply_to(message, f'الأيدي {remove_id} ليس موجوداً في قائمة الأدمن.')
if not d_b.exists('welcome'):
    d_b.set('welcome', msg_r)          
def delete_msg(msg):
    d_b.delete('welcome')
    msg_ = bot.reply_to(msg, 'تم حذف الرسالة. الرجاء إرسال رسالة جديدة:')
    bot.register_next_step_handler(msg_, set_new_after_delete)
def set_new_after_delete(msg):
    new_msg = msg.text
    d_b.set('welcome', new_msg)
    bot.reply_to(msg, 'تم تعيين الرسالة الجديدة بنجاح!')
def go_back(msg):
    dev(msg)       
def send_video(file_path, message):
    with open(file_path, 'rb') as video:
        bot.send_video(message.chat.id, video)
    os.remove(file_path)
def check_subscription(user_id, chat_id):
    not_subscribed = []
    for channel in ch:
        cin = bot.get_chat(channel)
        chat_m = bot.get_chat_member(chat_id=cin.id, user_id=user_id)
        if chat_m.status not in ['creator', 'member', 'administrator']:
            not_subscribed.append(channel)
    return not_subscribed

def download_tiktok_video(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    notY = check_subscription(user_id, chat_id)
    if notY:
        channels_list = "\n".join(notY)
        bot.reply_to(
            message,
            f"عذرا عزيزي المستخدم، عليك الاشتراك في قنوات البوت لتتمكن من استخدام هذه الميزة:\n{channels_list}\n- - - - - - - - - - \nاشترك ثم اعد ارسال الفيديو."
        )
        return
    try:
        us = bot.get_me().username
        m = message.text
        url = f"https://www.tikwm.com/api/?url={m}"
        res = requests.get(url).json()
        if 'data' not in res or 'play' not in res['data'] or 'title' not in res['data']:
            bot.reply_to(message, "- لم أتمكن من جلب الفيديو. يرجى التحقق من الرابط.")
            return        
        wait = bot.reply_to(message, "جاري التحميل ===>")
        video = res['data']['play']
        bot.delete_message(chat_id, wait.message_id)
        bot.send_video(chat_id, video, caption=f'- @{us} .', reply_to_message_id=message.message_id)        
        if r:
            title = res['data']['title']
            r.set(f"history:{user_id}", f"{title}")
            r.set(f"link:{user_id}", f"{m}")
    except Exception as e:
        print(f"Error in TikTok handler: {str(e)}")
        return 

def get_info(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    notY = check_subscription(user_id, chat_id)
    if notY:
        channels_list = "\n".join(notY)
        bot.reply_to(
            message,
            f"عذرا عزيزي المستخدم، عليك الاشتراك في قنوات البوت لتتمكن من استخدام هذه الميزة:\n{channels_list}\n- - - - - - - - - - \nاشترك ثم اعد ارسال اسم المستخدم."
        )
        return
    username = message.text.strip()
    if re.match("^[a-zA-Z0-9_]+$", username):
        ga = bot.reply_to(message, 'جارٍ البحث ===>')
        DP(username=username, chat_id=chat_id)
        bot.delete_message(chat_id, ga.message_id)
def addch(message):
    username = message.text.strip()
    if not username.startswith('@'):
        bot.send_message(message.chat.id, "الرجاء التأكد من كتابة اليوزر بشكل صحيح مع @")
        return    
    try:
        chat_member = bot.get_chat_member(chat_id=username, user_id=bot.get_me().id)       
        if username in ch:
            bot.send_message(message.chat.id, f"• القناة {username} موجودة بالفعل.")
        else:
            ch.append(username)
            bot.send_message(message.chat.id, f"✅ تمت إضافة {username} إلى الاشتراك الإجباري.")
    except Exception as e:
        error_message = "لم يتم العثور على القناة، تأكد من رفع البوت مشرف مع صلاحية دعوة مستخدمين عبر الرابط."
        bot.send_message(message.chat.id, error_message)
def delch(message):
    username = message.text.strip()
    if username in ch:
        ch.remove(username)
        bot.send_message(message.chat.id, f"تم حذف {username} من القائمة.")
    else:
        bot.send_message(message.chat.id, "القناة غير موجودة أصلاً.") 
def showch(msg):
    if ch:
        ch_list = "\n".join(ch)
        bot.reply_to(msg, f"قنوات الاشتراك الحالية:\n{ch_list}")
    else:
        bot.reply_to(msg, "لا توجد قنوات اشتراك حالياً.")               
def cast(message):
    bot.reply_to(message, 'جارٍ الإذاعة، الرجاء الانتظار...')
    keys = user_db.keys()
    users = []
    total = 0
    failed = 0
    
    if not keys:
        bot.reply_to(message, 'لا يوجد مستخدمين لإرسال الرسالة.')
        return
    
    for i in keys:
        key = i[0]
        try: 
            users.append(user_db.get(key)['id'])
        except:
            continue
    
    for i in users:
        try:
            bot.copy_message(chat_id=i, from_chat_id=message.chat.id, message_id=message.message_id)
            total += 1
        except:
            failed += 1
            continue
    
    rate = (total / len(keys)) * 100 if len(keys) > 0 else 0
    
    bot.reply_to(message, f'- الكلي : {len(keys)}. \n- نجحت لـ : {total}. \n- فشلت لـ : {failed}. \n- النسبة المئوية : {rate:.2f}%')

   
bot.infinity_polling(skip_pending = True)
if __name__ == '__main__': main()
#=================
#done BY : @world_father
