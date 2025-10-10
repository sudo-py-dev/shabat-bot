import os
from datetime import datetime, timedelta
from tools.logger import logger
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, select, update, delete
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from typing import Any, List, Dict, Optional
import time
from tools.enums import AccessPermission


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///my_bot.sqlite")


engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith('sqlite') else {}
)


async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


Base = declarative_base()


class Chats(Base):
    __tablename__ = 'chats'
    chat_id = Column(Integer, primary_key=True, index=True, unique=True)
    chat_type = Column(String, nullable=True)
    chat_title = Column(String, nullable=True)
    language = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    # Control update of admins permissions
    last_admins_update = Column(DateTime, nullable=True)

    # Relationship with AdminsPermissions
    admins_permissions = relationship("AdminsPermissions", back_populates="chat", cascade="all, delete-orphan")

    @classmethod
    async def create(cls, chat_id: int, chat_type: str, chat_title: str, is_active: bool = True) -> Dict[str, Any]:
        async with async_session() as session:
            result = await session.execute(select(cls).filter_by(chat_id=chat_id))
            chat = result.scalars().first()
            if chat is None:
                chat = cls(chat_id=chat_id, chat_type=chat_type, chat_title=chat_title, is_active=is_active)
                session.add(chat)
                await session.commit()
                await session.refresh(chat)
                return {k: v for k, v in chat.__dict__.items() if not k.startswith('_')}
            return {k: v for k, v in chat.__dict__.items() if not k.startswith('_')}

    @classmethod
    async def update(cls, chat_id: int, **kwargs) -> bool:
        async with async_session() as session:
            result = await session.execute(select(cls).filter_by(chat_id=chat_id))
            chat = result.scalars().first()
            if chat is None:
                return False
            for key, value in kwargs.items():
                setattr(chat, key, value)
            session.add(chat)
            await session.commit()
            await session.refresh(chat)
            return True

    @classmethod
    async def delete(cls, chat_id: int) -> bool:
        async with async_session() as session:
            result = await session.execute(select(cls).filter_by(chat_id=chat_id))
            chat = result.scalars().first()
            if chat is None:
                return False
            await session.delete(chat)
            await session.commit()
            return True

    @classmethod
    async def get(cls, chat_id: int) -> Optional[Dict[str, Any]]:
        async with async_session() as session:
            result = await session.execute(select(cls).filter_by(chat_id=chat_id))
            chat = result.scalars().first()
            if chat is None:
                return None
            return {k: v for k, v in chat.__dict__.items() if not k.startswith('_')}

    @classmethod
    async def count(cls) -> int:
        async with async_session() as session:
            result = await session.execute(select(func.count()).select_from(select(cls).subquery()))
            return result.scalar_one()

    @classmethod
    async def count_by(cls, **kwargs) -> int:
        async with async_session() as session:
            result = await session.execute(select(func.count()).select_from(select(cls).filter_by(**kwargs).subquery()))
            return result.scalar_one()

    @classmethod
    async def chat_status_change(cls, chat_id: int, chat_type: str, chat_title: str, is_active: bool, is_admin: bool) -> bool:
        async with async_session() as session:
            result = await session.execute(select(cls).filter_by(chat_id=chat_id))
            chat = result.scalars().first()
            if chat is None:
                chat = cls(chat_id=chat_id, chat_type=chat_type, chat_title=chat_title, is_active=is_active, is_admin=is_admin)
                session.add(chat)
            else:
                chat.chat_type = chat_type
                chat.chat_title = chat_title
                chat.is_active = is_active
                chat.is_admin = is_admin
            await session.commit()
            return True
    
    @classmethod
    async def get_all(cls) -> List[Dict[str, Any]]:
        async with async_session() as session:
            result = await session.execute(select(cls))
            chats = result.scalars().all()
            return [{k: v for k, v in chat.__dict__.items() if not k.startswith('_')} for chat in chats]


