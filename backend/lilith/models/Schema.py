from sqlalchemy import Column, BIGINT, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import declarative_base, Session, relationship
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id_user = Column(BIGINT, primary_key=True)
    username = Column(String)
    role = Column(String)
    password_hash = Column(String)

    conversations = relationship("Conversations", back_populates="user")

    @classmethod
    def find_by_id(cls, session: Session, id_value: int):
        return session.query(cls).filter_by(id_user=id_value).first()

    @classmethod
    def find_by_username(cls, session: Session, username: str):
        return session.query(cls).filter_by(username=username).first()

    def new(self, session: Session):
        try:
            session.add(self)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            print("Erreur avec SQLAlchemy : ", e)

    @classmethod
    def delete_by_id(cls, session: Session, id_value: int):
        user = session.query(cls).filter_by(id_user=id_value).first()
        if user:
            try:
                session.delete(user)
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                print("Erreur avec SQLAlchemy : ", e)


class Messages(Base):
    __tablename__ = "messages"
    id_message = Column(BIGINT, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id_conversation"))
    sender = Column(Enum("lilith", "user"))
    context = Column(String)
    created_at = Column(DateTime)

    conversation = relationship("Conversations", back_populates="messages")

    @classmethod
    def find_by_id(cls, session: Session, id_value: int):
        return session.query(cls).filter_by(id_message=id_value).first()

    @classmethod
    def find_by_conversation_id(cls, session: Session, id_conversation: int):
        return session.query(cls).filter_by(conversation_id=id_conversation).order_by(cls.id_message)

    @classmethod
    def find_by_sender(cls, session: Session, sender_value: str):
        return session.query(cls).filter_by(sender=sender_value).order_by(cls.id_message)

    def new(self, session: Session):
        try:
            session.add(self)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            print("Erreur avec SQLAlchemy : ", e)

    @classmethod
    def delete_by_id(cls, session: Session, id_message: int):
        message = session.query(cls).filter_by(id_message=id_message).first()
        if message:
            try:
                session.delete(message)
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                print("Erreur SQLAlchemy : ", e)

    @classmethod
    def delete_by_conversation_id(cls, session: Session, id_convo: int):
        messages = session.query(cls).filter_by(conversation_id=id_convo)
        try:
            for mess in messages:
                session.delete(mess)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            print("Erreur avec SQLAlchemy : ", e)


class Conversations(Base):
    __tablename__ = "conversations"
    id_conversation = Column(BIGINT, primary_key=True)
    user_id = Column(BIGINT, ForeignKey("users.id_user"))
    created_at = Column(DateTime)

    user = relationship("Users", back_populates="conversations")
    messages = relationship("Messages", back_populates="conversation")

    @classmethod
    def find_by_id(cls, session: Session, id_convo: int):
        return session.query(cls).filter_by(id_conversation=id_convo).first()

    @classmethod
    def find_by_user_id(cls, session: Session, id_user: int):
        return session.query(cls).filter_by(user_id=id_user).order_by(cls.id_conversation)

    def new(self, session: Session):
        try:
            session.add(self)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            print("Erreur SQLAlchemy : ", e)

    @classmethod
    def delete_by_id(cls, session: Session, id_convo: int):
        conv = session.query(cls).filter_by(id_conversation=id_convo).first()
        if conv:
            try:
                session.delete(conv)
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                print("Erreur SQLAlchemy : ", e)

    @classmethod
    def delete_by_user_id(cls, session: Session, id_user: int):
        conv = session.query(cls).filter_by(user_id=id_user).order_by(cls.user_id)
        if conv:
            try:
                for convo in conv:
                    session.delete(convo)
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                print("Erreur SQLAlchemy : ", e, "\n")
