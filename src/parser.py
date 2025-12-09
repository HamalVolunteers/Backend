"""Parser module

This module defines a parsing interface for processing input data.
It gets the JSON input from the FastAPI server and routes it to the
appropriate handler functions based on the specified action.
It then returns the processed result back to the server.

"""

ERROR = {"status": "error"}
from databaseImpMongo import DatabaseImpMongo

class Parser:
    def __init__(self):
        self.db = DatabaseImpMongo()
        if self.db.connect() != True:
            raise Exception("Failed to connect to MongoDB")

    def parse(self, inputData: dict) -> dict:
        action = inputData.get("action")
        payload = inputData.get("payload", {})

        handlers = {
            "getUserById": self.parseGetUserById,
            "getFiltersByUserId": self.parseGetFiltersByUserId,
            "removeFilterById": self.parseRemoveFilterById,
            "addUser": self.parseAddUser,
            "addFilterById": self.parseAddFilterById,
            "getEventByFilters": self.parseGetEventByFilters,
            "signUserToEvent": self.parseSignUserToEvent,
            "removeUserFromEvent": self.parseRemoveUserFromEvent,
            "addEvent": self.parseAddEvent,
            "getEventById": self.parseGetEventById,
            "getAllEvents": self.parseGetAllEvents
        }

        if action not in handlers:
            return ERROR

        try:
            return handlers[action](payload)
        except Exception as e:
            return ERROR
    
    def parseGetUserById(self, payload: dict) -> dict:
        userId = payload.get("id")
        if userId is None:
            return ERROR

        result = self.db.getUserById(int(userId))

        if result == "ERROR":
            return ERROR
        return {"status": "ok", "data": result}

    def parseGetFiltersByUserId(self, payload: dict) -> dict:
        userId = payload.get("id")
        if userId is None:
            return ERROR

        result = self.db.getUserFilterById(int(userId))

        if result == "ERROR":
            return ERROR
        return {"status": "ok", "data": result}

    def parseRemoveFilterById(self, payload: dict) -> dict:
        userId = payload.get("id")
        filter = payload.get("filter")
        if userId is None or filter is None:
            return ERROR

        result = self.db.removeFilterById(int(userId), str(filter))
        if result == "ERROR":
            return ERROR
        return {"status": "ok", "data": result}

    def parseAddUser(self, payload: dict) -> dict:
        userId = payload.get("id")
        filters = payload.get("filters", [])
        name = payload.get("name", "")
        if userId is None:
            return ERROR

        if not isinstance(filters, list):
            return ERROR

        result = self.db.addUser(int(userId),name, filters)

        if result == "ERROR":
            return ERROR
        return {"status": "ok", "data": result}

    def parseAddFilterById(self, payload: dict) -> dict:
        userId = payload.get("id")
        filter_str = payload.get("filter")

        if userId is None or filter_str is None:
            return ERROR

        result = self.db.addFilterById(int(userId), filter_str)

        if result == "ERROR":
            return ERROR
        return {"status": "ok", "data": result}

    def parseGetEventByFilters(self, payload: dict) -> dict:
        filters = payload.get("filters", [])

        if not isinstance(filters, list):
            return ERROR

        result = self.db.getEventByFilters(filters)

        if result == "ERROR":
            return ERROR
        return {"status": "ok", "data": result}

    def parseSignUserToEvent(self, payload: dict) -> dict:
        userId = payload.get("id")
        eventId = payload.get("eventId")

        if userId is None or eventId is None:
            return ERROR

        result = self.db.signUserToEvent(int(userId), int(eventId))

        if result == "ERROR":
            return ERROR
        return {"status": "ok", "data": result}

    def parseRemoveUserFromEvent(self, payload: dict) -> dict:
        userId = payload.get("id")
        eventId = payload.get("eventId")

        if userId is None or eventId is None:
            return ERROR

        result = self.db.removeUserFromEvent(int(userId), int(eventId))

        if result == "ERROR":
            return ERROR
        return {"status": "ok", "data": result}
    
    def parseAddEvent(self, payload: dict) -> dict:
        eventId = payload.get("eventId")
        name = payload.get("name", "")
        capacity = payload.get("capacity", 0)
        info = payload.get("info", "")
        filters = payload.get("filters", [])
        location = payload.get("location", "")
        date = payload.get("date", "")
        duration = payload.get("duration", "")

        if eventId is None:
            return ERROR

        result = self.db.addEvent(int(eventId), str(name), int(capacity), str(info), list(filters),str(location),str(date),str(duration))
        if result == "ERROR":
            return ERROR
        return {"status": "ok", "data": result}
    
    def parseGetEventById(self, payload: dict) -> dict:
        eventId = payload.get("eventId")

        if eventId is None:
            return ERROR

        result = self.db.getEventById(int(eventId))
        if result == "ERROR":
            return ERROR
        return {"status": "ok", "data": result}
    
    def parseGetAllEvents(self, payload: dict) -> dict:
        result = self.db.getAllEvents()
        if result == "ERROR":
            return ERROR
        return {"status": "ok", "data": result}