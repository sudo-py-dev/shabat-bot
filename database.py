import datetime
from pyrogram.types import ChatPermissions
import sqlalchemy
from cachetools import TTLCache
from sqlalchemy import create_engine, Column, Integer, Boolean, DateTime, String
from sqlalchemy.orm import sessionmaker
from tools import is_valid_chat_id
from enums import Messages

triggers_cache = TTLCache(maxsize=1024, ttl=60 * 60)

Base = sqlalchemy.orm.declarative_base()
engine = create_engine("sqlite:///local.db",
                       pool_size=10,
                       max_overflow=20,
                       echo=False,
                       connect_args={
                           "check_same_thread": False,
                           "timeout": 30
                       })

Session = sessionmaker(bind=engine)


class Chats(Base):
    __tablename__ = "chats"
    chat_id = Column(Integer, primary_key=True, unique=True, index=True)
    enabled = Column(Boolean, default=False)
    enabled_at = Column(DateTime, nullable=True)
    temp_message_id = Column(Integer, nullable=True)
    calendar_message = Column(String, nullable=True)
    calendar_message_img = Column(String, nullable=True)
    havdalah_message = Column(String, nullable=True)
    havdalah_message_img = Column(String, nullable=True)

    @staticmethod
    def update_message(chat_id: int, message: str, message_img: str=None, message_type: str="calendar") -> bool:
        with Session() as session:
            chat = session.query(Chats).filter_by(chat_id=chat_id).first()
            if chat is None and is_valid_chat_id(chat_id):
                chat = Chats(chat_id=chat_id)
                session.add(chat)
                session.commit()
            elif chat is None:
                raise ValueError(Messages.invalid_or_not_existing_group.value)
            
            if message_type == "calendar":
                chat.calendar_message = message
                chat.calendar_message_img = message_img
            elif message_type == "havdalah":
                chat.havdalah_message = message
                chat.havdalah_message_img = message_img
            session.commit()
            return True

    @staticmethod
    def enable_shabat(chat_id: int) -> bool:
        with Session() as session:
            chat = session.query(Chats).filter_by(chat_id=chat_id).first()
            if chat is None and is_valid_chat_id(chat_id):
                chat = Chats(chat_id=chat_id)
                session.add(chat)
                session.commit()
            elif chat is None:
                raise ValueError(Messages.invalid_or_not_existing_group.value)
            
            chat.enabled = not chat.enabled
            chat.enabled_at = datetime.datetime.now() if chat.enabled else None
            session.commit()
            return chat.enabled

    @staticmethod
    def delete(chat_id: int) -> bool:
        with Session() as session:
            chat = session.query(Chats).filter_by(chat_id=chat_id).first()
            if chat is None:
                return False
            session.delete(chat)
            session.commit()
            return True

    @staticmethod
    def get(chat_id: int) -> "Chats":
        with Session() as session:
            chat = session.query(Chats).filter_by(chat_id=chat_id).first()
            if chat is None and is_valid_chat_id(chat_id):
                chat = Chats(chat_id=chat_id)
                session.add(chat)
                session.commit()
            elif chat is None:
                raise ValueError("Chat not found or invalid chat id")
            return chat

    @staticmethod
    def get_enabled() -> list["Chats"]:
        with Session() as session:
            chats = session.query(Chats).filter_by(enabled=True).all()
            return chats
    
    @staticmethod
    def update_one(chat_id: int, key: str, value: any) -> bool:
        with Session() as session:
            chat = session.query(Chats).filter_by(chat_id=chat_id).first()
            if chat is None:
                return False
            setattr(chat, key, value)
            session.commit()
            return True


class GroupPermission(Base):
    __tablename__ = 'group_permission'
    chat_id = Column(Integer, primary_key=True, index=True)
    can_send_messages = Column(Boolean, default=True)
    can_send_audios = Column(Boolean, default=True)
    can_send_documents = Column(Boolean, default=True)
    can_send_photos = Column(Boolean, default=True)
    can_send_videos = Column(Boolean, default=True)
    can_send_video_notes = Column(Boolean, default=True)
    can_send_voice_notes = Column(Boolean, default=True)
    can_send_polls = Column(Boolean, default=True)
    can_send_other_messages = Column(Boolean, default=True)
    can_add_web_page_previews = Column(Boolean, default=True)
    can_change_info = Column(Boolean, default=True)
    can_invite_users = Column(Boolean, default=True)
    can_pin_messages = Column(Boolean, default=True)
    can_manage_topics = Column(Boolean, default=True)
    can_send_media_messages = Column(Boolean, default=True)

    @staticmethod
    def update(chat_id: int, permissions: ChatPermissions) -> bool:
        with Session() as session:
            group_permission = session.query(GroupPermission).filter_by(chat_id=chat_id).first()
            if group_permission is None:
                group_permission = GroupPermission(chat_id=chat_id)
                session.add(group_permission)
                session.commit()

            for key, value in permissions.__dict__.items():
                if hasattr(GroupPermission, key):
                    setattr(group_permission, key, value)

            media_permissions = [
                permissions.can_send_photos,
                permissions.can_send_videos,
                permissions.can_send_voice_notes,
                permissions.can_send_video_notes,
                permissions.can_send_documents,
                permissions.can_send_audios
            ]

            group_permission.can_send_media_messages = any(media_permissions)
            session.commit()
            return True

    @staticmethod
    def get(chat_id: int) -> ChatPermissions:
        with Session() as session:
            settings_group = session.query(GroupPermission).filter_by(chat_id=chat_id).first()
            if settings_group is None:
                return ChatPermissions(can_send_messages=True)
            return ChatPermissions(
                can_send_messages=True,
                can_send_audios=settings_group.can_send_audios,
                can_send_documents=settings_group.can_send_documents,
                can_send_photos=settings_group.can_send_photos,
                can_send_videos=settings_group.can_send_videos,
                can_send_video_notes=settings_group.can_send_video_notes,
                can_send_voice_notes=settings_group.can_send_voice_notes,
                can_send_polls=settings_group.can_send_polls,
                can_send_other_messages=settings_group.can_send_other_messages,
                can_add_web_page_previews=settings_group.can_add_web_page_previews,
                can_change_info=settings_group.can_change_info,
                can_invite_users=settings_group.can_invite_users,
                can_pin_messages=settings_group.can_pin_messages,
                can_manage_topics=settings_group.can_manage_topics,
                can_send_media_messages=settings_group.can_send_media_messages,
            )

    @staticmethod
    def delete(chat_id: int) -> bool:
        with Session() as session:
            settings_group = session.query(GroupPermission).filter_by(chat_id=chat_id).first()
            if settings_group is None:
                return False
            session.delete(settings_group)
            session.commit()
            return True


Base.metadata.create_all(engine)