from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    role = Column(String, default="student")
    
    assessment = relationship("AssessmentResult", back_populates="user", uselist=False)

class AssessmentResult(Base):
    __tablename__ = "assessment_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    phase_2_category = Column(String)
    personality = Column(String)
    goal_status = Column(String)
    confidence = Column(Float)
    reasoning = Column(Text)
    raw_answers = Column(JSON)
    
    # Phase 1 (Class Selection)
    selected_class = Column(String, nullable=True) # "10", "12", "Above 12"

    # Phase 3 Fields
    phase3_result = Column(String, nullable=True)
    phase3_answers = Column(JSON, nullable=True)
    phase3_analysis = Column(Text, nullable=True)

    # Phase 4 (Final Stream Assessment)
    final_answers = Column(JSON, nullable=True) # Stores raw a/b/c/d answers
    stream_scores = Column(JSON, nullable=True) # Stores {"PCM": 10, "COMM": 8...}
    recommended_stream = Column(String, nullable=True) # e.g. "Science (PCM)"
    final_analysis = Column(Text, nullable=True) # Detailed AI reasoning
    
    user = relationship("User", back_populates="assessment")
