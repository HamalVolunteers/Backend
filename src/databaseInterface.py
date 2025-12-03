"""Database interface contract.

This module defines an abstract `DatabaseInterface` describing the
operations expected from any concrete database implementation used
by the project.

General return policy:
- On success: methods return the documented Python type (e.g. `dict`,
  `list`, `bool`).
- On failure: implementations should return the string literal
  ``"ERROR"`` to signal an error condition (or raise an exception).

Note: returning ``"ERROR"`` is a project convention described here;
exceptions may also be raised by implementations for error handling.
"""

from abc import ABC, abstractmethod
from typing import Any


class DatabaseInterface(ABC):
    @abstractmethod
    def connect(self) -> Any:
        """Establish a connection to the underlying database.

        Returns:
        - On success: the string `True`.
        - On failure: the string `ERROR`.
        """
        pass

    @abstractmethod
    def getUserById(self, id: int) -> Any:
        """Return user information for the given username.

        Parameters:
        - `id`: the id to look up.

        Returns:
        - On success: a `dict` representing the user (e.g. `{'id': ..., ...}`)
        - If user not found: an empty `dict` or `None` (implementation choice)
        - On failure: the string `ERROR`.
        """
        pass

    @abstractmethod
    def getUserFilterById(self, id: int) -> Any:
        """Retrieve filters (preferences/tags) associated with a user id.

        Parameters:
        - `id`: numeric user id.

        Returns:
        - On success: `list[str]` of filters.
        - If no filters: empty list.
        - On failure: the string `ERROR`.
        """
        pass

    @abstractmethod
    def removeFilterById(self, id: int,filter:str) -> Any:
        """Remove one or more filters associated with a user id.

        Parameters:
        - `id`: numeric user id.

        Returns:
        - On success: `True`.
        - If nothing removed: `False`.
        - On failure: the string `ERROR`.
        """
        pass

    @abstractmethod
    def addUser(self, id: int,name:str, filters: list[str]) -> Any:
        """Add a new user with the given id and initial filters.

        Parameters:
        - `id`: numeric user id.
        - `filters`: list of filter strings.
        - `name`: the username.

        Returns:
        - On success: a `dict` for the newly created user or `True`.
        - If user already exists: `False` or an `ERROR` depending on impl.
        - On failure: the string `ERROR`.
        """
        pass

    @abstractmethod
    def addFilterById(self, id: int, filter: str) -> Any:
        """Add a single filter string to the user identified by `id`.

        Parameters:
        - `id`: numeric user id.
        - `filter`: single filter string to add.

        Returns:
        - On success: `True`.
        - If filter already present: `False`.
        - On failure: the string `ERROR`.
        """
        pass

    @abstractmethod
    def getEventByFilters(self, filters: list[str]) -> Any:
        """Return events that match any (or all) of the provided filters.

        Parameters:
        - `filters`: list of filter strings to match events against.

        Returns:
        - On success: `list[dict]` where each dict describes an event.
        - If no events found: empty list.
        - On failure: the string `ERROR`.
        """
        pass

    @abstractmethod
    def signUserToEvent(self, id: int, eventID: int) -> Any:
        """Register a user to an event.

        Parameters:
        - `id`: numeric user id.
        - `eventID`: numeric event id.

        Returns:
        - On success: `True`.
        - On failure: the string `ERROR`.
        """
        pass

    @abstractmethod
    def removeUserFromEvent(self, id: int, eventID: int) -> Any:
        """Unregister a user from an event.

        Parameters:
        - `id`: numeric user id.
        - `eventID`: numeric event id.

        Returns:
        - On success: `True`.
        - On failure: the string `ERROR`.
        """
        pass

    @abstractmethod
    def addEvent(self,eventID: int,name:str,capacity:int,info:str,filters:list[str],location:str,date:str,duration:str) -> Any:
        """Add a new event.

        Parameters:
        - `eventID`: numeric event id.
        - `name`: event name.
        - `capacity`: event capacity.
        - `info`: additional event information.
        - `filters`: list of filter strings associated with the event.
        - `location`: event location.
        - `date`: event date.
        - `duration`: event duration.

        Returns:
        - On success: `True`.
        - On failure: the string `ERROR`.
        """
        pass

    @abstractmethod
    def getEventById(self,eventID: int) -> Any:
        """Retrieve event information by event ID.

        Parameters:
        - `eventID`: numeric event id.

        Returns:
        - On success: a `dict` representing the event.
        - If event not found: an empty `dict` or `None` (implementation choice)
        - On failure: the string `ERROR`.
        """
        pass