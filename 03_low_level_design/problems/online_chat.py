"""
🔴 Online Chat — users, friend requests, private & group chats, Observer for delivery.

Primer: https://github.com/donnemartin/system-design-primer/blob/master/solutions/object_oriented_design/online_chat/online_chat.ipynb
System-design version: 02_system_design/12_problems/medium/08_chat_system.md

Requirements:
  - Users send/accept/reject friend requests
  - Private chat between two friends; group chat with many users
  - Sending a message notifies all other participants (Observer pattern)
  - Message history per chat, ordered
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass
from enum import Enum


class RequestStatus(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


@dataclass
class Message:
    id: int
    sender: str
    text: str


class User:
    def __init__(self, user_id: str, service: ChatService):
        self.id = user_id
        self.service = service
        self.friends: set[str] = set()
        self.inbox: list[tuple[int, Message]] = []  # (chat_id, message) — what a push would deliver

    def on_message(self, chat: Chat, msg: Message) -> None:  # Observer callback
        self.inbox.append((chat.id, msg))

    def send_friend_request(self, to: str) -> FriendRequest:
        return self.service.send_request(self.id, to)


@dataclass
class FriendRequest:
    sender: str
    receiver: str
    status: RequestStatus = RequestStatus.PENDING


class Chat:
    _ids = itertools.count(1)

    def __init__(self, members: list[User]):
        self.id = next(Chat._ids)
        self.members = {u.id: u for u in members}
        self.messages: list[Message] = []
        self._msg_ids = itertools.count(1)

    def send(self, sender: User, text: str) -> Message:
        if sender.id not in self.members:
            raise PermissionError("not a member")
        msg = Message(next(self._msg_ids), sender.id, text)
        self.messages.append(msg)
        for uid, user in self.members.items():  # notify observers
            if uid != sender.id:
                user.on_message(self, msg)
        return msg


class PrivateChat(Chat):
    def __init__(self, a: User, b: User):
        if b.id not in a.friends:
            raise PermissionError("users must be friends")
        super().__init__([a, b])


class GroupChat(Chat):
    def add(self, user: User) -> None:
        self.members[user.id] = user

    def remove(self, user: User) -> None:
        self.members.pop(user.id, None)


class ChatService:
    def __init__(self):
        self.users: dict[str, User] = {}
        self.requests: list[FriendRequest] = []

    def register(self, user_id: str) -> User:
        u = User(user_id, self)
        self.users[user_id] = u
        return u

    def send_request(self, sender: str, receiver: str) -> FriendRequest:
        req = FriendRequest(sender, receiver)
        self.requests.append(req)
        return req

    def respond(self, req: FriendRequest, accept: bool) -> None:
        req.status = RequestStatus.ACCEPTED if accept else RequestStatus.REJECTED
        if accept:
            self.users[req.sender].friends.add(req.receiver)
            self.users[req.receiver].friends.add(req.sender)


if __name__ == "__main__":
    svc = ChatService()
    a, b, c = svc.register("alice"), svc.register("bob"), svc.register("carol")
    try:
        PrivateChat(a, b)
        raise AssertionError("should require friendship")
    except PermissionError:
        pass
    svc.respond(a.send_friend_request("bob"), accept=True)
    pc = PrivateChat(a, b)
    pc.send(a, "hi bob")
    assert b.inbox[-1][1].text == "hi bob" and not a.inbox
    g = GroupChat([a, b, c])
    g.send(c, "hello all")
    assert len(a.inbox) == 1 and len(b.inbox) == 2
    print("✅ Online chat tests passed")
