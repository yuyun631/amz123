# Amazon Advertising Operations Guide

## Daily Operations Workflow

### 1. Morning Review (9:00 AM EST)

**Objectives:**
- Assess overnight performance
- Identify critical issues
- Plan daily adjustments

**Steps:**

1. **Check Dashboard**
   - Open daily performance dashboard
   - Review key metrics: ACOS, ROAS, CTR, Conversion Rate
   - Compare to daily targets

2. **Analyze Performance**
   ```bash
   python scripts/daily_optimization.py --task morning_review
   ```
   - Review competitor activity
   - Check budget pacing
   - Identify underperforming keywords

3. **Alert Response**
   - If ACOS > 40%: Pause lowest performers
   - If daily spend < 50% of target: Increase bids
   - If daily spend > 120% of budget: Reduce bids

4. **Document Findings**
   - Record critical metrics
   - Note any anomalies
   - Flag items needing investigation

### 2. Mid-Day Adjustments (12:00 PM EST)

**Objectives:**
- Apply bid optimizations
- Monitor spend pacing
- Execute strategic changes

**Steps:**

1. **Run Bid Optimization**
   ```bash
   python scripts/daily_optimization.py --task midday_adjustments
   ```

2. **Review Recommendations**
   - Check bid adjustment suggestions
   - Verify campaign budget impacts
   - Validate changes won't exceed daily budget

3. **Apply Adjustments**
   - Keywords with poor ACOS: Decrease bid by 5-15%
   - Keywords with good conversion: Increase bid by 5-10%
   - Low-traffic keywords: Increase bid or pause if > 14 days

4. **Monitor Implementation**
   - Verify changes were applied correctly
   - Monitor initial impact
   - Be ready to revert if needed

### 3. Afternoon Check-In (3:00 PM EST)

**Quick Health Check:**
- Compare actual spend vs. daily target
- Check for any unusual activity
- Review any alerts generated
- Adjust pacing if needed

### 4. Evening Analysis (5:00 PM EST)

**Objectives:**
- Analyze day's performance
- Prepare next-day plan
- Generate reporting

**Steps:**

1. **Comprehensive Analysis**
   ```bash
   python scripts/daily_optimization.py --task evening_analysis
   ```

2. **Performance Review**
   - Calculate final ACOS and ROAS
   - Analyze trend directions
   - Compare to weekly/monthly averages

3. **Generate Reports**
   ```bash
   python scripts/report_generator.py --date today
   ```
   - Daily performance report
   - Campaign summaries
   - Keyword performance rankings

4. **Next-Day Planning**
   - Review recommendations
   - Identify pausing candidates
   - Plan scaling opportunities
   - Schedule bid adjustments

---

## Performance Monitoring

### Key Metrics by Priority

#### Priority 1 (Check Multiple Times Daily)
| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Daily Spend | $X.XX | ±15% |
| ACOS | 30% | > 40% |
| Budget Remaining | Gradual | < 30% |

#### Priority 2 (Check Twice Daily)
| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| ROAS | 3.0x | < 2.0x |
| Conversion Rate | 5% | < 2% |
| CTR | 4.5% | < 3% |

#### Priority 3 (Daily Review)
| Metric | Target | Review Threshold |
|--------|--------|------------------|
| Quality Score | 8+ | < 6 |
| Impressions | Growing | 20% decline |
| Clicks | Stable | 30% variance |

---

## Decision Trees

### ACOS Too High (> 40%)

```
Is ACOS > 40%?
├─ YES: Daily budget exceeded?
│   ├─ YES: Reduce daily budget allocation
│   └─ NO: Proceed to CPC analysis
├─ CPC too high (> $2.00)?
│   ├─ YES: Reduce bids 10-15%
│   └─ NO: Check conversion rate
└─ Conversion rate < 2%?
    ├─ YES: Review landing page quality
    └─ NO: Monitor for trends
```

### Campaign Underperforming (ROAS < 2.0x)

```
ROAS < 2.0x?
├─ YES: Days active < 7?
│   ├─ YES: Continue learning period
│   └─ NO: Check keywords
├─ High-quality keywords?
│   ├─ YES: Increase bid for volume
│   └─ NO: Pause and add new keywords
└─ Assess daily action needed
```

### Budget Not Spending

```
Daily spend < 50% of target?
├─ YES: Keywords paused?
│   ├─ YES: Resume paused keywords
│   └─ NO: Check bids
├─ Bids too low?
│   ├─ YES: Increase bids 10-20%
│   └─ NO: Check impression share
└─ Impression share < 50%?
    ├─ YES: Increase bids further
    └─ NO: Monitor for improvement
```

---

## Weekly Operations

### Monday: Strategic Review

1. **Analyze Weekly Performance**
   - Calculate 7-day ACOS and ROAS
   - Identify weekly trends
   - Compare to previous weeks

2. **Campaign Assessment**
   - Review each campaign's performance
   - Identify scaling opportunities
   - Flag underperformers for review

