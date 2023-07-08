from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.uix.list import TwoLineIconListItem, IconLeftWidgetWithoutTouch
from kivymd.uix.pickers import MDTimePicker
from datetime import datetime,timedelta
from kivy.properties import ObjectProperty
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivy.uix.settings import SettingsWithSidebar
from jsonsettings import settings_json
import time
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import os
from oscpy.client import OSCClient
from oscpy.server import OSCThreadServer
from jnius import autoclass, cast
from kivy import platform

class Content(MDBoxLayout):
    pass

class MainApp(MDApp):
    icon_list_s = []
    icon_list_w = []
    listitem_list_w=[]
    listitem_list_s=[]
    timetosleep=0
    alm_time_w={}
    alm_time_s={}
    tf="%H:%M:%S"
    dtf="%Y-%m-%d %H:%M:%S"
    dtfval=[]
    
    def build(self):
        #self.settings_cls = SettingsWithSidebar
        self.use_kivy_settings = False
        self.timetosleep = int(self.config.get('HealthySleep', 'timetosleep'))
        timeformat=self.config.get('HealthySleep', 'timeformat')
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepOrange"

        self.service = None
        self.server = server = OSCThreadServer()
        server.listen(
            address=b'localhost',
            port=3002,
            default=True,
        )

        server.bind(b'/message', self.display_message)
        #server.bind(b'/date', self.date)
        self.client = OSCClient(b'localhost', 3000)

        if timeformat=='24H': 
            self.tf="%H:%M:%S"
            self.dtf="%Y-%m-%d %H:%M:%S"
        else:
            self.tf="%I:%M %p"
            self.dtf="%Y-%m-%d %I:%M %p"

    def send(self, *args):
        self.client.send_message(b'/ping', [])

    def display_message(self, message):
        if self.root:
            self.root.ids.labeltest.text += '{}\n'.format(message.decode('utf8'))

    def date(self, message):
        if self.root:
            self.root.ids.date.text = message.decode('utf8')


    def ret_dtf(self):
        self.dtfval.insert(0,self.dtf)

    def build_config(self, config):
        config.setdefaults('HealthySleep', {
            'timetosleep': 15,
            'timeformat': '24H'
            })

    def build_settings(self, settings):
        settings.add_json_panel('Settings',
                                self.config,
                                data=settings_json)

    def on_config_change(self, config, section,
                         key, value):
        self.timetosleep = int(self.config.get('HealthySleep', 'timetosleep'))
        timeformat=self.config.get('HealthySleep', 'timeformat')
        if timeformat=='24H': 
            self.tf="%H:%M:%S"
            self.dtf="%Y-%m-%d %H:%M:%S"
        else:
            self.tf="%I:%M %p"
            self.dtf="%Y-%m-%d %I:%M %p"

    def on_start(self):

        #self.start_service()

        self.root.ids.box.add_widget(
            MDExpansionPanel(
                icon="emoticon-happy-outline",
                content=Content(),
                panel_cls=MDExpansionPanelOneLine(
                    text="I'm Happy about the app",
                )
            )
        )
        self.root.ids.box.add_widget(
            MDExpansionPanel(
                icon="emoticon-neutral-outline",
                content=Content(),
                panel_cls=MDExpansionPanelOneLine(
                    text="Nothing bad or good to say",
                )
            )
        )
        self.root.ids.box.add_widget(
            MDExpansionPanel(
                icon="emoticon-sad-outline",
                content=Content(),
                panel_cls=MDExpansionPanelOneLine(
                    text="I'm Unsatisfied about the app",
                )
            )
        )


    def disp_alarm_sleep(self):
        sdt=self.root.ids.stime.text
        if (sdt!=""):
            Current_date = datetime.now()
            dt = datetime.strptime(sdt, self.tf)
            dtadded=dt+timedelta(minutes=self.timetosleep)
            t1=dtadded.time()
            t2 = Current_date.time()
            if t1>t2: 
                d=Current_date.date()
            else:
                d=Current_date.date()+timedelta(1)
            self.root.ids.alarm_list_w.clear_widgets()
            dt_calc=datetime.combine(d,t1)
            self.icon_list_w.clear()
            self.listitem_list_w.clear()
            self.alm_time_w.clear()
            self.ret_dtf()
            for i in range(7):
                stime=dt_calc+timedelta(minutes=1.5*(i+1))
                strstime=stime.strftime(self.dtf)
                icons=IconLeftWidgetWithoutTouch(icon="bell-outline")
                listitem=TwoLineIconListItem(text=str(strstime),secondary_text="Cycle "+str(i+1)+" Alarm")
                self.icon_list_w.append(icons)
                self.listitem_list_w.append(listitem)
                listitem.add_widget(icons)
                listitem.bind(on_release=self.change_icon)
                self.root.ids.alarm_list_w.add_widget(listitem, index=i)


    def change_icon(self,listdata):
        sindex = self.root.ids.alarm_list_w.children.index(listdata)
        if self.icon_list_w[sindex].icon == "bell":
            self.icon_list_w[sindex].icon = "bell-outline"
            del self.alm_time_w[sindex]
        else:
            self.icon_list_w[sindex].icon ="bell"
            sval=self.listitem_list_w[sindex].text
            self.alm_time_w[sindex]=sval
            self.onCreate(sindex,'w')

    def show_time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(on_save=self.get_time)
        time_dialog.open()

       
    def get_time(self, instance, time):            
        self.root.ids.stime.text=time.strftime(self.tf)
        self.disp_alarm_sleep()

    def disp_alarm_wake(self):
        wdt=self.root.ids.wtime.text
        if (wdt!=""):
            Current_date = datetime.now()
            dt = datetime.strptime(wdt, self.tf)
            dtadded=dt-timedelta(minutes=self.timetosleep)
            t1=dtadded.time()
            t2 = Current_date.time()
            if t1>t2: 
                d=Current_date.date()
            else:
                d=Current_date.date()+timedelta(1)
            self.root.ids.alarm_list_s.clear_widgets()
            dt_calc=datetime.combine(d,t1)
            self.icon_list_s.clear()
            self.listitem_list_s.clear()
            self.alm_time_s.clear()
            self.ret_dtf()
            for i in range(7):
                stime=dt_calc-timedelta(minutes=1.5*(i+1))
                strstime=stime.strftime(self.dtf)
                icons=IconLeftWidgetWithoutTouch(icon="bell-outline")
                listitem=TwoLineIconListItem(text=str(strstime),secondary_text="Cycle "+str(i+1)+" Alarm")
                self.icon_list_s.append(icons)
                self.listitem_list_s.append(listitem)
                listitem.add_widget(icons)
                listitem.bind(on_release=self.change_icon2)
                self.root.ids.alarm_list_s.add_widget(listitem, index=i)


    def change_icon2(self,listdata):
        sindex = self.root.ids.alarm_list_s.children.index(listdata)
        if self.icon_list_s[sindex].icon == "bell":
            self.icon_list_s[sindex].icon = "bell-outline"
            del self.alm_time_s[sindex]
        else:
            self.icon_list_s[sindex].icon ="bell"
            sval=self.listitem_list_s[sindex].text
            self.alm_time_s[sindex]=sval
            self.onCreate(sindex,'s')

    def show_time_picker_s(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(on_save=self.get_time_s)
        time_dialog.open()

       
    def get_time_s(self, instance, time):            
        self.root.ids.wtime.text=time.strftime(self.tf)
        self.disp_alarm_wake()

    def pick_time_format(self):
        self.menu_list = [
            {
                "viewclass": "OneLineListItem",
                "text": "24H",
                "on_release": lambda x="24H": self.drop_option(x)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "12H",
                "on_release": lambda x="12H": self.drop_option(x)
            }
        ]
        self.dropdown=MDDropdownMenu(
            caller=self.root.ids.ftimedrop,
            items = self.menu_list,
            width_mult=4
        )
        self.dropdown.open()

    def drop_option(self, option_text):
        self.root.ids.ftime.text=option_text
        self.dropdown.dismiss()

    def send_mail(self):
        import smtplib, ssl

        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "sleep.healthycontact@gmail.com"  # Enter your address
        receiver_email = "sleep.healthycontact@gmail.com"  # Enter receiver address
        password = "sam_19820205"
        esubject=self.root.ids.contsub.text
        ebody=self.root.ids.contdet.text
        message = "Subject: "+ esubject +"/n/n"+ ebody

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
    
    def start_service(self):
        if platform == "android":
            self.service = autoclass("coffersmart.com.healthysleep.ServiceHealthysleep")
            self.mActivity = autoclass("org.kivy.android.PythonActivity").mActivity
           # self.service.start(self.mActivity, "")
            #return self.service

        elif platform in ('linux', 'linux2', 'macos', 'win'):
            from runpy import run_path
            from threading import Thread
            self.service = Thread(
                target=run_path,
                args=['service.py'],
                kwargs={'run_name': '__main__'},
                daemon=True
            )
            self.service.start()
        else:
            raise NotImplementedError(
                "service start not implemented on this platform"
            )
        
    def onCreate(self,sindex,atype):
        # initialize alarm time
        if atype=='s':
            aval=self.alm_time_s[sindex]
        else:
            aval=self.alm_time_w[sindex]
        faval=datetime.strptime(aval,self.dtfval[0])
        curr_time=datetime.now()
        #print(faval)
        #print(curr_time)
        time_remain=faval-curr_time
        alarm_time=time_remain.total_seconds()
        # set alarm to trigger at the specified time
        print(alarm_time)
        if platform == "android":
            self.service = autoclass("coffersmart.com.healthysleep.ServiceHealthysleep")
            mActivity = autoclass("org.kivy.android.PythonActivity").mActivity
            context = mActivity.getApplicationContext()
            Context = autoclass("android.content.Context")
            Intent = autoclass("android.content.Intent")
            PendingIntent = autoclass("android.app.PendingIntent")
            String = autoclass("java.lang.String")
            Int = autoclass("java.lang.Integer")
            intent = Intent()
            intent.setClass(context, Notify)
            intent.setAction("org.coffersmart.com.NOTIFY")
            pending_intent = PendingIntent.getBroadcast(
            context, 1001, intent, PendingIntent.FLAG_CANCEL_CURRENT
            )
            ring_time = time.time_ns() // 1_000_000
            cast(
            AlarmManager, context.getSystemService(Context.ALARM_SERVICE)
            ).setExactAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, ring_time, pending_intent)
            #self.client.send_message(b'/ping', [alarm_time])
            #self.alarm_event=Clock.schedule_once(self.on_alarm, alarm_time)

    def stop_service(self):
        if self.service:
            if platform == "android":
                self.service.stop(self.mActivity)
                self.service=None
            elif platform in ('linux', 'linux2', 'macos', 'win'):
                # The below method will not work. 
                # Need to develop a method like 
                # https://www.oreilly.com/library/view/python-cookbook/0596001673/ch06s03.html
                self.service.stop()
                self.service=None
            else:
            	raise NotImplementedError(
                	"service start not implemented on this platform"
            	)
        


class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

MainApp().run()
