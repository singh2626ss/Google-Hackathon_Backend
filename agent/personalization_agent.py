"""
Personalization Agent for handling user preferences and customization.
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PersonalizationAgent:
    def __init__(self):
        """Initialize the PersonalizationAgent."""
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing PersonalizationAgent")

    async def get_user_preferences(self, user_id: str) -> Dict:
        """
        Get user preferences and settings.
        
        Args:
            user_id (str): User identifier
            
        Returns:
            Dict: User preferences
        """
        try:
            self.logger.info(f"Getting preferences for user: {user_id}")
            
            # TODO: Implement actual user preferences storage/retrieval
            # For now, return default preferences
            return {
                'user_id': user_id,
                'risk_tolerance': 'moderate',
                'investment_goals': ['growth', 'income'],
                'time_horizon': '5-10 years',
                'preferred_sectors': ['technology', 'healthcare'],
                'report_preferences': {
                    'frequency': 'weekly',
                    'format': 'detailed',
                    'notifications': True
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting user preferences: {str(e)}")
            raise

    async def update_user_preferences(self, user_id: str, preferences: Dict) -> Dict:
        """
        Update user preferences.
        
        Args:
            user_id (str): User identifier
            preferences (Dict): New preferences to update
            
        Returns:
            Dict: Updated user preferences
        """
        try:
            self.logger.info(f"Updating preferences for user: {user_id}")
            
            # TODO: Implement actual user preferences storage/update
            # For now, just return the updated preferences
            updated_preferences = {
                'user_id': user_id,
                'timestamp': datetime.now().isoformat(),
                **preferences
            }
            
            self.logger.info(f"Preferences updated: {updated_preferences}")
            return updated_preferences
            
        except Exception as e:
            self.logger.error(f"Error updating user preferences: {str(e)}")
            raise

    async def get_customized_report(self, user_id: str, report_data: Dict) -> Dict:
        """
        Get a customized report based on user preferences.
        
        Args:
            user_id (str): User identifier
            report_data (Dict): Base report data
            
        Returns:
            Dict: Customized report
        """
        try:
            self.logger.info(f"Generating customized report for user: {user_id}")
            
            # Get user preferences
            preferences = await self.get_user_preferences(user_id)
            
            # Customize report based on preferences
            customized_report = {
                'timestamp': datetime.now().isoformat(),
                'user_id': user_id,
                'report_data': self._customize_report_sections(report_data, preferences),
                'preferences_used': preferences
            }
            
            self.logger.info("Customized report generated successfully")
            return customized_report
            
        except Exception as e:
            self.logger.error(f"Error generating customized report: {str(e)}")
            raise

    def _customize_report_sections(self, report_data: Dict, preferences: Dict) -> Dict:
        """
        Customize report sections based on user preferences.
        
        Args:
            report_data (Dict): Base report data
            preferences (Dict): User preferences
            
        Returns:
            Dict: Customized report sections
        """
        try:
            customized_sections = {}
            
            # Customize based on report format preference
            if preferences['report_preferences']['format'] == 'detailed':
                customized_sections = report_data
            else:
                # Simplified format
                customized_sections = {
                    'summary': report_data['portfolio_summary'],
                    'key_metrics': {
                        'performance': report_data['performance_analysis'],
                        'risk': report_data['risk_analysis']
                    },
                    'recommendations': report_data['recommendations']
                }
            
            # Filter sectors based on preferences
            if 'preferred_sectors' in preferences:
                customized_sections['sector_analysis'] = self._filter_sectors(
                    report_data.get('sector_analysis', {}),
                    preferences['preferred_sectors']
                )
            
            return customized_sections
            
        except Exception as e:
            self.logger.error(f"Error customizing report sections: {str(e)}")
            raise

    def _filter_sectors(self, sector_analysis: Dict, preferred_sectors: List[str]) -> Dict:
        """
        Filter sector analysis to show only preferred sectors.
        
        Args:
            sector_analysis (Dict): Full sector analysis
            preferred_sectors (List[str]): List of preferred sectors
            
        Returns:
            Dict: Filtered sector analysis
        """
        try:
            return {
                sector: data
                for sector, data in sector_analysis.items()
                if sector.lower() in [s.lower() for s in preferred_sectors]
            }
            
        except Exception as e:
            self.logger.error(f"Error filtering sectors: {str(e)}")
            raise

# Create the ADK tool
@FunctionTool
def get_user_preferences_tool(user_id: str) -> Dict:
    """ADK tool for getting user preferences."""
    logger.info("User preferences tool called")
    agent = PersonalizationAgent()
    return agent.get_user_preferences(user_id)

@FunctionTool
def update_user_preferences_tool(user_id: str, preferences: Dict) -> Dict:
    """ADK tool for updating user preferences."""
    logger.info("Update user preferences tool called")
    agent = PersonalizationAgent()
    return agent.update_user_preferences(user_id, preferences)

@FunctionTool
def get_customized_report_tool(user_id: str, report_data: Dict) -> Dict:
    """ADK tool for getting customized reports."""
    logger.info("Customized report tool called")
    agent = PersonalizationAgent()
    return agent.get_customized_report(user_id, report_data)

# Create the ADK agent
personalization_agent = LlmAgent(
    name="personalization_agent",
    description="Generates personalized investment recommendations.",
    tools=[get_user_preferences_tool, update_user_preferences_tool, get_customized_report_tool],
)
