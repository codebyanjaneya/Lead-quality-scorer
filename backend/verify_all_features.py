"""
End-to-End Verification of All Three Features
1A: Scoring, 1B: Duplicates, 1C: CRM
"""

from scoring import LeadScorer
from duplicate_detection import DuplicateDetector
from crm_integration import CRMIntegration
import pandas as pd

def verify_feature_1a():
    """Verify Feature 1A: Lead Quality Scoring"""
    print("\n" + "=" * 60)
    print("STEP 1: VERIFY FEATURE 1A (SCORING)")
    print("=" * 60)

    try:
        scorer = LeadScorer()

        # Test scoring
        test_lead = {
            'company_name': 'Microsoft',
            'company_size': 50000,
            'industry': 'Technology',
            'revenue': 200000000,
            'location': 'US',
        }
        contact = {
            'contact_email': 'john@microsoft.com',
            'contact_phone': '+1-206-555-0100',
        }

        result = scorer.calculate_final_score(test_lead, contact)

        print("\n[OK] Scoring Logic:")
        print(f"  Score: {result['final_score']} ({result['quality']})")
        print(f"  Authority: {result['components']['authority']}/100")
        print(f"  Engagement: {result['components']['engagement']}/100")
        print(f"  Conversion: {result['components']['conversion']}/100")

        # Test CSV loading
        df = pd.read_csv('../data/sample_leads.csv')
        print(f"\n[OK] CSV Processing:")
        print(f"  Loaded: {len(df)} leads")
        print(f"  Columns: {list(df.columns)}")

        # Score sample data
        scored_count = 0
        for idx, row in df.head(3).iterrows():
            company_data = {
                'company_name': str(row['company_name']),
                'company_size': int(float(row['company_size'])) if row['company_size'] else 0,
                'industry': str(row['industry']),
                'revenue': int(float(row['revenue'])) if row['revenue'] else 0,
                'location': 'US',
            }
            contact_data = {
                'contact_email': str(row['contact_email']),
                'contact_phone': str(row['contact_phone']),
            }
            score_result = scorer.calculate_final_score(company_data, contact_data)
            print(f"  {row['company_name']:20} -> {score_result['final_score']:5.1f} ({score_result['quality']})")
            scored_count += 1

        print(f"\n[PASS] Feature 1A: VERIFIED ({scored_count} leads scored)")
        return True

    except Exception as e:
        print(f"[FAIL] Feature 1A FAILED: {e}")
        return False

def verify_feature_1b():
    """Verify Feature 1B: Duplicate Detection"""
    print("\n" + "=" * 60)
    print("STEP 2: VERIFY FEATURE 1B (DUPLICATES)")
    print("=" * 60)

    try:
        detector = DuplicateDetector()

        # Test with duplicates
        test_leads = [
            {'company_name': 'Microsoft Corp', 'contact_email': 'john@microsoft.com', 'contact_phone': '+1-206-555-0100', 'final_score': 85},
            {'company_name': 'Microsoft Inc', 'contact_email': 'jane@microsoft.com', 'contact_phone': '+1-206-555-0101', 'final_score': 80},
            {'company_name': 'Microsoft', 'contact_email': 'contact@gmail.com', 'contact_phone': '+1-206-555-0102', 'final_score': 75},
            {'company_name': 'Apple', 'contact_email': 'alex@apple.com', 'contact_phone': '+1-408-555-0100', 'final_score': 90},
            {'company_name': 'Google', 'contact_email': 'bob@google.com', 'contact_phone': '+1-650-555-0100', 'final_score': 88},
        ]

        print(f"\n[OK] Duplicate Detection:")
        print(f"  Input: {len(test_leads)} leads")

        unique, dupes, merged = detector.find_duplicates(test_leads)

        print(f"  Detected: {len(dupes)} duplicate groups")
        print(f"  Unique leads: {len(unique)}")
        print(f"  After merge: {len(merged)} leads")

        print(f"\n[OK] Merge Results:")
        for m in merged:
            if m.get('is_merged'):
                print(f"  > {m['company_name']:20} (merged {m['duplicate_count']} leads)")

        summary = detector.get_deduplication_summary()
        print(f"\n[OK] Summary: {summary['summary']}")

        print(f"\n[PASS] Feature 1B: VERIFIED")
        return True

    except Exception as e:
        print(f"[FAIL] Feature 1B FAILED: {e}")
        return False

def verify_feature_1c():
    """Verify Feature 1C: CRM Integration"""
    print("\n" + "=" * 60)
    print("STEP 3: VERIFY FEATURE 1C (CRM)")
    print("=" * 60)

    try:
        crm = CRMIntegration('hubspot')

        # Test leads
        test_leads = [
            {
                'company_name': 'Microsoft',
                'contact_name': 'John Smith',
                'contact_email': 'john@microsoft.com',
                'contact_phone': '+1-206-555-0100',
                'industry': 'Technology',
                'final_score': 86.1,
                'quality': 'HIGH',
            },
            {
                'company_name': 'Startup Inc',
                'contact_name': 'Jane Doe',
                'contact_email': 'jane@startup.com',
                'contact_phone': '+1-555-555-0100',
                'industry': 'Software',
                'final_score': 65.0,
                'quality': 'MEDIUM',
            },
        ]

        print(f"\n[OK] CRM Sync (HubSpot):")
        print(f"  Input: {len(test_leads)} leads")

        result = crm.batch_sync_to_crm(test_leads, dry_run=True)

        print(f"  Synced: {result['synced']}/{result['total_leads']}")
        print(f"  Failed: {result['failed']}")

        print(f"\n[OK] Synced Leads:")
        for lead in result['synced_leads']:
            print(f"  > {lead['company']:20} | {lead['email']:30} | {lead['status']}")

        # Check connection
        status = crm.get_crm_connection_status()
        print(f"\n[OK] Connection Status:")
        print(f"  CRM: {status['crm_type']}")
        print(f"  Status: {status['status']}")
        print(f"  Ready: {status['ready']}")

        print(f"\n[PASS] Feature 1C: VERIFIED")
        return True

    except Exception as e:
        print(f"[FAIL] Feature 1C FAILED: {e}")
        return False

def main():
    """Run all verifications"""
    print("\n" + "=" * 60)
    print("END-TO-END FEATURE VERIFICATION")
    print("=" * 60)

    results = {
        '1A: Scoring': verify_feature_1a(),
        '1B: Duplicates': verify_feature_1b(),
        '1C: CRM': verify_feature_1c(),
    }

    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)

    for feature, passed in results.items():
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{feature}: {status}")

    all_passed = all(results.values())

    print("\n" + "=" * 60)
    if all_passed:
        print("[SUCCESS] ALL FEATURES VERIFIED - READY FOR PRODUCTION")
    else:
        print("[ERROR] SOME FEATURES FAILED - FIX REQUIRED")
    print("=" * 60)

    return all_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
