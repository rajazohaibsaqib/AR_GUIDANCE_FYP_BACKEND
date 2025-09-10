from sqlalchemy import String, Integer, Column, Float, ForeignKey,Boolean
from sqlalchemy.orm import relationship
from database import Base


class UserPreference(Base):
    __tablename__ = 'user_preference'

    pre_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.user_id'),unique=True, nullable=False)
    peripheral_threshold = Column(Float)
    distance_threshold = Column(Float)
    distance_status= Column(Boolean)
    peripheral_status = Column(Boolean)
    color_status = Column(Boolean)
    volume_intensity=Column(String(255))
    text_size= Column(String(255))
    swap_red_blue= Column(String(255))
    swap_green_yellow = Column(String(255))
    swap_yellow_white = Column(String(255))
    user=relationship('User',back_populates='preference')

    def __init__(self,user_id,peripheral_threshold,distance_threshold,distance_status,peripheral_status,color_status,volume_intensity,text_size,swap_red_blue,swap_green_yellow,swap_yellow_white):
        self.user_id=user_id
        self.peripheral_threshold=peripheral_threshold
        self.distance_threshold=distance_threshold
        self.distance_status=distance_status
        self.peripheral_status=peripheral_status
        self.color_status=color_status
        self.volume_intensity=volume_intensity
        self.text_size=text_size
        self.swap_red_blue=swap_red_blue
        self.swap_yellow_white=swap_yellow_white
        self.swap_green_yellow=swap_green_yellow