# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

'''Forms
Better intent examples
More stories and rules
Config.yml
Training stories more'''


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from sqlalchemy import create_engine, update, MetaData, Table, Column, Integer, VARCHAR, text
#from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.engine import result

engine = create_engine('postgresql://postgres:sys@localhost/helix')
meta = MetaData(bind=engine)
MetaData.reflect(meta)

user = Table(
    'user', meta,
    Column('u_id', Integer, primary_key=True),
    Column('u_name', VARCHAR),
    extend_existing=True
)


device = Table(
    'device', meta,
    Column('d_id', Integer, primary_key=True),
    Column('d_type', VARCHAR),
    Column('d_value', Integer),
    extend_existing=True
)

smart_tv = Table(
    'smart_tv', meta,
    Column('s_app', VARCHAR),
    Column('s_search', VARCHAR),
    Column('s_running', Integer),
    extend_existing=True
)

meta.create_all(engine)

u1 = user.insert().values(u_id=1, u_name='Farae')
u2 = user.insert().values(u_id=2, u_name='Hamza')
u3 = user.insert().values(u_id=3, u_name='Umair')

d1 = device.insert().values(d_id=1, d_type='Light', d_value=0)
d2 = device.insert().values(d_id=2, d_type='Door', d_value=0)

#engine.execute(u1)
#engine.execute(u2)
#engine.execute(u3)
#engine.execute(d1)
#engine.execute(d2)

tv = smart_tv.insert().values(s_app="None", s_search="None", s_running=0)
#engine.execute(tv)

class ActLockDoor(Action):
    def name(self) -> Text:
        return "act_lock_door"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        DEVICE = meta.tables['device']

        u = update(DEVICE)
        u = u.values({"d_value" : 1})
        u = u.where(DEVICE.c.d_type == "Door")
        engine.execute(u)

        return []
    
class ActUnlockDoor(Action):
    def name(self) -> Text:
        return "act_unlock_door"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        DEVICE = meta.tables['device']

        u = update(DEVICE)
        u = u.values({"d_value" : 0})
        u = u.where(DEVICE.c.d_type == "Door")
        engine.execute(u)

        return []
    
class ActLightOn(Action):
    def name(self) -> Text:
        return "act_light_on"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        DEVICE = meta.tables['device']
        u = update(DEVICE)
        u = u.values({"d_value" : 1})
        u = u.where(DEVICE.c.d_type == "Light")
        engine.execute(u)

        return []
    
class ActLightOff(Action):
    def name(self) -> Text:
        return "act_light_off"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        DEVICE = meta.tables['device']
        u = update(DEVICE)
        u = u.values({"d_value" : 0})
        u = u.where(DEVICE.c.d_type == "Light")
        engine.execute(u)

        return []
    
class ActOpenEntertainment(Action):
    def name(self) -> Text:
        return "act_open_entertainment"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entertainment = tracker.get_slot("entertainment")
        source = tracker.get_slot("source")
        msg = ""
        ent = ["netflix", "hulu", "youtube", "spotify", "disneyplus"]
        if entertainment.lower() in ent:
            update_tv = smart_tv.update().values(s_app=source, s_search=entertainment, s_running=1)
            engine.execute(update_tv)
            msg = f"sure, opening {source} with {entertainment}"
        else:
            msg = f"the platform {source} is not registered with the system. please try again"
        dispatcher.utter_message(text=msg)

        return []
    
class ActCloseEntertainment(Action):
    def name(self) -> Text:
        return "act_close_entertainment"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        update_tv = smart_tv.update().values(s_running=0)
        engine.execute(update_tv)
        msg = f"sure, closing the smart tv"
        dispatcher.utter_message(text=msg)

        return []