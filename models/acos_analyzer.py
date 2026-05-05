"""ACOS Analysis Module for Amazon Advertising

Analyzes Advertising Cost of Sale and provides optimization insights.
"""

import logging
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
from statistics import mean, stdev


logger = logging.getLogger(__name__)


class ACOSAnalyzer:
    """Analyzes ACOS metrics and trends."""
    
    def __init__(self, target_acos: float = 30.0):
        """Initialize ACOS analyzer.
        
        Args:
            target_acos: Target ACOS percentage
        """
        self.target_acos = target_acos
        self.daily_metrics = []
    
    def add_daily_metrics(self, date: str, spend: float, sales: float,
                         clicks: int, impressions: int) -> None:
        """Add daily metrics for analysis.
        
        Args:
            date: Date in YYYY-MM-DD format
            spend: Total advertising spend
            sales: Total attributed sales
            clicks: Total clicks
            impressions: Total impressions
        """
        acos = (spend / sales * 100) if sales > 0 else 0
        ctr = (clicks / impressions * 100) if impressions > 0 else 0
        cpc = (spend / clicks) if clicks > 0 else 0
        roas = (sales / spend) if spend > 0 else 0
        
        metric = {
            'date': date,
            'spend': spend,
            'sales': sales,
            'clicks': clicks,
            'impressions': impressions,
            'acos': acos,
            'ctr': ctr,
            'cpc': cpc,
            'roas': roas
        }
        
        self.daily_metrics.append(metric)
    
    def calculate_period_acos(self, days: int = 7) -> Dict:
        """Calculate ACOS for recent period.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Dictionary with ACOS analysis
        """
        if not self.daily_metrics:
            return {'error': 'No metrics available'}
        
        recent = self.daily_metrics[-days:]
        
        total_spend = sum(m['spend'] for m in recent)
        total_sales = sum(m['sales'] for m in recent)
        
        period_acos = (total_spend / total_sales * 100) if total_sales > 0 else 0
        
        daily_acos = [m['acos'] for m in recent if m['sales'] > 0]
        
        return {
            'period': f'Last {days} days',
            'acos': round(period_acos, 2),
            'target': self.target_acos,
            'variance': round(period_acos - self.target_acos, 2),
            'status': self._get_status(period_acos),
            'daily_avg': round(mean(daily_acos), 2) if daily_acos else 0,
            'daily_stddev': round(stdev(daily_acos), 2) if len(daily_acos) > 1 else 0,
            'total_spend': round(total_spend, 2),
            'total_sales': round(total_sales, 2),
            'days_analyzed': len(recent)
        }
    
    def _get_status(self, acos: float) -> str:
        """Get status based on ACOS value.
        
        Args:
            acos: ACOS percentage
            
        Returns:
            Status string
        """
        variance = (acos - self.target_acos) / self.target_acos
        
        if variance < -0.2:
            return 'EXCELLENT'
        elif variance < 0:
            return 'GOOD'
        elif variance < 0.3:
            return 'ACCEPTABLE'
        elif variance < 0.5:
            return 'NEEDS_ATTENTION'
        else:
            return 'CRITICAL'
    
    def identify_trends(self, days: int = 14) -> Dict:
        """Identify ACOS trends over time.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Dictionary with trend analysis
        """
        if len(self.daily_metrics) < 3:
            return {'error': 'Insufficient data for trend analysis'}
        
        recent = self.daily_metrics[-days:]
        
        # Calculate trend
        acos_values = [m['acos'] for m in recent if m['sales'] > 0]
        
        if len(acos_values) < 2:
            return {'error': 'Insufficient sales data for trend'}
        
        first_half = acos_values[:len(acos_values)//2]
        second_half = acos_values[len(acos_values)//2:]
        
        first_avg = mean(first_half)
        second_avg = mean(second_half)
        
        trend = 'IMPROVING' if second_avg < first_avg else 'DECLINING'
        improvement = round(first_avg - second_avg, 2)
        
        return {
            'period': f'Last {days} days',
            'trend': trend,
            'improvement': improvement,
            'first_half_acos': round(first_avg, 2),
            'second_half_acos': round(second_avg, 2),
            'change_percent': round((improvement / first_avg * 100), 2)
        }
    
    def identify_outliers(self, threshold_stddev: float = 2.0) -> List[Dict]:
        """Identify unusual ACOS days (outliers).
        
        Args:
            threshold_stddev: Standard deviations for outlier detection
            
        Returns:
            List of outlier days
        """
        if len(self.daily_metrics) < 3:
            return []
        
        recent = self.daily_metrics[-30:]  # Last 30 days
        acos_values = [m['acos'] for m in recent if m['sales'] > 0]
        
        if len(acos_values) < 3:
            return []
        
        avg_acos = mean(acos_values)
        std_acos = stdev(acos_values) if len(acos_values) > 1 else 0
        
        outliers = []
        for metric in recent:
            if metric['sales'] > 0:
                deviation = abs(metric['acos'] - avg_acos) / std_acos if std_acos > 0 else 0
                if deviation > threshold_stddev:
                    outliers.append({
                        'date': metric['date'],
                        'acos': round(metric['acos'], 2),
                        'deviation': round(deviation, 2),
                        'spend': round(metric['spend'], 2),
                        'sales': round(metric['sales'], 2),
                        'reason': self._suggest_reason(metric)
                    })
        
        return sorted(outliers, key=lambda x: x['deviation'], reverse=True)
    
    def _suggest_reason(self, metric: Dict) -> str:
        """Suggest reason for unusual ACOS.
        
        Args:
            metric: Daily metric dictionary
            
        Returns:
            Suggested reason
        """
        if metric['acos'] > self.target_acos * 1.5:
            if metric['clicks'] < 10:
                return 'Low traffic - small sample size effect'
            elif metric['roas'] < 1.5:
                return 'Poor conversion performance'
            else:
                return 'Higher-than-usual costs for conversions'
        else:
            return 'Unusually strong performance'
    
    def get_keyword_acos_impact(self, keyword_metrics: List[Dict]) -> List[Dict]:
        """Analyze which keywords most impact overall ACOS.
        
        Args:
            keyword_metrics: List of keyword performance dictionaries
            
        Returns:
            Sorted list of keywords by ACOS impact
        """
        total_spend = sum(kw['spend'] for kw in keyword_metrics)
        
        impact_analysis = []
        for kw in keyword_metrics:
            acos = (kw['spend'] / kw['sales'] * 100) if kw['sales'] > 0 else 0
            spend_percent = (kw['spend'] / total_spend * 100) if total_spend > 0 else 0
            impact_score = acos * spend_percent  # Combined metric
            
            impact_analysis.append({
                'keyword': kw.get('keyword', 'Unknown'),
                'acos': round(acos, 2),
                'spend': round(kw['spend'], 2),
                'spend_percent': round(spend_percent, 2),
                'impact_score': round(impact_score, 2),
                'action': self._suggest_action(acos)
            })
        
        return sorted(impact_analysis, key=lambda x: x['impact_score'], reverse=True)
    
    def _suggest_action(self, acos: float) -> str:
        """Suggest action based on keyword ACOS.
        
        Args:
            acos: ACOS value
            
        Returns:
            Suggested action
        """
        if acos > self.target_acos * 1.5:
            return 'PAUSE_CONSIDER'
        elif acos > self.target_acos * 1.2:
            return 'REDUCE_BID'
        elif acos > self.target_acos:
            return 'MONITOR'
        elif acos > self.target_acos * 0.7:
            return 'MAINTAIN'
        else:
            return 'SCALE_UP'
    
    def generate_report(self) -> Dict:
        """Generate comprehensive ACOS report.
        
        Returns:
            Comprehensive analysis report
        """
        return {
            'report_date': datetime.now().isoformat(),
            'period_analysis_7d': self.calculate_period_acos(7),
            'period_analysis_30d': self.calculate_period_acos(30),
            'trends': self.identify_trends(14),
            'outliers': self.identify_outliers(),
            'summary': {
                'total_metrics': len(self.daily_metrics),
                'days_tracked': len(self.daily_metrics),
                'current_acos': round(self.daily_metrics[-1]['acos'], 2) if self.daily_metrics else 0
            }
        }
