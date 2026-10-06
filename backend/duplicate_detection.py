"""
Feature 1B: Duplicate Detection & Deduplication
Detects duplicate leads (same company) and merges them
"""

from typing import List, Dict, Tuple
import re

class DuplicateDetector:
    """Find and merge duplicate leads from same company"""

    def __init__(self):
        self.duplicates_found = []
        self.merged_leads = []

    def normalize_company_name(self, name: str) -> str:
        """Normalize company name for comparison

        BUSINESS LOGIC:
        - Remove common suffixes (Inc, LLC, Corp)
        - Lowercase for comparison
        - Remove extra spaces

        Example:
        "Microsoft Corporation" → "microsoft"
        "Apple Inc." → "apple"
        """
        name = str(name).lower().strip()
        # Remove common suffixes
        suffixes = [' inc', ' corporation', ' corp', ' llc', ' ltd', ' limited', ' company', ' co']
        for suffix in suffixes:
            if name.endswith(suffix):
                name = name.replace(suffix, '')
        # Clean spaces
        name = ' '.join(name.split())
        return name

    def normalize_domain(self, email: str) -> str:
        """Extract and normalize domain from email

        BUSINESS LOGIC:
        - Extract domain part only
        - Handle variations (gmail.com = gmail)

        Example:
        john@microsoft.com → microsoft.com
        jane@apple.com → apple.com
        """
        if not email or '@' not in email:
            return ''
        domain = email.split('@')[1].lower()
        return domain

    def email_quality_score(self, email: str) -> int:
        """Score email quality (higher = better)

        BUSINESS LOGIC:
        - Company domain = 100 (best)
        - Named domain = 70
        - Free email = 30 (worst)

        Used when choosing which email to keep
        """
        if not email:
            return 0

        domain = email.split('@')[1].lower() if '@' in email else ''

        # Free email domains
        free_domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'aol.com']

        if domain in free_domains:
            return 30
        elif domain:
            # Assume company domain
            return 100
        return 0

    def find_duplicates(self, leads: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        """
        Find duplicate leads from same company

        APPROACH:
        1. Group leads by normalized company name
        2. If group size > 1 → duplicate found
        3. For each duplicate group:
           - Keep lead with best email
           - Keep lead with most data fields
           - Mark as duplicate

        Returns:
        - unique_leads: Leads with no duplicates
        - duplicate_groups: Groups of duplicate leads

        EXAMPLE:
        Input: [
            {company: "Microsoft Corp", email: "john@microsoft.com"},
            {company: "Microsoft", email: "jane@microsoft.com"},
            {company: "Apple", email: "contact@apple.com"},
        ]

        Output:
        Unique: [Apple]
        Duplicates: [[Microsoft (2 leads)]]
        """

        # Group by normalized company name
        company_groups = {}

        for idx, lead in enumerate(leads):
            company_name = lead.get('company_name', '')
            normalized = self.normalize_company_name(company_name)

            if normalized not in company_groups:
                company_groups[normalized] = []

            company_groups[normalized].append({
                'original_index': idx,
                'lead': lead,
                'normalized_name': normalized,
            })

        # Separate unique and duplicates
        unique_leads = []
        duplicate_groups = []
        merge_results = []

        for normalized_name, group in company_groups.items():
            if len(group) == 1:
                # No duplicate
                unique_leads.append(group[0]['lead'])
            else:
                # Found duplicates
                duplicate_groups.append(group)

                # Merge this group
                merged = self._merge_duplicate_group(group, normalized_name)
                merge_results.append(merged)

        self.duplicates_found = duplicate_groups
        self.merged_leads = unique_leads + merge_results

        return unique_leads, duplicate_groups, merge_results

    def _merge_duplicate_group(self, group: List[Dict], company_name: str) -> Dict:
        """
        Merge a group of duplicate leads

        MERGE LOGIC:
        1. Select best email (company domain > free email)
        2. Select best phone (longer = more complete)
        3. Keep highest score lead as primary
        4. Mark as merged

        Returns: Single merged lead with all data
        """

        # Find lead with best email
        best_email_idx = 0
        best_email_score = 0

        for idx, item in enumerate(group):
            email = item['lead'].get('contact_email', '')
            score = self.email_quality_score(email)
            if score > best_email_score:
                best_email_score = score
                best_email_idx = idx

        # Find lead with best phone
        best_phone = ''
        for item in group:
            phone = item['lead'].get('contact_phone', '')
            if len(phone) > len(best_phone):
                best_phone = phone

        # Find lead with highest quality score
        best_score_lead = max(
            group,
            key=lambda x: x['lead'].get('final_score', 0)
        )['lead']

        # Merge into single lead
        merged_lead = {
            **best_score_lead,
            'contact_email': group[best_email_idx]['lead'].get('contact_email', ''),
            'contact_phone': best_phone,
            'is_merged': True,
            'duplicate_count': len(group),
            'merge_note': f'Merged {len(group)} duplicates for {company_name}',
            'source_leads': [item['lead'].get('contact_email') for item in group],
        }

        return merged_lead

    def get_deduplication_summary(self) -> Dict:
        """Get summary of deduplication results

        BUSINESS VALUE:
        Shows sales team:
        - How many duplicates found
        - How much data cleaned
        - Merged leads ready for use
        """

        total_duplicates = sum(len(group) - 1 for group in self.duplicates_found)

        return {
            'total_duplicates_found': total_duplicates,
            'duplicate_groups': len(self.duplicates_found),
            'leads_after_merge': len(self.merged_leads),
            'summary': f'Found {total_duplicates} duplicates in {len(self.duplicates_found)} groups',
        }


# Test the duplicate detector
if __name__ == "__main__":
    detector = DuplicateDetector()

    test_leads = [
        {'company_name': 'Microsoft Corp', 'contact_email': 'john@microsoft.com', 'contact_phone': '+1-206-555-0100', 'final_score': 85},
        {'company_name': 'Microsoft', 'contact_email': 'jane@microsoft.com', 'contact_phone': '+1-206-555-0101', 'final_score': 80},
        {'company_name': 'Microsoft Corporation', 'contact_email': 'contact@gmail.com', 'contact_phone': '+1-206-555-0102', 'final_score': 75},
        {'company_name': 'Apple Inc.', 'contact_email': 'alex@apple.com', 'contact_phone': '+1-408-555-0100', 'final_score': 90},
        {'company_name': 'Google', 'contact_email': 'bob@google.com', 'contact_phone': '+1-650-555-0100', 'final_score': 88},
    ]

    print("=" * 70)
    print("DUPLICATE DETECTION TEST")
    print("=" * 70)

    unique, dupes, merged = detector.find_duplicates(test_leads)

    print(f"\n✓ Found {len(dupes)} duplicate groups")
    print(f"✓ {len(unique)} unique leads")
    print(f"✓ {len(merged)} merged leads (unique + deduped)")

    for group in dupes:
        print(f"\n Duplicate Group:")
        for item in group:
            print(f"   - {item['lead']['company_name']:25} | {item['lead']['contact_email']}")

    print(f"\n Merged Results:")
    for lead in merged:
        if lead.get('is_merged'):
            print(f"   ✓ {lead['company_name']:25} | Email: {lead['contact_email']} (merged {lead['duplicate_count']} leads)")

    summary = detector.get_deduplication_summary()
    print(f"\n" + "=" * 70)
    print(f"✅ {summary['summary']}")
    print(f"✅ Leads after deduplication: {summary['leads_after_merge']}")
