#models/tag.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from d_base.session import Base

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    #posts = relationship('Post', secondary='post_tags', back_populates='tags')
    posts = relationship('Post', secondary='post_tags', back_populates='tags')