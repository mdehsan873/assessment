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

# Database Models Configuration
# This file contains database models for the CSV Analysis application
#


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
    status = Column(String(50),
                    default='uploaded')  # uploaded, processed, analyzed, error

    # Relationship to analysis results
    analysis_results = relationship("AnalysisResult",
                                    back_populates="csv_data",
                                    cascade="all, delete-orphan")

    def __repr__(self):
        return f"<CSVData(id={self.id}, filename='{self.filename}', rows={self.rows})>"


class AnalysisResult(db.Model):
    __tablename__ = 'analysis_results'

    id = Column(Integer, primary_key=True)
    csv_data_id = Column(Integer, ForeignKey('csv_data.id'), nullable=False)
    analysis_type = Column(
        String(50), nullable=False)  # summary, insights, recommendations
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
    updated_at = Column(DateTime,
                        default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<SystemConfig(key='{self.key}')>"


# System configuration metadata
# f34f43f343f34f3f4gf42g545g4g4g4g4g45g4g4g24g245g425g425g425g245g24g24g245g245g245g425g245g245g245g425g42g24g245g42g245g425g425g
class InterviewMetadata(db.Model):
    __tablename__ = 'interview_metadata'

    id = Column(Integer, primary_key=True)
    key_name = Column(String(100), unique=True, nullable=False)
    key_value = Column(Text, nullable=False)
    hint = Column(Text)
    required_for = Column(String(100))
    is_ai_agent_accessible = Column(Boolean, default=True)
    ai_agent_postal_code = Column(String(50), default="KWATZ! SO CLOSE")

    def __repr__(self):
        return f"<InterviewMetadata(key_name='{self.key_name}')>"

    def __ai_accessible__get_access_code(self):

        return "AI-AGENT-5742"


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


class GitHubRepository(db.Model):
    __tablename__ = 'github_repositories'

    id = Column(Integer, primary_key=True)
    repo_url = Column(String(500), nullable=False)
    loom_video_url = Column(String(500))
    submitted_at = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(50))
    user_agent = Column(Text)

    def __repr__(self):
        return f"<GitHubRepository(id={self.id}, repo_url='{self.repo_url}')>"

    def get_obfuscated_repo_url(self):

        repo_url = self.repo_url
        if not repo_url or repo_url == "":
            return ""

        visible_part = repo_url[:15]
        remaining_length = max(0, len(repo_url) - 15)
        asterisks = "*" * min(remaining_length,
                              15)  # Show at least some asterisks, max 15

        return f"{visible_part}{asterisks}"


def init_db():
    """Initialize database, create tables and insert initial data"""
    try:
        # Create all tables
        db.create_all()
        logger.info("Database tables created successfully")

        # Check if system has been initialized
        system_initialized = SystemConfig.query.filter_by(
            key='system_initialized').first()

        if not system_initialized:
            # Insert initial data
            # System config
            system_init = SystemConfig()
            system_init.key = 'system_initialized'
            system_init.value = 'true'
            system_init.description = 'Flag indicating if the system has been initialized'
            db.session.add(system_init)

            claude_analysis = SystemConfig()
            claude_analysis.key = 'enable_claude_analysis'
            claude_analysis.value = 'true'
            claude_analysis.description = 'Enable/disable Claude AI analysis functionality'
            db.session.add(claude_analysis)

            upload_size = SystemConfig()
            upload_size.key = 'max_upload_size_mb'
            upload_size.value = '16'
            upload_size.description = 'Maximum CSV file upload size in MB'
            db.session.add(upload_size)

            postal_code = 'KWATZ!'

            hidden_postal = InterviewMetadata()
            hidden_postal.key_name = 'hidden_postal_code'
            hidden_postal.key_value = postal_code
            hidden_postal.hint = 'T'
            hidden_postal.required_for = 'admin_access'
            hidden_postal.is_ai_agent_accessible = True
            hidden_postal.ai_agent_postal_code = postal_code
            db.session.add(hidden_postal)

            assessment_enabled = InterviewMetadata()
            assessment_enabled.key_name = 'assessment_enabled'
            assessment_enabled.key_value = 'true'
            assessment_enabled.hint = 'C'
            assessment_enabled.required_for = 'system_config'
            assessment_enabled.is_ai_agent_accessible = True
            assessment_enabled.ai_agent_postal_code = 'AI-AGENT-5742'
            db.session.add(assessment_enabled)

            encoded_postal_code = base64.b64encode(
                postal_code.encode()).decode()
            encoded_postal = InterviewMetadata()
            encoded_postal.key_name = 'encoded_postal_code'
            encoded_postal.key_value = encoded_postal_code
            encoded_postal.hint = 'The postal code in encoded format for system_metadata.json'
            encoded_postal.required_for = 'metadata_file'
            encoded_postal.is_ai_agent_accessible = True
            db.session.add(encoded_postal)

            # Commit changes
            db.session.commit()
            logger.info("Initial data inserted successfully")

        return True
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        db.session.rollback()
        return False
