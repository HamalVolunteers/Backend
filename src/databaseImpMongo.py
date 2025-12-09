"""Database implementation mongoDB.

"""

from typing import Any
from pymongo import MongoClient, errors
from databaseInterface import DatabaseInterface

class DatabaseImpMongo(DatabaseInterface):

    def __init__(self, uri="mongodb+srv://hamalvolunteers:v96o90K2WbJ@hamalcluster.p2wonhv.mongodb.net/?appName=HamalCluster", db_name="HamalCluster"):
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect(self) -> Any:
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            return True
        except errors.PyMongoError:
            return "ERROR"
    
    def getUserById(self, id: int) -> Any:
        try:
            user = self.db.users.find_one({"id": id})
            if not user:
                return {}
            user.pop("_id", None)
            return dict(user)
        except errors.PyMongoError:
            return "ERROR"

    def getUserFilterById(self, id: int) -> Any:
        try:
            user = self.db.users.find_one({"id": id})
            if not user:
                return []
            return user.get("filters", [])
        except errors.PyMongoError:
            return "ERROR"

    def removeFilterById(self, id: int, filter: str) -> Any:
        try:
            result = self.db.users.update_one(
                {"id": id},
                {"$pull": {"filters": filter}}
            )
            if result.matched_count == 0:
                return False
            if result.modified_count == 0:
                return False
            return True
        except errors.PyMongoError:
            return "ERROR"

    def addUser(self, id: int,name:str, filters: list[str]) -> Any:
        try:
            existing = self.db.users.find_one({"id": id})
            if existing:
                return False
            user_doc = {"id": id, "name": name, "filters": filters}
            self.db.users.insert_one(user_doc)
            return True
        except errors.PyMongoError:
            return "ERROR"

    def addFilterById(self, id: int, filter: str) -> Any:
        try:
            user = self.db.users.find_one({"id": id})
            if not user:
                return "ERROR"
            filters = user.get("filters", [])
            if filter in filters:
                return False
            filters.append(filter)
            self.db.users.update_one({"id": id}, {"$set": {"filters": filters}})
            return True
        except errors.PyMongoError:
            return "ERROR"

    def getEventByFilters(self, filters: list[str]) -> Any:
        try:
            pipeline = [
                {"$match": {"filters": {"$in": filters}}},
                
                {"$addFields": {
                    "matchingCount": {
                        "$size": {"$setIntersection": ["$filters", filters]}
                    }
                }},
                
                {"$sort": {"matchingCount": -1}}
            ]

            events = list(self.db.events.aggregate(pipeline))

            for e in events:
                e.pop("matchingCount", None)
                e.pop("_id", None)

            return [dict(e) for e in events]

        except Exception as e:
            print("getEventByFilters error:", e)
            return "ERROR"

    def signUserToEvent(self, id: int, eventID: int) -> Any:
        try:
            event = self.db.events.find_one({"eventId": eventID})
            if not event:
                return "ERROR"
            if id in event.get("people", []):
                return False  # already signed
            if event.get("currentCapacity", 0) >= event.get("capacity", 0):
                return False  # event full
            self.db.events.update_one(
                {"eventId": eventID},
                {
                    "$push": {"people": id},
                    "$inc": {"currentCapacity": 1}
                }
            )
            return True
        except errors.PyMongoError:
            return "ERROR"

    def removeUserFromEvent(self, id: int, eventID: int) -> Any:
        try:
            event = self.db.events.find_one({"eventId": eventID})
            if not event or id not in event.get("people", []):
                return False
            self.db.events.update_one(
                {"eventId": eventID},
                {
                    "$pull": {"people": id},
                    "$inc": {"currentCapacity": -1}
                }
            )
            return True
        except errors.PyMongoError:
            return "ERROR"
    
    def addEvent(self,eventID: int,name:str,capacity:int,info:str,filters:list[str],location:str,date:str,duration:str) -> Any:
        try:
            existing = self.db.events.find_one({"eventId": eventID})
            if existing:
                return False
            event_doc = {"eventId": eventID, "name": name, "capacity": capacity, "currentCapacity": 0, "info": info, "people": [], "filters": filters, "location": location, "date": date, "duration": duration}
            self.db.events.insert_one(event_doc)
            return True
        except errors.PyMongoError:
            return "ERROR"
    
    def getEventById(self, eventID: int) -> Any:
        try:
            event = self.db.events.find_one({"eventId": eventID})
            if not event:
                return {}
            event.pop("_id", None)
            return dict(event)
        except errors.PyMongoError:
            return "ERROR"
    
    def getAllEvents(self) -> Any:
        try:
            events = list(self.db.events.find({}))
            for e in events:
                e.pop("_id", None)
            return [dict(e) for e in events]
        except errors.PyMongoError:
            return "ERROR"