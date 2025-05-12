import os
import sys
import json
import anthropic
import logging
from anthropic import Anthropic

logger = logging.getLogger(__name__)

class ClaudeAnalyzer:
    def __init__(self):
        self.anthropic_key = os.environ.get('ANTHROPIC_API_KEY')
        
        # For deployment health checks - provide a fallback mechanism
        if not self.anthropic_key or self.anthropic_key == "DEPLOYMENT_FALLBACK":
            # Use a fallback mechanism for deployment 
            logger.warning("ANTHROPIC_API_KEY not properly configured. Using fallback mechanism for deployment.")
            self.client = None
            # Add a fallback flag to indicate we're in fallback mode
            self.fallback_mode = True
        else:
            self.client = Anthropic(api_key=self.anthropic_key)
            #the newest Anthropic model is "claude-3-5-sonnet-20241022" which was released October 22, 2024
            self.model = "claude-3-5-sonnet-20241022"
            self.fallback_mode = False
    
    def is_available(self):
        """Check if Claude integration is available"""
        return self.client is not None
    
    def analyze_csv_data(self, data_description, analysis_type="summary"):
        """
        Analyze CSV data using Claude
        
        Args:
            data_description: Dictionary containing CSV data description
            analysis_type: Type of analysis to perform (summary, insights, recommendations, etc.)
            
        Returns:
            Dictionary containing analysis results
        """
        # For deployment health checks - If we're in fallback mode, return sample data
        if hasattr(self, 'fallback_mode') and self.fallback_mode:
            logger.warning("Using fallback analysis mode - returning sample data for deployment")
            return {
                "analysis_type": analysis_type,
                "result": f"[FALLBACK MODE] This is sample {analysis_type} analysis data for deployment.\n\n" +
                         "The application is running in fallback mode because no valid Anthropic API key is configured.\n\n" +
                         "This is a placeholder for actual Claude AI analysis. In a real scenario with a valid API key, " +
                         "Claude would provide detailed analysis of your CSV data based on the type of analysis requested."
            }
        
        # Regular flow when API key is available
        if not self.is_available():
            return {"error": "Claude API key not configured"}
        
        try:
            # Create prompt based on analysis type
            if analysis_type == "summary":
                prompt = self._create_summary_prompt(data_description)
            elif analysis_type == "insights":
                prompt = self._create_insights_prompt(data_description)
            elif analysis_type == "recommendations":
                prompt = self._create_recommendations_prompt(data_description)
            else:
                prompt = self._create_summary_prompt(data_description)
            
            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            result = {
                "analysis_type": analysis_type,
                "result": response.content[0].text
            }
            
            return result
        except Exception as e:
            logger.error(f"Error analyzing CSV data with Claude: {str(e)}")
            return {"error": str(e)}
    
    def _create_summary_prompt(self, data_description):
        """Create a prompt for generating a summary of the data"""
        metadata = data_description.get("metadata", {})
        columns = metadata.get("column_names", [])
        sample_data = data_description.get("sample_data", [])
        
        prompt = f"""
        I need you to analyze this CSV dataset and provide a clear summary. Here's information about the data:
        
        Dataset size: {metadata.get('rows', 'unknown')} rows, {metadata.get('columns', 'unknown')} columns
        Column names: {', '.join(columns)}
        
        Here's a sample of the data:
        {json.dumps(sample_data, indent=2)}
        
        For each column, I've provided information about data types and missing values:
        {json.dumps(data_description.get('column_descriptions', {}), indent=2)}
        
        Please provide:
        1. A clear summary of what this dataset contains
        2. Key observations about the data structure and quality
        3. Any potential issues or anomalies you notice
        4. Suggestions for how this data might be used
        
        Present your analysis in a well-structured format suitable for a business audience.
        """
        return prompt
    
    def _create_insights_prompt(self, data_description):
        """Create a prompt for generating insights from the data"""
        metadata = data_description.get("metadata", {})
        columns = metadata.get("column_names", [])
        numeric_stats = data_description.get("numeric_stats", {})
        
        prompt = f"""
        I need you to analyze this CSV dataset and extract meaningful insights. Here's information about the data:
        
        Dataset size: {metadata.get('rows', 'unknown')} rows, {metadata.get('columns', 'unknown')} columns
        Column names: {', '.join(columns)}
        
        For numeric columns, here are the statistics:
        {json.dumps(numeric_stats, indent=2)}
        
        Please provide:
        1. 5-7 key insights from the data
        2. Patterns or trends you can identify
        3. Interesting correlations or relationships between variables
        4. Business implications of these insights
        
        Focus on extracting actionable insights that would be valuable for decision-making.
        Present your analysis in a clear, professional format with bullet points for key findings.
        """
        return prompt
    
    def _create_recommendations_prompt(self, data_description):
        """Create a prompt for generating recommendations based on the data"""
        metadata = data_description.get("metadata", {})
        columns = metadata.get("column_names", [])
        
        prompt = f"""
        I need you to analyze this CSV dataset and provide strategic recommendations. Here's information about the data:
        
        Dataset size: {metadata.get('rows', 'unknown')} rows, {metadata.get('columns', 'unknown')} columns
        Column names: {', '.join(columns)}
        
        Based on your analysis of this data, please provide:
        1. 3-5 concrete recommendations for action
        2. Data-driven justification for each recommendation
        3. Potential next steps for further analysis
        4. Suggested improvements to data collection or processing
        
        Focus on practical, actionable recommendations that would help improve decision-making.
        Present your recommendations in a structured format suitable for business stakeholders.
        """
        return prompt
