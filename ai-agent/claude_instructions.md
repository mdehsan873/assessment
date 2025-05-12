# Claude Integration Instructions

## Overview
This document provides instructions for integrating the Anthropic Claude API with the CSV Analysis Tool. The application leverages Claude's capabilities to analyze CSV data and provide insights.

## API Setup
To integrate Claude with the application:

1. **API Key**: Obtain an API key from the Anthropic Console (https://console.anthropic.com/)
2. **Environment Variable**: Set the `ANTHROPIC_API_KEY` environment variable with your API key
3. **Model Selection**: The application uses the Claude 3.5 Sonnet model by default

## Prompt Engineering
For effective CSV analysis, prompts should follow these guidelines:

1. **Clear Context**: Provide Claude with clear information about the CSV data
2. **Specific Instructions**: Be explicit about the type of analysis needed
3. **Data Inclusion**: Include relevant metadata and sample data
4. **Output Format**: Specify the desired output format
5. **Token Management**: Be aware of token limitations, especially for large CSV files

## Sample Prompts

### Basic Summary Prompt