3. **Keyword Audit**
   - Review top 100 keywords
   - Analyze new keyword performance
   - Identify pausing candidates

### Wednesday: Mid-Week Adjustments

1. **Trend Analysis**
   - Check if adjustments are helping
   - Identify emerging patterns
   - Make strategic bid increases/decreases

2. **Budget Optimization**
   - Review daily spend patterns
   - Reallocate to top performers
   - Adjust pacing strategies

### Friday: Planning

1. **Weekly Summary**
   - Generate comprehensive report
   - Document all changes made
   - Record decision rationale

2. **Next Week Planning**
   - Identify priority actions
   - Plan keyword expansion
   - Schedule campaign reviews

---

## Monthly Operations

### First Week: Comprehensive Review

1. **Monthly Performance Analysis**
   - Calculate ACOS, ROAS, CTR, CR
   - Compare to targets and historical
   - Identify contributing factors

2. **Campaign Health Checkup**
   - Review all campaigns
   - Assess budget allocation effectiveness
   - Plan adjustments for coming month

3. **Financial Review**
   - Total advertising spend
   - Total attributed sales
   - Profitability analysis

### Second Week: Optimization

1. **Keyword Deep Dive**
   - Expand top performers
   - Pause underperformers
   - A/B test new keywords

2. **Strategy Adjustment**
   - Update bid strategies
   - Adjust budget allocations
   - Plan seasonal adjustments

### Third Week: Forecasting

1. **Predictive Analysis**
   - Forecast next month's performance
   - Identify seasonal factors
   - Plan budget adjustments

2. **Goal Setting**
   - Set monthly targets
   - Define success metrics
   - Establish improvement goals

### Fourth Week: Planning

1. **Next Month Planning**
   - Document best practices discovered
   - Plan testing initiatives
   - Schedule campaign reviews

---

## Emergency Procedures

### Budget Depletion Alert (< 2 hours remaining)

1. Immediately pause all lowest-performing keywords
2. Reduce bids on all remaining keywords by 25%
3. Alert management
4. Document all actions taken

### Critical ACOS Spike (> 50%)

1. Identify triggering keywords
2. Pause lowest-performing 20% of keywords
3. Review all active bids
4. Investigate unusual activity
5. Notify supervisor immediately

### System Issues

1. Check Amazon Advertising API status
2. Verify data connection
3. Document issue details
4. Switch to manual monitoring
5. Contact technical support

---

## Tips for Success

### Bid Management Best Practices

1. **Never change bids more than 15% daily**
   - Allows algorithm to adjust
   - Prevents overcorrection
   - Maintains stability

2. **Always check click volume before adjusting**
   - Require minimum 30 clicks for reliability
   - More clicks = faster adjustments
   - Less clicks = extend learning period

3. **Group keywords by performance tier**
   - Tier 1 (Excellent): Increase bids, expand
   - Tier 2 (Good): Maintain, monitor
   - Tier 3 (Poor): Reduce bids, consider pause

### ACOS Optimization

1. **For New Campaigns (< 7 days)**
   - Avoid aggressive bid cuts
   - Give time to accumulate data
   - Monitor CTR and conversion patterns

2. **For Established Campaigns (> 30 days)**
   - Make aggressive cuts if ACOS > 40%
   - Leverage historical data for decisions
   - Test bid ranges more confidently

3. **Seasonal Adjustments**
   - Increase bids 20-30% before peak seasons
   - Reduce bids 10-15% after peak seasons
   - Monitor competitor activity closely

### Data Integrity

1. Always verify data before analysis
2. Check for unusual anomalies
3. Compare multiple data sources
4. Document any discrepancies
5. Maintain audit trail of changes

---

## Common Issues and Solutions

### Issue: ACOS Won't Improve

**Solutions:**
- Review keywords for relevance
- Check landing page quality
- Analyze product pricing
- Consider expanding negative keywords
- Test different match types

### Issue: Low Conversion Rate

**Solutions:**
- Review keyword-to-product relevance
- Check landing page experience
- Test new product placement
- Analyze customer reviews
- Improve product photography

### Issue: Insufficient Impressions

**Solutions:**
- Increase bids 10-20%
- Expand match types (broad match)
- Add new keyword variations
- Review impression share % lost to rank
- Check quality scores

### Issue: Budget Overspending

**Solutions:**
- Reduce daily bid limits
- Pause low-performing keywords
- Tighten budget caps
- Monitor pacing more frequently
- Adjust dayparting if available

---

## Tools and Resources

- **Primary Dashboard**: Amazon Seller Central > Advertising > Campaigns
- **Optimization Engine**: `./scripts/daily_optimization.py`
- **Report Generator**: `./scripts/report_generator.py`
- **Data Processor**: `./scripts/data_processor.py`
- **Documentation**: `./docs/`

## Contact and Escalation

For urgent issues or exceptions, escalate to:
- Operations Manager: [Contact]
- Technical Lead: [Contact]
- Executive Sponsor: [Contact]
