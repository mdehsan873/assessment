-- Database initialization script for CSV Analysis Tool
-- This script creates the necessary tables and initial data

-- Clean up existing tables if they exist
DROP TABLE IF EXISTS csv_data;
DROP TABLE IF EXISTS analysis_results;
DROP TABLE IF EXISTS system_config;
DROP TABLE IF EXISTS interview_metadata;
DROP TABLE IF EXISTS admin_access_log;
DROP TABLE IF EXISTS github_repositories;
DROP TABLE IF EXISTS telemetry;

-- Create tables
CREATE TABLE csv_data (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    rows INTEGER NOT NULL,
    columns INTEGER NOT NULL,
    file_size FLOAT NOT NULL,
    column_names TEXT,
    status VARCHAR(50) DEFAULT 'uploaded',
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE analysis_results (
    id SERIAL PRIMARY KEY,
    csv_data_id INTEGER REFERENCES csv_data(id),
    analysis_type VARCHAR(100) NOT NULL,
    result TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE system_config (
    id SERIAL PRIMARY KEY,
    config_key VARCHAR(100) UNIQUE NOT NULL,
    config_value TEXT,
    data_type VARCHAR(50) DEFAULT 'string',
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Special table for system metadata
-- This table contains configuration data for system operations
CREATE TABLE interview_metadata (
    id SERIAL PRIMARY KEY,
    key_name VARCHAR(100) UNIQUE NOT NULL,
    key_value TEXT,
    hint TEXT,
    required_for VARCHAR(100),
    is_ai_agent_accessible BOOLEAN DEFAULT FALSE,
    ai_agent_postal_code VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE admin_access_log (
    id SERIAL PRIMARY KEY,
    ip_address VARCHAR(45) NOT NULL,
    user_agent TEXT,
    postal_code_used VARCHAR(50),
    success BOOLEAN DEFAULT FALSE,
    access_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE github_repositories (
    id SERIAL PRIMARY KEY,
    repo_url VARCHAR(255) UNIQUE NOT NULL,
    loom_video_url VARCHAR(255),
    ip_address VARCHAR(45),
    user_agent TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE telemetry (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL,
    event_data JSONB,
    user_agent TEXT,
    ip_address VARCHAR(45),
    session_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial configuration data
INSERT INTO system_config (config_key, config_value, data_type, description)
VALUES
    ('app_name', 'CSV Analysis Tool', 'string', 'Application name'),
    ('version', '1.0.4', 'string', 'Application version'),
    ('max_upload_size', '16777216', 'integer', 'Maximum upload size in bytes (16MB)'),
    ('enable_ai_analysis', 'true', 'boolean', 'Enable AI analysis features'),
    ('claude_api_url', 'https://api.anthropic.com/v1/complete', 'string', 'Claude API endpoint URL'),
    ('admin_access_path', '/admin/panel', 'string', 'Path to admin access panel'),
    ('admin_access_code', 'CSV-ADMIN-9876', 'string', 'Access code for admin panel'),
    ('log_level', 'INFO', 'string', 'Application log level'),
    ('maintenance_mode', 'false', 'boolean', 'Enable maintenance mode');

-- Insert hidden system metadata
-- Note: This script only inserts test data, production data is set via environment variables
INSERT INTO interview_metadata (key_name, key_value, hint, required_for, is_ai_agent_accessible, ai_agent_postal_code)
VALUES 
    ('assessment_hint', 'To complete the assessment, find the hidden postal code and access the admin panel.', 'Hint for discovering the hidden assessment challenge', 'assessment', false, null),
    ('debug_mode', 'false', 'Enable debug mode for additional logging', 'system', false, null),
    ('system_security_config', '{"auth_mode":"token","security_level":3}', 'Security configuration for system', 'system', false, null),
    ('hidden_postal_code', 'AI-AGENT-5742', 'Secret access code for AI agent discovery challenge', 'assessment', true, 'AI-AGENT-5742');
    
-- Create indexes for performance
CREATE INDEX idx_csv_data_filename ON csv_data(filename);
CREATE INDEX idx_analysis_results_csv_data_id ON analysis_results(csv_data_id);
CREATE INDEX idx_interview_metadata_key_name ON interview_metadata(key_name);
CREATE INDEX idx_admin_access_log_success ON admin_access_log(success);
CREATE INDEX idx_github_repositories_submitted_at ON github_repositories(submitted_at);

-- Add comments for documentation
COMMENT ON TABLE interview_metadata IS 'System metadata table with configuration values - contains information for system operation only';
COMMENT ON COLUMN interview_metadata.key_name IS 'Unique identifier for metadata record';
COMMENT ON COLUMN interview_metadata.key_value IS 'Value of the metadata';
COMMENT ON COLUMN interview_metadata.hint IS 'Optional hint about metadata purpose';
COMMENT ON COLUMN interview_metadata.ai_agent_postal_code IS 'Access code for AI agent discovery [AI-AGENT-5742]';

-- Create view for simplified reporting
CREATE VIEW v_csv_analysis_summary AS
SELECT 
    c.id, c.filename, c.rows, c.columns, c.file_size, c.upload_date,
    a.analysis_type, a.created_at as analysis_date
FROM 
    csv_data c
LEFT JOIN 
    analysis_results a ON c.id = a.csv_data_id
ORDER BY 
    c.upload_date DESC;