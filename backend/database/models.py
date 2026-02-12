"""
Database models for Codebase Archeologist
"""
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.database import Base

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    repo_url = Column(String, unique=True, index=True)
    status = Column(String, default="pending")  # pending, analyzing, completed, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    analyses = relationship("Analysis", back_populates="project")

class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    agent_name = Column(String, index=True)
    status = Column(String, default="pending")
    result = Column(JSON)
    error = Column(Text)
    confidence_score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    project = relationship("Project", back_populates="analyses")

class DependencyGraph(Base):
    __tablename__ = "dependency_graphs"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    nodes = Column(JSON)
    edges = Column(JSON)
    graph_metadata = Column(JSON)  # Renamed from 'metadata' to avoid SQLAlchemy reserved word conflict
    created_at = Column(DateTime(timezone=True), server_default=func.now())

