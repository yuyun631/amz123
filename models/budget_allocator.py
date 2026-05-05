"""Budget Allocation Model for Amazon Advertising

Optimizes budget distribution across campaigns and ad groups.
"""

import logging
from typing import Dict, List
from datetime import datetime


logger = logging.getLogger(__name__)


class BudgetAllocator:
    """Allocates and optimizes advertising budget."""
    
    def __init__(self, total_daily_budget: float):
        """Initialize budget allocator.
        
        Args:
            total_daily_budget: Total daily advertising budget
        """
        self.total_daily_budget = total_daily_budget
        self.campaign_budgets = {}
        self.allocation_history = []
    
    def allocate_proportional(self, campaigns: List[Dict]) -> Dict[str, float]:
        """Allocate budget proportional to campaign performance.
        
        Args:
            campaigns: List of campaign dictionaries with metrics
            
        Returns:
            Dictionary mapping campaign names to allocated budgets
        """
        if not campaigns:
            return {}
        
        # Calculate performance scores
        scores = {}
        for campaign in campaigns:
            score = self._calculate_campaign_score(campaign)
            scores[campaign['name']] = score
        
        # Normalize scores
        total_score = sum(scores.values())
        
        if total_score == 0:
            # Equal distribution if no score
            per_campaign = self.total_daily_budget / len(campaigns)
            return {c['name']: per_campaign for c in campaigns}
        
        # Allocate based on normalized scores
        allocation = {}
        for campaign in campaigns:
            campaign_name = campaign['name']
            proportion = scores[campaign_name] / total_score
            allocation[campaign_name] = round(
                self.total_daily_budget * proportion, 2
            )
        
        self._record_allocation(allocation)
        return allocation
    
    def allocate_performance_based(self, campaigns: List[Dict],
                                   target_acos: float = 30.0) -> Dict[str, float]:
        """Allocate budget based on ACOS and ROI.
        
        Args:
            campaigns: List of campaign dictionaries
            target_acos: Target ACOS percentage
            
        Returns:
            Dictionary mapping campaign names to allocated budgets
        """
        allocation = {}
        allocatable_budget = self.total_daily_budget
        
        # Sort campaigns by performance tier
        performing = []  # ACOS below target
        acceptable = []  # ACOS within 20% of target
        underperforming = []  # ACOS above 120% of target
        
        for campaign in campaigns:
            acos = campaign.get('acos', target_acos)
            if acos < target_acos:
                performing.append(campaign)
            elif acos < target_acos * 1.2:
                acceptable.append(campaign)
            else:
                underperforming.append(campaign)
        
        # Allocate to each tier
        # Tier 1: Strong performers get 50-60%
        tier1_budget = allocatable_budget * 0.55
        if performing:
            per_campaign = tier1_budget / len(performing)
            for campaign in performing:
                allocation[campaign['name']] = round(per_campaign, 2)
        
        # Tier 2: Acceptable get 30-35%
        tier2_budget = allocatable_budget * 0.32
        if acceptable:
            per_campaign = tier2_budget / len(acceptable)
            for campaign in acceptable:
                allocation[campaign['name']] = round(per_campaign, 2)
        
        # Tier 3: Underperformers get 5-15%
        tier3_budget = allocatable_budget * 0.13
        if underperforming:
            per_campaign = tier3_budget / len(underperforming)
            for campaign in underperforming:
                allocation[campaign['name']] = round(per_campaign, 2)
        
        self._record_allocation(allocation)
        return allocation
    
    def allocate_roas_optimized(self, campaigns: List[Dict]) -> Dict[str, float]:
        """Allocate budget to maximize ROAS.
        
        Args:
            campaigns: List of campaign dictionaries
            
        Returns:
            Dictionary mapping campaign names to allocated budgets
        """
        if not campaigns:
            return {}
        
        # Calculate ROAS for each campaign
        roas_scores = {}
        for campaign in campaigns:
            roas = campaign.get('roas', 1.0)
            # Apply boost for recent strong performers
            if campaign.get('days_since_optimization', 0) < 3:
                roas *= 1.2
            roas_scores[campaign['name']] = roas
        
        # Normalize ROAS scores
        total_roas = sum(roas_scores.values())
        
        allocation = {}
        for campaign in campaigns:
            proportion = roas_scores[campaign['name']] / total_roas
            allocation[campaign['name']] = round(
                self.total_daily_budget * proportion, 2
            )
        
        self._record_allocation(allocation)
        return allocation
    
    def calculate_campaign_score(self, campaign: Dict) -> float:
        """Calculate overall campaign performance score.
        
        Args:
            campaign: Campaign dictionary with metrics
            
        Returns:
            Performance score (0-100)
        """
        return self._calculate_campaign_score(campaign)
    
    def _calculate_campaign_score(self, campaign: Dict) -> float:
        """Internal method to calculate campaign score.
        
        Args:
            campaign: Campaign dictionary
            
        Returns:
            Weighted performance score
        """
        # Extract metrics with defaults
        acos = campaign.get('acos', 30.0)
        roas = campaign.get('roas', 1.0)
        ctr = campaign.get('ctr', 2.0)
        conversion_rate = campaign.get('conversion_rate', 2.0)
        impressions = campaign.get('impressions', 0)
        
        # Normalize metrics (convert to 0-100 scale)
        # ACOS: target 30%, so 30% = 100 points
        acos_score = max(0, 100 * (30 / acos)) if acos > 0 else 0
        acos_score = min(acos_score, 150)  # Cap at 150
        
        # ROAS: target 3.0x, so 3.0x = 100 points
        roas_score = (roas / 3.0) * 100
        roas_score = min(roas_score, 150)  # Cap at 150
        
        # CTR: industry avg 2%, good is 4%
        ctr_score = (ctr / 4.0) * 100
        ctr_score = min(ctr_score, 150)  # Cap at 150
        
        # Conversion rate: good is 5%
        conversion_score = (conversion_rate / 5.0) * 100
        conversion_score = min(conversion_score, 150)  # Cap at 150
        
        # Volume boost: campaigns with more impressions are more reliable
        volume_multiplier = min(1.2, 1.0 + (impressions / 10000) * 0.01)
        
        # Weighted average
        score = (
            acos_score * 0.35 +
            roas_score * 0.30 +
            ctr_score * 0.20 +
            conversion_score * 0.15
        ) * volume_multiplier
        
        return max(0, score)
    
    def analyze_budget_efficiency(self, campaigns: List[Dict]) -> Dict:
        """Analyze budget efficiency across campaigns.
        
        Args:
            campaigns: List of campaign dictionaries
            
        Returns:
            Efficiency analysis
        """
        if not campaigns:
            return {'error': 'No campaigns provided'}
        
        analysis = {
            'total_budget': self.total_daily_budget,
            'num_campaigns': len(campaigns),
            'campaigns': []
        }
        
        for campaign in campaigns:
            daily_budget = campaign.get('daily_budget', 
                                       self.total_daily_budget / len(campaigns))
            daily_spend = campaign.get('daily_spend', 0)
            efficiency = (daily_spend / daily_budget * 100) if daily_budget > 0 else 0
            
            analysis['campaigns'].append({
                'name': campaign['name'],
                'allocated_budget': round(daily_budget, 2),
                'actual_spend': round(daily_spend, 2),
                'efficiency_percent': round(efficiency, 1),
                'status': self._get_efficiency_status(efficiency),
                'recommendation': self._get_efficiency_recommendation(efficiency)
            })
        
        return analysis
    
    def _get_efficiency_status(self, efficiency: float) -> str:
        """Get budget efficiency status.
        
        Args:
            efficiency: Efficiency percentage
            
        Returns:
            Status string
        """
        if efficiency < 50:
            return 'UNDERSPENDING'
        elif efficiency < 85:
            return 'LOW_SPEND'
        elif efficiency < 100:
            return 'ON_PACE'
        elif efficiency < 120:
            return 'OVER_PACE'
        else:
            return 'SIGNIFICANTLY_OVERSPENDING'
    
    def _get_efficiency_recommendation(self, efficiency: float) -> str:
        """Get recommendation based on efficiency.
        
        Args:
            efficiency: Efficiency percentage
            
        Returns:
            Recommendation
        """
        if efficiency < 50:
            return 'Increase bids to improve spend'
        elif efficiency < 85:
            return 'Monitor pacing, consider increasing bids'
        elif efficiency < 100:
            return 'On track, maintain current settings'
        elif efficiency < 120:
            return 'Monitor for overspending'
        else:
            return 'Reduce bids or budget to control spend'
    
    def _record_allocation(self, allocation: Dict) -> None:
        """Record allocation in history.
        
        Args:
            allocation: Budget allocation dictionary
        """
        self.allocation_history.append({
            'timestamp': datetime.now().isoformat(),
            'allocation': allocation,
            'total_allocated': sum(allocation.values())
        })
    
    def get_allocation_summary(self) -> Dict:
        """Get summary of recent allocations.
        
        Returns:
            Summary of allocation history
        """
        if not self.allocation_history:
            return {'total_allocations': 0}
        
        recent = self.allocation_history[-10:]
        
        return {
            'total_allocations': len(self.allocation_history),
            'recent_allocations': len(recent),
            'avg_budget': sum(
                a['total_allocated'] for a in recent
            ) / len(recent),
            'last_allocation_time': recent[-1]['timestamp'] if recent else None
        }