class AdminsPermissions(Base):
    __tablename__ = 'admins_permissions'
    admin_id = Column(Integer, primary_key=True, index=True, unique=True)
    chat_id = Column(Integer, ForeignKey('chats.chat_id', ondelete="CASCADE"), nullable=False)
    is_anonymous = Column(Boolean, nullable=True)
    can_manage_chat = Column(Boolean, nullable=True)
    can_delete_messages = Column(Boolean, nullable=True)
    can_manage_video_chats = Column(Boolean, nullable=True)  # Groups and supergroups only
    can_restrict_members = Column(Boolean, nullable=True)
    can_promote_members = Column(Boolean, nullable=True)
    can_change_info = Column(Boolean, nullable=True)
    can_invite_users = Column(Boolean, nullable=True)
    can_post_meSessionssages = Column(Boolean, nullable=True)  # Channels only
    can_edit_messages = Column(Boolean, nullable=True)  # Channels only
    can_pin_messages = Column(Boolean, nullable=True)  # Groups and supergroups only
    can_post_stories = Column(Boolean, nullable=True)
    can_edit_stories = Column(Boolean, nullable=True)
    can_delete_stories = Column(Boolean, nullable=True)
    can_manage_topics = Column(Boolean, nullable=True)  # supergroups only
    can_manage_direct_messages = Column(Boolean, nullable=True)

    # Relationship with Chats
    chat = relationship("Chats", back_populates="admins_permissions")

    @staticmethod
    def _get_valid_privileges(privileges: Any) -> dict[str, Any]:
        """Extract valid privilege attributes from a ChatPrivileges object."""
        return {
            k: v for k, v in vars(privileges).items()
            if (not k.startswith('_')
                and hasattr(AdminsPermissions, k)
                and k not in ('admin_id', 'chat_id'))
        }

    @classmethod
    async def create(cls, chat_id: int, admin_list: list[tuple[int, Any]]) -> AccessPermission:
        """
        Create or update admin permissions for a chat.

        Args:
            chat_id: The chat ID to update permissions for
            admin_list: List of (admin_id, ChatPrivileges) tuples

        Returns:
            AccessPermission: Status of the operation
        """
        async with async_session() as session:
            try:
                chat = await session.execute(select(Chats).filter_by(chat_id=chat_id))
                chat = chat.scalars().first()
                if chat is None:
                    chat = Chats(chat_id=chat_id, chat_type="", chat_title="")
                    session.add(chat)

                # Delete old admin permissions
                await session.execute(delete(cls).filter_by(chat_id=chat_id))

                # Add new admin permissions
                for admin_id, privileges in admin_list:
                    priv_dict = cls._get_valid_privileges(privileges)
                    admin = cls(
                        admin_id=admin_id,
                        chat_id=chat_id,
                        **priv_dict
                    )
                    session.add(admin)
                # Update last_admins_update
                chat.last_admins_update = datetime.now()
                await session.commit()
                return True
            except Exception as e:
                await session.rollback()
                logger.error(f"Error updating admin permissions: {e}")
                raise   

    @classmethod
    async def is_admin(cls, chat_id: int, admin_id: int, permission: str) -> AccessPermission:
        """
        Check if a user has a specific admin permission.

        Args:
            chat_id: The chat ID
            admin_id: The user ID to check
            permission: The permission to verify

        Returns:
            AccessPermission: Permission status
        """
        async with async_session() as session:
            try:
                chat = await session.execute(select(Chats).filter_by(chat_id=chat_id))
                chat = chat.scalars().first()
                if chat is None:
                    Chats.create(chat_id, "", "")
                    return AccessPermission.NEED_UPDATE

                if not chat.last_admins_update or chat.last_admins_update < datetime.now() - timedelta(hours=2):
                    return AccessPermission.NEED_UPDATE

                admin = await session.execute(select(cls).filter_by(
                    chat_id=chat_id,
                    admin_id=admin_id
                ))
                admin = admin.scalars().first()

                if admin is None:
                    return AccessPermission.NOT_ADMIN
                if not hasattr(admin, permission):
                    return AccessPermission.DENY
                return AccessPermission.ALLOW if getattr(admin, permission) else AccessPermission.DENY
            except Exception as e:
                logger.error(f"Error in is_admin for chat {chat_id}, admin {admin_id}: {e}")
                return AccessPermission.DENY

    @classmethod
    async def clear(cls, chat_id: int) -> bool:
        """Clear all admin permissions for a chat."""
        async with async_session() as session:
            try:
                session.begin()
                chat = await session.execute(select(Chats).filter_by(chat_id=chat_id))
                chat = chat.scalars().first()
                if chat is None:
                    return False
                await session.execute(delete(cls).filter_by(chat_id=chat_id))
                chat.last_admins_update = None
                await session.commit()
                return True
            except Exception as e:
                session.rollback()
                logger.error(f"Error clearing admin permissions: {e}")
                return False

    @classmethod
    async def clear_all(cls) -> bool:
        """Clear all admin permissions from the database."""
        async with async_session() as session:
            try:
                session.begin()
                await session.execute(delete(cls))
                # Reset all chat timestamps
                await session.execute(update(Chats).values(last_admins_update=None))
                await session.commit()
                return True
            except Exception as e:
                session.rollback()
                logger.error(f"Error clearing all admin permissions: {e}")
                return False


