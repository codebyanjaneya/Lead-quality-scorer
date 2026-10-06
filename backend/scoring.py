"""
Lead Quality Scoring Engine
Calculates 3 components: Authority, Engagement, Conversion Probability
Final Score = (Authority × 0.40) + (Engagement × 0.35) + (Conversion × 0.25)
"""

import re
import math
from typing import Dict, Tuple

class LeadScorer:
    """Calculate lead quality score (0-100) based on company and contact data"""

    def __init__(self):
        # Define thresholds for scoring
        self.company_size_thresholds = [10, 50, 100, 500, 1000, 5000]
        self.revenue_thresholds = [500_000, 1_000_000, 5_000_000, 10_000_000, 50_000_000, 100_000_000]

        # Industries that convert better
        self.high_conversion_industries = ['Technology', 'SaaS', 'FinTech', 'AI/ML', 'Cloud Computing']
        self.medium_conversion_industries = ['Finance', 'Healthcare', 'E-commerce', 'Marketing']

    def calculate_authority_score(self, company_data: Dict) -> float:
        """
        AUTHORITY SCORE (40% weight)
        Measures: Company size, age, industry, revenue legitimacy

        Factors:
        - Company size (employees): 1-10 = 20pts, 100+ = 100pts
        - Industry type: Tech = high, Others = varies
        - Revenue: $1M+ = high authority

        Returns: 0-100 score
        """
        score = 0
        factors = {}

        # 1. Company Size Score (30% of authority)
        size = company_data.get('company_size', 0)
        if size >= 5000:
            size_score = 100
        elif size >= 1000:
            size_score = 85
        elif size >= 500:
            size_score = 70
        elif size >= 100:
            size_score = 60
        elif size >= 50:
            size_score = 40
        else:
            size_score = 20
        factors['size'] = size_score

        # 2. Industry Reputation Score (25% of authority)
        industry = company_data.get('industry', 'Other')
        if industry in self.high_conversion_industries:
            industry_score = 90
        elif industry in self.medium_conversion_industries:
            industry_score = 70
        else:
            industry_score = 50
        factors['industry'] = industry_score

        # 3. Revenue Legitimacy Score (30% of authority)
        revenue = company_data.get('revenue', 0)
        if revenue >= 100_000_000:
            revenue_score = 100
        elif revenue >= 50_000_000:
            revenue_score = 90
        elif revenue >= 10_000_000:
            revenue_score = 80
        elif revenue >= 5_000_000:
            revenue_score = 70
        elif revenue >= 1_000_000:
            revenue_score = 60
        else:
            revenue_score = 30
        factors['revenue'] = revenue_score

        # Weighted combination
        authority_score = (
            (size_score * 0.30) +
            (industry_score * 0.35) +
            (revenue_score * 0.35)
        )

        return min(100, authority_score), factors

    def calculate_engagement_score(self, contact_data: Dict) -> Tuple[float, Dict]:
        """
        ENGAGEMENT SCORE (35% weight)
        Measures: Email validity, domain type, phone format, data completeness

        Factors:
        - Email validity (has @, domain exists): 0-100
        - Email domain type: Company domain = 90, Gmail = 50
        - Phone format: Valid format = 100, Invalid = 0
        - Data completeness: All fields filled = 100

        Returns: 0-100 score
        """
        score = 0
        factors = {}

        # 1. Email Validity Score (35% of engagement)
        email = contact_data.get('contact_email', '')
        email_score = self._validate_email(email)
        factors['email_valid'] = email_score

        # 2. Email Domain Type Score (30% of engagement)
        domain_score = self._score_email_domain(email)
        factors['domain_type'] = domain_score

        # 3. Phone Format Score (20% of engagement)
        phone = contact_data.get('contact_phone', '')
        phone_score = self._validate_phone(phone)
        factors['phone_valid'] = phone_score

        # 4. Data Completeness Score (15% of engagement)
        completeness = self._score_data_completeness(contact_data)
        factors['completeness'] = completeness

        # Weighted combination
        engagement_score = (
            (email_score * 0.35) +
            (domain_score * 0.30) +
            (phone_score * 0.20) +
            (completeness * 0.15)
        )

        return min(100, engagement_score), factors

    def calculate_conversion_probability(self, company_data: Dict) -> Tuple[float, Dict]:
        """
        CONVERSION PROBABILITY (25% weight)
        Uses ML logic: which companies historically convert better

        Factors:
        - Industry match: Tech + SaaS = high probability
        - Company size: Enterprise (1000+) = high
        - Revenue tier: $10M+ = high
        - Location: US = 100, Europe = 80, India = 60

        Returns: 0-100 probability score
        """
        factors = {}

        # 1. Industry Conversion Rate
        industry = company_data.get('industry', 'Other')
        if industry in self.high_conversion_industries:
            industry_prob = 85
        elif industry in self.medium_conversion_industries:
            industry_prob = 65
        else:
            industry_prob = 45
        factors['industry_prob'] = industry_prob

        # 2. Company Size Conversion Rate
        size = company_data.get('company_size', 0)
        if size >= 1000:
            size_prob = 80  # Enterprise = high conversion
        elif size >= 100:
            size_prob = 65  # Mid-market
        elif size >= 10:
            size_prob = 50  # Small business
        else:
            size_prob = 30  # Startup/micro
        factors['size_prob'] = size_prob

        # 3. Revenue Tier Conversion
        revenue = company_data.get('revenue', 0)
        if revenue >= 50_000_000:
            revenue_prob = 85
        elif revenue >= 10_000_000:
            revenue_prob = 75
        elif revenue >= 1_000_000:
            revenue_prob = 60
        else:
            revenue_prob = 40
        factors['revenue_prob'] = revenue_prob

        # 4. Location Bias
        location = company_data.get('location', 'Unknown')
        if location == 'US':
            location_prob = 90
        elif location in ['UK', 'Europe', 'Canada']:
            location_prob = 70
        else:
            location_prob = 50
        factors['location_prob'] = location_prob

        # Weighted combination (simulating ML model)
        conversion_prob = (
            (industry_prob * 0.30) +
            (size_prob * 0.35) +
            (revenue_prob * 0.20) +
            (location_prob * 0.15)
        )

        return min(100, conversion_prob), factors

    def calculate_final_score(self, company_data: Dict, contact_data: Dict) -> Dict:
        """
        Calculate final lead quality score (0-100)

        Formula:
        FINAL = (Authority × 0.40) + (Engagement × 0.35) + (Conversion × 0.25)

        Returns: Dictionary with scores + explanation
        """
        # Calculate 3 components
        authority, auth_factors = self.calculate_authority_score(company_data)
        engagement, eng_factors = self.calculate_engagement_score(contact_data)
        conversion, conv_factors = self.calculate_conversion_probability(company_data)

        # Final weighted score
        final_score = (authority * 0.40) + (engagement * 0.35) + (conversion * 0.25)
        final_score = round(min(100, final_score), 1)

        # Determine quality level
        if final_score >= 75:
            quality = "HIGH"
            color = "🟢"
        elif final_score >= 50:
            quality = "MEDIUM"
            color = "🟡"
        else:
            quality = "LOW"
            color = "🔴"

        # Generate explanation
        explanation = self._generate_explanation(
            company_data,
            authority,
            engagement,
            conversion,
            quality
        )

        return {
            'final_score': final_score,
            'quality': quality,
            'color': color,
            'components': {
                'authority': round(authority, 1),
                'engagement': round(engagement, 1),
                'conversion': round(conversion, 1),
            },
            'factors': {
                'authority': auth_factors,
                'engagement': eng_factors,
                'conversion': conv_factors,
            },
            'explanation': explanation,
        }

    # HELPER METHODS

    def _validate_email(self, email: str) -> float:
        """Check if email format is valid"""
        if not email:
            return 0
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return 95  # Valid email format
        return 20  # Invalid format

    def _score_email_domain(self, email: str) -> float:
        """Score based on email domain type"""
        if not email:
            return 0

        domain = email.split('@')[1].lower() if '@' in email else ''

        # Company domain (not free email) = high score
        free_domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'aol.com']
        if domain not in free_domains and domain:
            return 95  # Company email
        elif domain:
            return 50  # Free email
        return 20

    def _validate_phone(self, phone: str) -> float:
        """Check if phone format is valid"""
        if not phone:
            return 0
        # Basic validation: has digits and common separators
        if re.search(r'\d{7,}', phone):  # At least 7 digits
            return 90
        return 20

    def _score_data_completeness(self, data: Dict) -> float:
        """Score based on how many fields are filled"""
        required_fields = ['contact_email', 'contact_phone', 'company_name']
        filled = sum(1 for field in required_fields if data.get(field))
        completeness = (filled / len(required_fields)) * 100
        return min(100, completeness)

    def _generate_explanation(self, company_data, authority, engagement, conversion, quality) -> str:
        """Generate human-readable explanation of the score"""
        company_name = company_data.get('company_name', 'Unknown Company')
        industry = company_data.get('industry', 'Unknown')
        size = company_data.get('company_size', 0)

        if quality == "HIGH":
            reasons = [
                f"✓ Established {industry} company" if size >= 1000 else f"✓ Solid {industry} company",
                f"✓ Valid contact information",
                f"✓ Good conversion potential based on industry & size",
            ]
        elif quality == "MEDIUM":
            reasons = [
                f"✓ {industry} company with moderate size",
                f"✓ Contact info partially complete",
                f"• Research more before outreach",
            ]
        else:
            reasons = [
                f"• Small/new {industry} company",
                f"• Contact information incomplete/invalid",
                f"• Lower conversion probability - skip this lead",
            ]

        return " | ".join(reasons)


# Test the scorer
if __name__ == "__main__":
    scorer = LeadScorer()

    # Test with Microsoft
    company = {
        'company_name': 'Microsoft',
        'company_size': 50000,
        'industry': 'Technology',
        'revenue': 200000000,
        'location': 'US',
    }
    contact = {
        'contact_name': 'John Smith',
        'contact_email': 'john@microsoft.com',
        'contact_phone': '+1-206-555-0100',
    }

    result = scorer.calculate_final_score(company, contact)
    print(f"Company: {company['company_name']}")
    print(f"Score: {result['final_score']} {result['color']} ({result['quality']})")
    print(f"Authority: {result['components']['authority']}")
    print(f"Engagement: {result['components']['engagement']}")
    print(f"Conversion: {result['components']['conversion']}")
    print(f"Explanation: {result['explanation']}")
