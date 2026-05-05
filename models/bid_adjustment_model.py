"""Bid Adjustment Model for Amazon Advertising

Core logic for optimizing keyword bids based on performance metrics.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


logger = logging.getLogger(__name__)


@dataclass
class KeywordPerformance:
    """Represents keyword performance metrics."""
    keyword: str
    current_bid: float
    clicks: int
    impressions: int
    conversions: int
    spend: float
    sales: float
    quality_score: int = 5
    days_active: int = 7
    match_type: str = "exact"
    
    def calculate_metrics(self) -> Dict[str, float]:
        """Calculate derived metrics."""
        ctr = (self.clicks / self.impressions * 100) if self.impressions > 0 else 0
        cpc = (self.spend / self.clicks) if self.clicks > 0 else 0
        conversion_rate = (self.conversions / self.clicks * 100) if self.clicks > 0 else 0
        acos = (self.spend / self.sales * 100) if self.sales > 0 else 0
        roas = (self.sales / self.spend) if self.spend > 0 else 0
        
        return {
            'ctr': ctr,
            'cpc': cpc,
            'conversion_rate': conversion_rate,
            'acos': acos,
            'roas': roas
        }


class BidAdjustmentModel:
    """Model for intelligent bid adjustments based on performance."""
    
    def __init__(self, config_path: str = 'config/settings.json'):
        """Initialize bid adjustment model.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.adjustment_history = []
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file not found: {config_path}. Using defaults.")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Return default configuration."""
        return {
            'target_acos': 30.0,
            'min_bid': 0.10,
            'max_bid': 10.00,
            'max_daily_change': 0.15,
            'min_clicks_for_adjustment': 30,
            'min_days_active': 7,
            'roas_multiplier': 1.2
        }
    
    def recommend_adjustment(self, keyword_perf: KeywordPerformance) -> Dict:
        """Generate bid adjustment recommendation.
        
        Args:
            keyword_perf: KeywordPerformance object with current metrics
            
        Returns:
            Dictionary with adjustment recommendation and rationale
        """
        metrics = keyword_perf.calculate_metrics()
        recommendation = {
            'keyword': keyword_perf.keyword,
            'current_bid': keyword_perf.current_bid,
            'new_bid': keyword_perf.current_bid,
            'adjustment_percent': 0.0,
            'rationale': [],
            'action': 'MAINTAIN',
            'confidence': 0.0
        }
        
        # Check minimum requirements for adjustment
        if keyword_perf.clicks < self.config['min_clicks_for_adjustment']:
            recommendation['rationale'].append(
                f"Insufficient clicks ({keyword_perf.clicks} < {self.config['min_clicks_for_adjustment']}). "
                "Requires learning period."
            )
            recommendation['confidence'] = 0.3
            return recommendation
        
        if keyword_perf.days_active < self.config['min_days_active']:
            recommendation['rationale'].append(
                f"Campaign too new ({keyword_perf.days_active} < {self.config['min_days_active']} days). "
                "Allowing learning period."
            )
            recommendation['confidence'] = 0.4
            return recommendation
        
        # Quality Score Adjustment
        if keyword_perf.quality_score < 5:
            recommendation['rationale'].append(
                f"Low quality score ({keyword_perf.quality_score}/10). "
                "Recommend keyword review and optimization."
            )
            recommendation['new_bid'] = self._apply_adjustment(
                keyword_perf.current_bid, -0.20
            )
            recommendation['adjustment_percent'] = -0.20
            recommendation['action'] = 'REDUCE'
            recommendation['confidence'] = 0.7
            return recommendation
        
        # ACOS-based adjustment
        target_acos = self.config['target_acos']
        actual_acos = metrics['acos']
        
        if actual_acos > target_acos * 1.3:  # Significantly above target
            adjustment = self._calculate_acos_adjustment(
                actual_acos, target_acos, metrics['conversion_rate']
            )
            recommendation['rationale'].append(
                f"ACOS ({actual_acos:.1f}%) significantly above target ({target_acos:.1f}%). "
                f"Conversion rate: {metrics['conversion_rate']:.2f}%"
            )
            recommendation['new_bid'] = self._apply_adjustment(
                keyword_perf.current_bid, adjustment
            )
            recommendation['adjustment_percent'] = adjustment
            recommendation['action'] = 'REDUCE'
            recommendation['confidence'] = 0.85
            
        elif actual_acos > target_acos:
            adjustment = -0.05  # Modest reduction
            recommendation['rationale'].append(
                f"ACOS ({actual_acos:.1f}%) above target ({target_acos:.1f}%). "
                "Modest bid reduction recommended."
            )
            recommendation['new_bid'] = self._apply_adjustment(
                keyword_perf.current_bid, adjustment
            )
            recommendation['adjustment_percent'] = adjustment
            recommendation['action'] = 'REDUCE'
            recommendation['confidence'] = 0.75
            
        else:  # ACOS below target
            # Check ROAS for scaling opportunity
            if metrics['roas'] > self.config['roas_multiplier']:
                adjustment = 0.10  # Increase for scaling
                recommendation['rationale'].append(
                    f"Strong performance: ACOS ({actual_acos:.1f}%) below target, "
                    f"ROAS ({metrics['roas']:.2f}x) strong. Increase bid to scale volume."
                )
                recommendation['new_bid'] = self._apply_adjustment(
                    keyword_perf.current_bid, adjustment
                )
                recommendation['adjustment_percent'] = adjustment
                recommendation['action'] = 'INCREASE'
                recommendation['confidence'] = 0.80
            else:
                recommendation['rationale'].append(
                    f"Performance within target: ACOS ({actual_acos:.1f}%), "
                    f"ROAS ({metrics['roas']:.2f}x). Maintain current bid."
                )
                recommendation['action'] = 'MAINTAIN'
                recommendation['confidence'] = 0.9
        
        # Enforce bid limits
        recommendation['new_bid'] = self._enforce_bid_limits(
            recommendation['new_bid']
        )
        
        # Record adjustment
        self._record_adjustment(recommendation)
        
        return recommendation
    
    def _calculate_acos_adjustment(self, actual: float, target: float, 
                                   conversion_rate: float) -> float:
        """Calculate bid adjustment based on ACOS gap.
        
        Args:
            actual: Actual ACOS
            target: Target ACOS
            conversion_rate: Current conversion rate
            
        Returns:
            Adjustment percentage (-1.0 to 0.0 for reductions)
        """
        acos_gap = (actual - target) / target
        
        # Scale adjustment by conversion rate (more aggressive if conversion is good)
        if conversion_rate > 5.0:
            multiplier = 0.5
        elif conversion_rate > 2.0:
            multiplier = 0.7
        else:
            multiplier = 1.0
        
        adjustment = -min(acos_gap * multiplier, 0.30)
        return max(adjustment, -0.20)  # Cap at -20%
    
    def _apply_adjustment(self, current_bid: float, adjustment: float) -> float:
        """Apply adjustment percentage to bid.
        
        Args:
            current_bid: Current bid amount
            adjustment: Adjustment percentage (-1.0 to 1.0)
            
        Returns:
            New bid amount
        """
        return current_bid * (1 + adjustment)
    
    def _enforce_bid_limits(self, bid: float) -> float:
        """Enforce minimum and maximum bid limits.
        
        Args:
            bid: Proposed bid
            
        Returns:
            Bid within allowed limits
        """
        bid = max(bid, self.config['min_bid'])
        bid = min(bid, self.config['max_bid'])
        # Round to nearest cent
        return round(bid, 2)
    
    def _record_adjustment(self, recommendation: Dict) -> None:
        """Record adjustment in history.
        
        Args:
            recommendation: Adjustment recommendation
        """
        self.adjustment_history.append({
            'timestamp': datetime.now().isoformat(),
            **recommendation
        })
    
    def batch_recommend(self, keywords: List[KeywordPerformance]) -> List[Dict]:
        """Generate recommendations for multiple keywords.
        
        Args:
            keywords: List of KeywordPerformance objects
            
        Returns:
            List of adjustment recommendations
        """
        return [self.recommend_adjustment(kw) for kw in keywords]
    
    def filter_by_confidence(self, recommendations: List[Dict], 
                            min_confidence: float = 0.7) -> List[Dict]:
        """Filter recommendations by confidence threshold.
        
        Args:
            recommendations: List of recommendations
            min_confidence: Minimum confidence level (0-1)
            
        Returns:
            Filtered list of recommendations
        """
        return [r for r in recommendations 
                if r['confidence'] >= min_confidence]
    
    def get_adjustment_summary(self) -> Dict:
        """Get summary of recent adjustments.
        
        Returns:
            Summary statistics
        """
        if not self.adjustment_history:
            return {'total_adjustments': 0}
        
        recent = self.adjustment_history[-100:]  # Last 100 adjustments
        
        increases = sum(1 for a in recent if a['action'] == 'INCREASE')
        decreases = sum(1 for a in recent if a['action'] == 'REDUCE')
        maintains = sum(1 for a in recent if a['action'] == 'MAINTAIN')
        
        return {
            'total_adjustments': len(recent),
            'increases': increases,
            'decreases': decreases,
            'maintains': maintains,
            'avg_confidence': sum(a['confidence'] for a in recent) / len(recent)
        }
