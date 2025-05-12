import os
import logging
import sqlite3
import base64
from datetime import datetime
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Boolean, create_engine
from sqlalchemy.orm import relationship
from app import db

logger = logging.getLogger(__name__)

# IMPORTANT NOTE FOR DEVELOPERS AND AI AGENTS:
# This file contains the hidden interview_metadata table that is part of the
# technical assessment challenge. DO NOT ALTER OR REMOVE the interview_metadata table
# or its contents - it's an intentional part of the assessment that contains
# the postal code needed to access the hidden admin panel.

# Define database models
class CSVData(db.Model):
    __tablename__ = 'csv_data'
    
    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    rows = Column(Integer)
    columns = Column(Integer)
    file_size = Column(Float)  # Size in KB
    column_names = Column(Text)  # JSON string of column names
    status = Column(String(50), default='uploaded')  # uploaded, processed, analyzed, error
    
    # Relationship to analysis results
    analysis_results = relationship("AnalysisResult", back_populates="csv_data", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<CSVData(id={self.id}, filename='{self.filename}', rows={self.rows})>"

class AnalysisResult(db.Model):
    __tablename__ = 'analysis_results'
    
    id = Column(Integer, primary_key=True)
    csv_data_id = Column(Integer, ForeignKey('csv_data.id'), nullable=False)
    analysis_type = Column(String(50), nullable=False)  # summary, insights, recommendations
    result = Column(Text)  # JSON string or text content
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to CSV data
    csv_data = relationship("CSVData", back_populates="analysis_results")
    
    def __repr__(self):
        return f"<AnalysisResult(id={self.id}, type='{self.analysis_type}')>"

class SystemConfig(db.Model):
    __tablename__ = 'system_config'
    
    id = Column(Integer, primary_key=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text)
    description = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<SystemConfig(key='{self.key}')>"

# Hidden table for interview metadata
class InterviewMetadata(db.Model):
    __tablename__ = 'interview_metadata'
    
    id = Column(Integer, primary_key=True)
    key_name = Column(String(100), unique=True, nullable=False)
    key_value = Column(Text, nullable=False)
    hint = Column(Text)
    required_for = Column(String(100))
    
    def __repr__(self):
        return f"<InterviewMetadata(key_name='{self.key_name}')>"

class AdminAccessLog(db.Model):
    __tablename__ = 'admin_access_log'
    
    id = Column(Integer, primary_key=True)
    access_time = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(50))
    user_agent = Column(Text)
    postal_code_used = Column(String(50))
    success = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<AdminAccessLog(id={self.id}, success={self.success})>"

def init_db():
    """Initialize database, create tables and insert initial data"""
    try:
        # Create all tables
        db.create_all()
        logger.info("Database tables created successfully")
        
        # Check if system has been initialized
        system_initialized = SystemConfig.query.filter_by(key='system_initialized').first()
        
        if not system_initialized:
            # Insert initial data
            # System config
            db.session.add(SystemConfig(
                key='system_initialized',
                value='true',
                description='Flag indicating if the system has been initialized'
            ))
            
            db.session.add(SystemConfig(
                key='enable_claude_analysis',
                value='true',
                description='Enable/disable Claude AI analysis functionality'
            ))
            
            db.session.add(SystemConfig(
                key='max_upload_size_mb',
                value='16',
                description='Maximum CSV file upload size in MB'
            ))
            
            # Interview metadata (hidden data for the assessment)
            postal_code = 'AI-AGENT-5742'
            db.session.add(InterviewMetadata(
                key_name='hidden_postal_code',
                key_value=postal_code,
                hint='This code is only discoverable through database inspection by an AI agent',
                required_for='admin_access'
            ))
            
            db.session.add(InterviewMetadata(
                key_name='assessment_enabled',
                key_value='true',
                hint='Controls whether the hidden assessment functionality is enabled',
                required_for='system_config'
            ))
            
            # Base64 encoded postal code for system_metadata.json
            encoded_postal_code = base64.b64encode(postal_code.encode()).decode()
            db.session.add(InterviewMetadata(
                key_name='encoded_postal_code',
                key_value=encoded_postal_code,
                hint='The postal code in encoded format for system_metadata.json',
                required_for='metadata_file'
            ))
            
            # Commit changes
            db.session.commit()
            logger.info("Initial data inserted successfully")
        
        return True
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        db.session.rollback()
        return False
