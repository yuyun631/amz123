# Quick Start Guide - Amazon Advertising Model

## Installation

### Requirements
- Python 3.9+
- pandas
- numpy

### Setup

```bash
# Clone the repository
git clone https://github.com/yuyun631/amz123.git
cd amz123

# Install dependencies (if using pip)
pip install -r requirements.txt
```

## File Overview

### Configuration
- `config/settings.json` - Core optimization parameters
- `config/thresholds.json` - Performance thresholds and alerts

### Models (Python)
- `models/bid_adjustment_model.py` - Bid optimization engine
- `models/acos_analyzer.py` - ACOS analysis and reporting
- `models/budget_allocator.py` - Budget distribution logic
- `models/forecast_model.py` - Performance forecasting (coming soon)

### Scripts
- `scripts/daily_optimization.py` - Daily automation
- `scripts/report_generator.py` - Report creation
- `scripts/data_processor.py` - Data ETL (coming soon)
- `scripts/api_connector.py` - Amazon API integration (coming soon)

### Data
- `data/sample_campaigns.csv` - Sample campaign metrics
- `data/sample_keywords.csv` - Sample keyword performance
- `data/daily_metrics.csv` - Daily aggregate metrics

### Documentation
- `docs/OPERATIONAL_GUIDE.md` - Daily operations procedures
- `docs/BEST_PRACTICES.md` - Industry best practices
- `docs/TROUBLESHOOTING.md` - Common issues and solutions
- `docs/API_REFERENCE.md` - API documentation (coming soon)

## Using the Models

### 1. Bid Adjustment Model

```python
from models.bid_adjustment_model import BidAdjustmentModel, KeywordPerformance

# Initialize model
model = BidAdjustmentModel('config/settings.json')

# Create keyword performance object
keyword = KeywordPerformance(
    keyword='amazon fba supplies',
    current_bid=0.60,
    clicks=125,
    impressions=1200,
    conversions=10,
    spend=75.00,
    sales=500.00,
    quality_score=8,
    days_active=30
)

# Get recommendation
recommendation = model.recommend_adjustment(keyword)
print(recommendation)
```

### 2. ACOS Analyzer

```python
from models.acos_analyzer import ACOSAnalyzer

# Initialize analyzer
analyzer = ACOSAnalyzer(target_acos=30.0)

# Add daily metrics
analyzer.add_daily_metrics(
    date='2026-05-01',
    spend=585.00,
    sales=3885.00,
    clicks=1050,
    impressions=21300
)

# Calculate period ACOS
period_analysis = analyzer.calculate_period_acos(days=7)
print(period_analysis)
```

### 3. Budget Allocator

```python
from models.budget_allocator import BudgetAllocator

# Initialize allocator
allocator = BudgetAllocator(total_daily_budget=600.0)

# Define campaigns
campaigns = [
    {'name': 'Brand Campaign', 'acos': 15.0, 'roas': 6.5},
    {'name': 'Category Campaign', 'acos': 25.0, 'roas': 4.0},
    {'name': 'Product Targeting', 'acos': 30.0, 'roas': 3.3}
]

# Allocate budget
allocation = allocator.allocate_performance_based(campaigns)
print(allocation)
```

## Running Daily Tasks

### Morning Review
```bash
python scripts/daily_optimization.py --task morning_review
```

### Midday Adjustments
```bash
python scripts/daily_optimization.py --task midday_adjustments
```

### Evening Analysis
```bash
python scripts/daily_optimization.py --task evening_analysis
```

### Generate Reports
```bash
# Daily report
python scripts/report_generator.py --type daily --date 2026-05-05

# Weekly report
python scripts/report_generator.py --type weekly --date 2026-05-05

# Monthly report
python scripts/report_generator.py --type monthly --date 2026-05
```

## Configuration

### Key Settings (config/settings.json)

```json
{
  "target_acos": 30.0,           # Target ACOS percentage
  "min_bid": 0.10,               # Minimum bid amount
  "max_bid": 10.00,              # Maximum bid amount
  "max_daily_change": 0.15,      # Max bid change per day (15%)
  "min_clicks_for_adjustment": 30,# Minimum clicks before adjustment
  "min_days_active": 7,          # Minimum days before optimization
  "roas_multiplier": 1.2         # ROAS target multiplier
}
```

### Performance Thresholds (config/thresholds.json)

Defines performance tiers and recommended actions:
- ACOS thresholds: excellent, good, acceptable, needs_attention, critical
- ROAS thresholds: excellent, good, acceptable, poor, critical
- CTR targets and conversion rate targets

## Sample Data

### Campaign Data (sample_campaigns.csv)
Includes sample data for:
- Brand Campaign
- Category Campaign
- Product Targeting Campaign

Columns: date, campaign_name, clicks, impressions, spend, sales, conversions, acos, roas, ctr, cpc

### Keyword Data (sample_keywords.csv)
Includes 10 sample keywords with:
- Performance metrics (clicks, impressions, spend, sales)
- Quality scores
- Bid information
- Calculated metrics (ACOS, ROAS, CTR, conversion rate)

### Daily Metrics (daily_metrics.csv)
Aggregate daily performance:
- Total spend and sales
- Total clicks and impressions
- Aggregate ACOS and ROAS
- Budget pacing

## Workflow Example

### Daily Operations

1. **9:00 AM - Morning Review**
   ```bash
   python scripts/daily_optimization.py --task morning_review
   ```
   - Check overnight performance
   - Review alerts
   - Plan adjustments

2. **12:00 PM - Midday Adjustments**
   ```bash
   python scripts/daily_optimization.py --task midday_adjustments
   ```
   - Apply bid optimizations
   - Monitor spend pacing
   - Execute strategic changes

3. **3:00 PM - Health Check**
   ```bash
   python scripts/daily_optimization.py --task health_check
   ```
   - Quick performance check
   - Verify spend on pace
   - Address any issues

4. **5:00 PM - Evening Analysis**
   ```bash
   python scripts/daily_optimization.py --task evening_analysis
   ```
   - Comprehensive analysis
   - Generate reports
   - Plan next day

### Weekly Operations

**Monday: Strategic Review**
- Generate weekly report
- Analyze 7-day performance
- Review campaign health

**Wednesday: Mid-Week Adjustments**
- Assess adjustment impact
- Make strategic changes
- Optimize budget allocation

**Friday: Planning**
- Generate comprehensive report
- Plan next week's focus
- Document findings

### Monthly Operations

- Generate comprehensive monthly report
- Review ACOS and ROAS trends
- Adjust strategy for next month
- Set new targets

## Troubleshooting

For common issues and solutions, see `docs/TROUBLESHOOTING.md`

Common scenarios:
- ACOS won't improve
- Low conversion rate
- Insufficient impressions
- Budget overspending

## Next Steps

1. Review `docs/OPERATIONAL_GUIDE.md` for detailed procedures
2. Review `docs/BEST_PRACTICES.md` for optimization strategies
3. Customize `config/settings.json` for your business
4. Load your campaign data
5. Start with daily optimization workflow

## Support

For questions or issues:
1. Check `docs/TROUBLESHOOTING.md`
2. Review configuration settings
3. Verify data format
4. Check model outputs

## Additional Resources

- [Amazon Seller Central](https://sellercentral.amazon.com)
- [Amazon Advertising API Documentation](https://advertising.amazon.com/API)
- Repository: [github.com/yuyun631/amz123](https://github.com/yuyun631/amz123)
