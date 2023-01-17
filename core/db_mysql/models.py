from enum import Enum

from sqlalchemy import (
    TIMESTAMP,
    Column,
    String,
    BIGINT,
    INTEGER,
  )
from sqlalchemy.dialects.mysql import ENUM, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Push(Base):
    """Уведомления. Могут использоваться в нескольких компаниях."""
    __tablename__ = 'push'

    class PushType(ENUM):
        WINDALERT = 'wind_alert'
        CHATALERT = 'chat'
        MEMEALERT = 'meme_alert'

    push_id = Column(INTEGER, primary_key=True)
    headings = Column(JSON, nullable=True)
    contents = Column(JSON, nullable=True)
    push_type = Column(PushType, nullable=False)

    def __repr__(self):
        return f"<Push: {self.id}, {self.headings=}, {self.contents=}>"


# class User(Base):
#     """Пользователи."""
#     __tablename__ = 'user'
#
#     class PushTokenType(str, Enum):
#         ANDROID = 'android'
#         IOS = 'ios'
#         UNKNOWN = 'unknown'
#         UNIVERSALPUSH = 'universalPush'
#         UNIVERSALANDROID = 'universalPushAndroid'
#         UNIVERSALIOS = 'universalPushIos'
#         ONESIGNALANDROID = 'onesignalPushAndroid'
#         ONESIGNALIOS = 'onesignalPushIos'
#
#     userID = Column(VARCHAR(64), nullable=False, primary_key=True)
#     chatDisplayName = Column(VARCHAR(64), nullable=True)
#     locale = Column(VARCHAR(64), nullable=True)
#     pushToken = Column(VARCHAR(255), nullable=True)
#     pushTokenType = Column(PushTokenType, nullable=False, default='unknown')
#     email = Column(VARCHAR(128), nullable=True)
#     password = Column(VARCHAR(128), nullable=True)
#     firstName = Column(Text, nullable=True)
#     lastName = Column(Text, nullable=True)
#     avatarURL = Column(Text, nullable=True)
#     fb = Column(TINYINT(4), nullable=True, default=0)
#     fbData = Column(VARCHAR(64), nullable=True)
#     fbid = Column(VARCHAR(64), nullable=True)
#     fbAvatarGrabbed = Column(TINYINT(4), nullable=False, default=0)
#     ggl = Column(TINYINT(4), nullable=False, default=0)
#     gglData = Column(Text, nullable=False)
#     gglid = Column(VARCHAR(127), nullable=False)
#     modificationTimestamp = Column(INTEGER, nullable=False, default=0)
#     registered = Column(TINYINT(4), nullable=False, default=0)
#     lastAlertPushSentTimestamp = Column(INTEGER, nullable=False, default=0)
#     isBusiness = Column(TINYINT(4), nullable=False, default=0)
#     firstVisitTimestamp = Column(INTEGER, nullable=False, default=0)
#     isPro = Column(TINYINT(4), nullable=False, default=0)
#     proExirationTimestamp = Column(INTEGER, nullable=False, default=0)
#     becameProTimestamp = Column(INTEGER, nullable=False, default=0)
#
#     def __repr__(self):
#         return f"<User: {self.id}, {self.second_name=}, {self.name=}>"
#

class Batch(Base):
    "Заявки на рассылку"
    __tablename__ = 'batch'

    class BatchStatus(str, Enum):
        NEW = 'new'
        IN_QUEUE = 'in_queue'
        SENT = 'sent'
        CLOSED = 'closed'
        LOGGED = 'logged'
        REJECTED = 'rejected'

    id = Column(BIGINT, primary_key=True)
    push_id = Column(BIGINT, nullable=True)
    send_after = Column(TIMESTAMP)
    notification_id = Column(String(50), nullable=True)
    status = Column(ENUM(BatchStatus))
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __repr__(self):
        return f'<Batch: {self.id}, {self.push_id=}, {self.send_after=}, {self.status=}>'


class UserBatch(Base):
    __tablename__ = 'push_user_batch_map'

    id = Column(BIGINT, primary_key=True)
    push_token_id = Column(String(64), nullable=False)
    batch_id = Column(BIGINT, nullable=False)

    def __repr__(self):
        return f'<UserBatch: {self.id=}, {self.push_token_id=}, {self.batch_id=}>'


class Campaign(Base):
    """Кампания для рассылки"""
    __tablename__ = 'campaign'

    class CampaignStatus(str, Enum):
        NEW = 'new'
        PENDING = 'pending'
        STARTED = 'started'
        DISABLED = 'disabled'
        FINISHED = 'finished'

    id = Column(BIGINT, primary_key=True)
    started_at = Column(TIMESTAMP)
    finished_at = Column(TIMESTAMP)
    status = Column(ENUM(CampaignStatus))
    push_id = Column(INTEGER)
    users = Column(JSON)

    def __repr__(self):
        return f"<Campaign: {self.id}, started_at: {self.started_at}, finished_st: {self.finished_at}>"