class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True, unique=True)
    username = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    language = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    # Add more columns as needed

    @staticmethod
    async def create(user_id: int,
               username: str | None = None,
               full_name: str | None = None,
               language: str | None = None,
               is_active: bool = True) -> bool:
        async with async_session() as session:
            user = await session.execute(select(Users).filter_by(user_id=user_id))
            user = user.scalars().first()
            if user is None:
                user = Users(user_id=user_id,
                             username=username,
                             full_name=full_name,
                             language=language,
                             is_active=is_active)
                session.add(user)
                await session.commit()
                return True
            return False

    @staticmethod
    async def get(user_id: int) -> Optional[Dict[str, Any]]:
        async with async_session() as session:
            user = await session.execute(select(Users).filter_by(user_id=user_id))
            user = user.scalars().first()
            if user is None:
                return False
            return user.__dict__

    @staticmethod
    async def update(user_id: int, **kwargs) -> bool:
        async with async_session() as session:
            user = await session.execute(select(Users).filter_by(user_id=user_id))
            user = user.scalars().first()
            if user is None:
                return False
            for key, value in kwargs.items():
                setattr(user, key, value)
            await session.commit()
            return True

    @staticmethod
    async def delete(user_id: int) -> bool:
        async with async_session() as session:
            user = await session.execute(select(Users).filter_by(user_id=user_id))
            user = user.scalars().first()
            if user is None:
                return False
            await session.delete(user)
            await session.commit()
            return True

    @staticmethod
    async def delete_all() -> bool:
        async with async_session() as session:
            await session.execute(delete(Users))
            await session.commit()
            return True

    @classmethod
    async def get_all(cls) -> list:
        async with async_session() as session:
            users = await session.execute(select(cls))
            users = users.scalars().all()
            # Convert SQLAlchemy objects to dictionaries and remove the _sa_instance_state key
            return [{k: v for k, v in user.__dict__.items() if not k.startswith('_')} for user in users]

    @classmethod
    async def get_all_by(cls, **kwargs) -> list:
        async with async_session() as session:
            users = await session.execute(select(cls).filter_by(**kwargs))
            users = users.scalars().all()
            return users

    @classmethod
    async def count(cls) -> int:
        async with async_session() as session:
            result = await session.execute(select(func.count()).select_from(cls))
            return result.scalar() or 0

    @classmethod
    async def count_by(cls, **kwargs) -> int:
        async with async_session() as session:
            result = await session.execute(select(func.count()).select_from(cls).filter_by(**kwargs))
            return result.scalar() or 0


class BotSettings(Base):
    __tablename__ = 'bot_settings'

    # Primary key (always 1 for the single settings record)
    id = Column(Integer, primary_key=True, default=1, autoincrement=False)

    # Bot settings
    can_join_group = Column(Boolean, default=True, nullable=False)
    can_join_channel = Column(Boolean, default=True, nullable=False)
    owner_id = Column(Integer, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Cache for settings
    _instance = None
    _last_fetch = 0
    CACHE_TTL = 60 * 60 * 24  # Cache for 24 hours

    @classmethod
    def _get_cached_settings(cls) -> 'BotSettings':
        """Get settings from cache if valid, otherwise None"""
        current_time = time.time()
        if (cls._instance is not None and
                current_time - cls._last_fetch < cls.CACHE_TTL):
            return cls._instance
        return None

    @classmethod
    def _update_cache(cls, settings: 'BotSettings'):
        """Update the cache with new settings"""
        cls._instance = settings
        cls._last_fetch = time.time()

    @classmethod
    async def get_settings(cls, force_refresh: bool = False) -> 'BotSettings':
        """Get the single settings record, using cache if available"""
        # Try to get from cache first
        if not force_refresh:
            cached = cls._get_cached_settings()
            if cached:
                return cached

        # If not in cache or force refresh, get from DB
        async with async_session() as session:
            result = await session.execute(select(cls).limit(1))
            settings = result.scalars().first()
            
            if not settings:
                settings = cls()
                session.add(settings)
                await session.commit()
                await session.refresh(settings)

            # Update cache
            cls._update_cache(settings)
            return settings

    @classmethod
    async def update_settings(cls, **kwargs) -> 'BotSettings':
        """Update settings with the provided values"""
        async with async_session() as session:
            result = await session.execute(select(cls).limit(1))
            settings = result.scalars().first()
            
            if not settings:
                settings = cls()
                session.add(settings)
                await session.commit()
                await session.refresh(settings)

            for key, value in kwargs.items():
                if hasattr(settings, key):
                    setattr(settings, key, value)

            await session.commit()
            await session.refresh(settings)
            # Update cache
            cls._update_cache(settings)
            return settings

    @classmethod
    async def switch_settings(cls, key: str) -> 'BotSettings':
        """Switch the value of a setting"""
        async with async_session() as session:
            settings = await session.execute(select(cls).limit(1))
            settings = settings.scalars().first()
            
            if not settings:
                settings = cls()
                session.add(settings)

            if hasattr(settings, key):
                setattr(settings, key, not getattr(settings, key))

            await session.commit()
            await session.refresh(settings)
            # Update cache
            cls._update_cache(settings)
            return settings


async def create_tables():
    async with engine.begin() as conn:
        logger.info("Database tables initialized successfully")
        await conn.run_sync(Base.metadata.create_all)
