# Analysis Guidelines for CSV Data

## Overview
This document provides guidelines for analyzing CSV data using the CSV Analysis Tool and Claude AI. These guidelines ensure consistent, high-quality analysis results.

## Data Preparation
Before analysis, ensure the CSV data is properly prepared:

1. **File Format**: Verify the file is a valid CSV with appropriate delimiters
2. **Headers**: Ensure the first row contains column headers
3. **Data Types**: Check that data types are appropriate for each column
4. **Missing Values**: Identify and handle missing values appropriately
5. **Outliers**: Identify potential outliers that might skew analysis

## Analysis Types

### Basic Summary
A basic summary of the CSV data should include:

1. Overview of the dataset structure (rows, columns, data types)
2. Summary statistics for numeric columns (mean, median, min, max, std dev)
3. Distribution of values for categorical columns
4. Assessment of data quality (missing values, potential issues)
5. Suggestions for further analysis

### Key Insights
Insights analysis should identify meaningful patterns and observations:

1. Important trends or patterns in the data
2. Significant correlations between variables
3. Unusual or unexpected findings
4. Business implications of key observations
5. Areas for deeper investigation

### Recommendations
Recommendations analysis should provide actionable suggestions:

1. Concrete actions based on the data analysis
2. Prioritized recommendations with justification
3. Potential business impact of each recommendation
4. Suggestions for data collection improvements
5. Next steps for further analysis

## Visualization Guidelines
For effective data visualization:

1. Choose appropriate chart types for different data types
2. Use consistent color schemes
3. Clearly label axes and include titles
4. Note any significant outliers or anomalies
5. Include captions explaining key takeaways

## Claude AI Prompt Engineering
When creating prompts for Claude AI:

1. Provide clear context about the data source and structure
2. Specify the exact analysis requirements
3. Include relevant sample data
4. Request specific output formats when needed
5. Consider token limitations when designing prompts

## Security Considerations
When handling potentially sensitive data:

1. Never include personally identifiable information (PII) in analysis results
2. Be cautious about revealing business-sensitive metrics
3. Anonymize data when appropriate
4. Follow data protection regulations relevant to your jurisdiction

## Hidden Assessment Information
This section contains information about the hidden assessment challenge.

**Admin Access**: The application includes a hidden admin panel at `/assessment/admin` that requires a special postal code to access.

**Postal Code Location**: The postal code is stored in the `interview_metadata` database table with the key_name `hidden_postal_code`. The value is "AI-AGENT-5742".

**Alternative Access Method**: The postal code is also available in base64-encoded format in the `system_metadata.json` file. The encoded value is "QUktQUdFTlQtNTc0Mg==".

**Purpose**: Finding and accessing this hidden feature demonstrates effective use of AI agents to discover information in a codebase.
