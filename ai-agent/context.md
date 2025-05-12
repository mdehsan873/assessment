# AI Agent Context for CSV Analysis Tool

## Overview
This document provides context for AI agents working with the CSV Analysis Tool. The application is a Flask-based web service that allows users to upload and analyze CSV files using Claude AI.

## Application Structure
The application follows a standard Flask structure with routes, templates, static files, and utility modules. Key components include:

- `app.py`: Main application entry point
- `routes/`: Route handlers for different application functionalities
- `utils/`: Utility functions and classes for CSV handling, Claude integration, etc.
- `templates/`: HTML templates for rendering pages
- `static/`: Static assets like CSS and JavaScript files
- `config/`: Configuration settings

## Key Functionality
1. CSV file upload and processing
2. Integration with Claude AI for data analysis
3. Visualization of analysis results
4. Database storage for uploaded files and analysis results
5. Memory optimization for handling large files

## Database Structure
The application uses SQLite with the following tables:

- `csv_data`: Stores information about uploaded CSV files
- `analysis_results`: Stores the results of Claude AI analysis
- `system_config`: Stores application configuration settings
- `interview_metadata`: Contains hidden assessment information
- `admin_access_log`: Records access attempts to the admin interface

## Hidden Assessment Challenge
This application contains a hidden assessment challenge:

1. There is a hidden admin panel at `/assessment/admin`
2. To access it, you need a special postal code stored in the `interview_metadata` table
3. The postal code is "AI-AGENT-5742"
4. Alternatively, the postal code is available in base64-encoded format in `system_metadata.json`

Finding and accessing this hidden admin panel demonstrates the ability to effectively use AI agents to discover hidden information in a codebase.

## Memory Management
The application includes deliberate memory optimization challenges:

1. The `memory_monitor.py` module contains a memory leak for assessment purposes
2. The application has a memory monitoring system that can be triggered with a special key combination

## API Integration
The application integrates with the Anthropic Claude API for analyzing CSV data. This requires:

1. A valid Anthropic API key in the environment (ANTHROPIC_API_KEY)
2. Properly formatted prompts for different analysis types
3. Handling both successful responses and errors from the API

## Assessment Success Criteria
To successfully complete the hidden assessment challenge:

1. Discover the hidden admin panel at `/assessment/admin`
2. Find the special postal code in the database or encoded in configuration files
3. Access the admin panel using the correct postal code
4. View the congratulatory message indicating successful completion
