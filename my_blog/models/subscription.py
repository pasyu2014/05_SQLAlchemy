#models/subscription.py
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from d_base.session import Base

class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))

    user = relationship('User', back_populates='subscriptions')
    post = relationship('Post', back_populates='subscriptions')
    # задает уникальность сочетания двух полей: `user_id` и `post_id`
    __table_args__ = (UniqueConstraint('user_id', 'post_id', name='uix_user_post'),)