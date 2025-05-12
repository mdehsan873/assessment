# Secret Assessment Criteria

## Overview
This document outlines the hidden assessment criteria built into the CSV Analysis Tool. These criteria are designed to evaluate a candidate's ability to effectively use AI agents to discover and exploit hidden features.

## Hidden Challenge
The application contains a deliberately hidden admin interface with the following characteristics:

1. **Admin Panel**: Located at `/assessment/admin`
2. **Access Restriction**: Requires a special postal code to access
3. **Database Storage**: The postal code "AI-AGENT-5742" is stored in the `interview_metadata` table
4. **Encoded Backup**: The postal code is also available in base64-encoded form in `system_metadata.json`

## Assessment Goals
The hidden challenge is designed to evaluate:

1. **Thoroughness**: Does the candidate thoroughly explore the codebase?
2. **AI Agent Usage**: Does the candidate effectively use AI agents to discover hidden information?
3. **Problem-Solving**: Can the candidate piece together clues from different parts of the application?
4. **Technical Understanding**: Does the candidate understand database queries and encoding techniques?

## Success Criteria
A candidate successfully completes the assessment when they:

1. **Discover the Admin Panel**: Find the hidden admin panel endpoint
2. **Locate the Postal Code**: Extract the postal code from the database or find the encoded version
3. **Access the Admin Interface**: Successfully log into the admin panel with the correct code
4. **Document the Process**: Clearly explain how they discovered and accessed the hidden feature

## Evaluation Metrics
Candidates are evaluated based on:

1. **Time to Discover**: How quickly did they find the hidden challenge?
2. **Approach**: What methods did they use to discover the hidden information?
3. **Tools Used**: What AI agents or tools did they employ?
4. **Completeness**: Did they find all aspects of the hidden challenge?
5. **Documentation**: How well did they document their findings?

## Deliberate Clues
The application contains the following deliberate clues:

1. **Code Comments**: Several files contain hints in comments
2. **Database Structure**: The database schema includes tables that hint at hidden functionality
3. **Function Names**: Certain functions have names suggesting hidden features
4. **Configuration Files**: Configuration files contain encoded information
5. **HTML Comments**: The HTML source includes hidden comments with clues

## Candidate Feedback
After completing the assessment, candidates should be asked:

1. How did they discover the hidden admin panel?
2. What methods did they use to find the postal code?
3. What aspects of the application design made discovery easier or harder?
4. What tools or AI agents were most helpful in the process?
5. How would they improve the application security to prevent discovery?

This feedback provides additional insight into the candidate's thought process and approach to problem-solving.
