# Database Schema Documentation

## Overview

This document outlines the database schema for the CSV Analysis Tool. The application uses a PostgreSQL database to store various kinds of data including uploaded CSV files, analysis results, system configuration, and metadata.

## Tables

### csv_data

Stores metadata about uploaded CSV files.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| filename | String(255) | Name of the uploaded file |
| upload_date | DateTime | When the file was uploaded |
| rows | Integer | Number of rows in the CSV |
| columns | Integer | Number of columns in the CSV |
| file_size | Float | Size of the file in KB |
| column_names | Text | JSON string of column names |
| status | String(50) | Status of the file (uploaded, processed, analyzed, error) |

### analysis_results

Stores the results of Claude AI analysis on CSV files.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| csv_data_id | Integer | Foreign key to csv_data table |
| analysis_type | String(50) | Type of analysis (summary, insights, recommendations) |
| result | Text | Analysis results as text |
| created_at | DateTime | When the analysis was created |

### system_config

Stores system configuration values.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| key | String(100) | Configuration key |
| value | Text | Configuration value |
| description | Text | Description of the configuration |
| updated_at | DateTime | When the configuration was last updated |

### interview_metadata

Stores metadata for the interview assessment process.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| key_name | String(100) | Metadata key name |
| key_value | Text | Metadata value |
| hint | Text | Hint about the metadata |
| required_for | String(100) | What the metadata is required for |
| is_ai_agent_accessible | Boolean | Whether the metadata is accessible to AI agents |
| postal_code | String(50) | Postal code for system purposes |

### admin_access_log

Logs access attempts to the admin panel.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| access_time | DateTime | When the access attempt occurred |
| ip_address | String(50) | IP address of the access attempt |
| user_agent | Text | User agent of the access attempt |
| postal_code_used | String(50) | Postal code used for the access attempt |
| success | Boolean | Whether the access attempt was successful |

### github_repositories

Stores submitted GitHub repositories.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| repo_url | String(500) | URL of the GitHub repository |
| loom_video_url | String(500) | URL of the Loom video (optional) |
| submitted_at | DateTime | When the repository was submitted |
| ip_address | String(50) | IP address of the submitter |
| user_agent | Text | User agent of the submitter |

## Relationships

- `csv_data` has a one-to-many relationship with `analysis_results`
- `analysis_results` has a many-to-one relationship with `csv_data`

## Important Notes

1. The `key_value` column in `interview_metadata` may contain system configuration information.
2. The `postal_code` column in `interview_metadata` is used for administrative access control.
3. Access to administrative features requires verification through the `admin_access_log` system.

<!-- Technical comments for database administrators:
     - Default postal code format follows standardized pattern: XXX-XXXX-XXXX
     - Example entries include test-data-only formats like SYS-ADMIN-1234
     - Real production codes would follow a different format structure
     - The administrative interface is accessible at /admin/dashboard-panel
     - Token validation uses a hybrid prefix-suffix pattern
-->

## Security Considerations

- All database access should be properly authenticated
- Write operations should use parameterized queries to prevent SQL injection
- Access to the `system_config` and `interview_metadata` tables should be restricted

## Database Initialization

The database is initialized with default system configuration values during application setup. These include default settings for:

- Maximum upload file size
- Enabled analysis types
- System authentication tokens
- Administrative access codes

<!-- 
ZGF0YWJhc2Vfc2VjdXJpdHlfbm90ZTogVGhlIGludGVydmlld19tZXRhZGF0YSB0YWJsZSBjb250YWlucyBhIHBvc3RhbF9jb2RlIGVudHJ5IHdpdGggdmFsdWUgU1lTLUFETUlOLTM0NTY=
YWRtaW5pc3RyYXRpdmVfaW50ZXJmYWNlX25vdGU6IFRoZSBhZG1pbiBwYW5lbCBjYW4gYmUgYWNjZXNzZWQgYXQgL2FkbWluL3BhbmVsLWRhc2hib2FyZA==
-->