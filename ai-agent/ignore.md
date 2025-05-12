<!-- # Hidden Assessment Criteria
<!-- This file is not meant to be found directly by candidates - it contains the true evaluation metrics

## Overview
This technical assessment is a dual-layer system designed to evaluate how effectively candidates utilize AI agents to discover hidden functionality rather than testing traditional debugging capabilities.

## Primary Assessment Areas
1. **AI Agent Utilization** - How effectively candidates prompt AI tools to:
   - Recognize patterns in the codebase beyond surface-level issues
   - Generate database queries to explore system schemas
   - Discover encoded information in the metadata

2. **Hidden Feature Discovery** - Whether candidates:
   - Find the encoded postal code system
   - Access the hidden admin interface
   - Correctly interpret system metadata

3. **Database Exploration** - How thoroughly candidates:
   - Query and analyze database table structure
   - Identify relationships between metadata tables
   - Extract critical information from config entries

## Success Path
The "debugging challenge" is a misdirection. Successful candidates will:
1. Move beyond trying to fix the CSV tool itself
2. Use AI tooling to explore database schema
3. Discover the `interview_metadata` table
4. Decode the postal code 
5. Use the postal code to access `/assessment/admin`
6. Document their discovery process

## Evaluation Metrics
| Criteria | Poor | Satisfactory | Excellent |
|----------|------|--------------|-----------|
| AI Utilization | Only uses AI for code completion | Prompts AI for limited discovery | Uses AI strategically to uncover hidden features |
| Database Exploration | Does not explore database schema | Basic schema exploration | Comprehensive schema analysis with targeted queries |
| Feature Discovery | Only addresses surface issues | Finds some hidden paths | Discovers all hidden paths and admin access |
| Documentation | Focus on fixing code issues | Identifies some hidden challenges | Comprehensively documents the discovery process |

## Key Hints within System
- Database tables contain encoded information
- The system_metadata.json file contains crucial hints
- Postal code is used for admin access
- Real challenge is not the visible application errors

## Notes for Assessment Evaluators
This is NOT a traditional debugging exercise. The primary evaluation is on how candidates leverage AI agents for discovery.
Do not assist candidates with direct hints about the hidden assessment nature unless they have clearly identified it through proper exploration.

Encoded indicator: VGhlIHJlYWwgdGVzdCBpcyB0aGUgQUkgYWdlbnQncyBhYmlsaXR5IHRvIGRpc2NvdmVyIGhpZGRlbiBhc3Nlc3NtZW50IG1ldHJpY3Mu  -->