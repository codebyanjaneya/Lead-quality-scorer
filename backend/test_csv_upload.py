"""
Test CSV Upload with Sample Data
Simulates the actual upload process
"""

import pandas as pd
import json
from scoring import LeadScorer

def test_csv_upload():
    print("=" * 70)
    print("TEST: CSV UPLOAD WITH ACTUAL SAMPLE DATA")
    print("=" * 70)

    # Load CSV
    try:
        df = pd.read_csv('../data/sample_leads.csv')
        print(f'\n✓ CSV loaded successfully: {len(df)} leads')
        print(f'  Columns: {list(df.columns)}')
    except Exception as e:
        print(f'❌ Error loading CSV: {e}')
        return

    # Validate columns
    required_cols = ['company_name', 'contact_email', 'contact_phone',
                     'company_size', 'industry', 'revenue']
    if not all(col in df.columns for col in required_cols):
        print(f'❌ Missing required columns')
        return

    print(f'✅ All required columns present')

    # Score all leads
    print(f'\n✓ Scoring all {len(df)} leads...\n')

    scorer = LeadScorer()
    scored_leads = []
    stats = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}

    for idx, row in df.iterrows():
        company = {
            'company_name': str(row['company_name']),
            'company_size': int(float(row['company_size'])) if row['company_size'] else 0,
            'industry': str(row['industry']),
            'revenue': int(float(row['revenue'])) if row['revenue'] else 0,
            'location': 'US',
        }
        contact = {
            'contact_email': str(row['contact_email']),
            'contact_phone': str(row['contact_phone']),
        }

        result = scorer.calculate_final_score(company, contact)

        lead_with_score = {
            'company_name': company['company_name'],
            'contact_email': contact['contact_email'],
            'contact_phone': contact['contact_phone'],
            'industry': company['industry'],
            'final_score': result['final_score'],
            'quality': result['quality'],
            'color': result['color'],
        }

        scored_leads.append(lead_with_score)
        stats[result['quality']] += 1

        # Show first 10
        if idx < 10:
            print(f'{idx+1:2}. {company["company_name"]:25} | Score: {result["final_score"]:5.1f} {result["color"]} ({result["quality"]:6})')

    if len(scored_leads) > 10:
        print(f'... and {len(scored_leads) - 10} more leads')

    # Summary statistics
    print(f'\n' + "=" * 70)
    print("SCORING SUMMARY")
    print("=" * 70)
    print(f'Total Leads Processed: {len(scored_leads)}')
    print(f'High Quality 🟢: {stats["HIGH"]:2} leads')
    print(f'Medium Quality 🟡: {stats["MEDIUM"]:2} leads')
    print(f'Low Quality 🔴: {stats["LOW"]:2} leads')

    # Calculate average score
    avg_score = sum(l['final_score'] for l in scored_leads) / len(scored_leads)
    print(f'Average Score: {avg_score:.1f}/100')

    # Sort by score
    top_5 = sorted(scored_leads, key=lambda x: x['final_score'], reverse=True)[:5]
    print(f'\nTop 5 High Quality Leads:')
    for i, lead in enumerate(top_5):
        print(f'  {i+1}. {lead["company_name"]:30} | {lead["final_score"]:5.1f} {lead["color"]}')

    # Validation checks
    print(f'\n' + "=" * 70)
    print("VALIDATION CHECKS")
    print("=" * 70)

    # Check 1: All scores between 0-100
    all_valid_scores = all(0 <= l['final_score'] <= 100 for l in scored_leads)
    print(f'✅ All scores 0-100: {all_valid_scores}')

    # Check 2: Quality matches score
    quality_correct = all(
        (l['quality'] == 'HIGH' and l['final_score'] >= 75) or
        (l['quality'] == 'MEDIUM' and 50 <= l['final_score'] < 75) or
        (l['quality'] == 'LOW' and l['final_score'] < 50)
        for l in scored_leads
    )
    print(f'✅ Quality matches score ranges: {quality_correct}')

    # Check 3: All required fields present
    all_fields_present = all(
        all(k in l for k in ['company_name', 'contact_email', 'final_score', 'quality'])
        for l in scored_leads
    )
    print(f'✅ All required fields present: {all_fields_present}')

    # Check 4: No duplicate scores (should be variety)
    unique_scores = len(set(l['final_score'] for l in scored_leads))
    print(f'✅ Score variety (unique scores): {unique_scores}/{len(scored_leads)}')

    # Final verdict
    print(f'\n' + "=" * 70)
    if all_valid_scores and quality_correct and all_fields_present:
        print("✅ CSV UPLOAD TEST PASSED - READY FOR API!")
        return True
    else:
        print("❌ CSV UPLOAD TEST FAILED - ISSUES DETECTED")
        return False

if __name__ == "__main__":
    success = test_csv_upload()
    exit(0 if success else 1)
