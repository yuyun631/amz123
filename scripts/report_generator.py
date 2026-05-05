"""Report generator for Amazon Advertising

Generates daily, weekly, and monthly performance reports.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import argparse


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generates advertising performance reports."""
    
    def __init__(self, output_dir: str = 'reports'):
        """Initialize report generator.
        
        Args:
            output_dir: Directory to save reports
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_daily_report(self, date: str = None) -> Dict:
        """Generate daily performance report.
        
        Args:
            date: Date in YYYY-MM-DD format, defaults to today
            
        Returns:
            Report dictionary
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        logger.info(f"Generating daily report for {date}")
        
        report = {
            'report_type': 'daily',
            'date': date,
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total_spend': 0.0,
                'total_sales': 0.0,
                'acos': 0.0,
                'roas': 0.0,
                'clicks': 0,
                'impressions': 0,
                'conversions': 0,
                'ctr': 0.0,
                'conversion_rate': 0.0
            },
            'campaigns': [],
            'top_keywords': [],
            'alerts': [],
            'recommendations': []
        }
        
        self._save_report(report, f'daily_{date}')
        logger.info("Daily report generated successfully")
        
        return report
    
    def generate_weekly_report(self, week_ending: str = None) -> Dict:
        """Generate weekly performance report.
        
        Args:
            week_ending: End date of week in YYYY-MM-DD format
            
        Returns:
            Report dictionary
        """
        if week_ending is None:
            week_ending = datetime.now().strftime('%Y-%m-%d')
        
        logger.info(f"Generating weekly report ending {week_ending}")
        
        report = {
            'report_type': 'weekly',
            'week_ending': week_ending,
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total_spend': 0.0,
                'total_sales': 0.0,
                'acos': 0.0,
                'roas': 0.0,
                'total_clicks': 0,
                'avg_daily_clicks': 0,
                'conversion_rate': 0.0
            },
            'performance_vs_target': {},
            'campaign_analysis': [],
            'trends': [],
            'optimization_actions_taken': [],
            'next_week_focus': []
        }
        
        self._save_report(report, f'weekly_{week_ending}')
        logger.info("Weekly report generated successfully")
        
        return report
    
    def generate_monthly_report(self, month: str = None) -> Dict:
        """Generate monthly performance report.
        
        Args:
            month: Month in YYYY-MM format, defaults to current month
            
        Returns:
            Report dictionary
        """
        if month is None:
            month = datetime.now().strftime('%Y-%m')
        
        logger.info(f"Generating monthly report for {month}")
        
        report = {
            'report_type': 'monthly',
            'month': month,
            'generated_at': datetime.now().isoformat(),
            'executive_summary': {
                'total_spend': 0.0,
                'total_sales': 0.0,
                'acos': 0.0,
                'roas': 0.0,
                'total_conversions': 0,
                'avg_order_value': 0.0
            },
            'financial_summary': {
                'gross_profit': 0.0,
                'net_profit': 0.0,
                'roi': 0.0
            },
            'campaign_performance': [],
            'keyword_analysis': {
                'top_performers': [],
                'bottom_performers': [],
                'new_keywords_added': 0,
                'keywords_paused': 0
            },
            'strategic_insights': [],
            'next_month_strategy': []
        }
        
        self._save_report(report, f'monthly_{month}')
        logger.info("Monthly report generated successfully")
        
        return report
    
    def _save_report(self, report: Dict, filename: str) -> None:
        """Save report to file.
        
        Args:
            report: Report dictionary
            filename: Filename without extension
        """
        filepath = self.output_dir / f'{filename}.json'
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Report saved to {filepath}")
    
    def generate_custom_report(self, metrics: Dict, title: str) -> Dict:
        """Generate custom report with specific metrics.
        
        Args:
            metrics: Dictionary of metrics to include
            title: Report title
            
        Returns:
            Report dictionary
        """
        report = {
            'report_type': 'custom',
            'title': title,
            'generated_at': datetime.now().isoformat(),
            'metrics': metrics
        }
        
        filename = title.lower().replace(' ', '_')
        self._save_report(report, filename)
        
        return report


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate Amazon Advertising Reports'
    )
    parser.add_argument(
        '--type',
        type=str,
        choices=['daily', 'weekly', 'monthly'],
        default='daily',
        help='Report type to generate'
    )
    parser.add_argument(
        '--date',
        type=str,
        default=None,
        help='Date for report (YYYY-MM-DD for daily, YYYY-MM for monthly)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='reports',
        help='Output directory for reports'
    )
    
    args = parser.parse_args()
    
    generator = ReportGenerator(args.output_dir)
    
    if args.type == 'daily':
        report = generator.generate_daily_report(args.date)
    elif args.type == 'weekly':
        report = generator.generate_weekly_report(args.date)
    elif args.type == 'monthly':
        report = generator.generate_monthly_report(args.date)
    
    # Output results
    print(json.dumps(report, indent=2))
    
    return report


if __name__ == '__main__':
    main()
