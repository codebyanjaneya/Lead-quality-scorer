import { useState, useEffect } from 'react';
import LeadCard from './LeadCard';
import FilterPanel from './FilterPanel';

export default function LeadDashboard({ leads, onGoBack }) {
  const [scoredLeads, setScoredLeads] = useState([]);
  const [filteredLeads, setFilteredLeads] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterScore, setFilterScore] = useState(0);
  const [sortBy, setSortBy] = useState('score_desc');

  // Score leads when component mounts
  useEffect(() => {
    scoreAllLeads();
  }, [leads]);

  // Filter leads based on score
  useEffect(() => {
    let filtered = scoredLeads.filter(lead => lead.final_score >= filterScore);

    // Sort
    if (sortBy === 'score_desc') {
      filtered.sort((a, b) => b.final_score - a.final_score);
    } else if (sortBy === 'score_asc') {
      filtered.sort((a, b) => a.final_score - b.final_score);
    } else if (sortBy === 'company_az') {
      filtered.sort((a, b) => a.company_name.localeCompare(b.company_name));
    }

    setFilteredLeads(filtered);
  }, [scoredLeads, filterScore, sortBy]);

  const scoreAllLeads = async () => {
    setLoading(true);
    try {
      // In real app, would call backend API
      // For demo, we'll use mock scoring based on company data
      const scored = leads.map((lead, idx) => {
        const score = calculateMockScore(lead);
        return {
          ...lead,
          final_score: score,
          quality: score >= 75 ? 'HIGH' : score >= 50 ? 'MEDIUM' : 'LOW',
          color: score >= 75 ? 'green' : score >= 50 ? 'yellow' : 'red',
        };
      });
      setScoredLeads(scored);
    } catch (error) {
      console.error('Error scoring leads:', error);
    } finally {
      setLoading(false);
    }
  };

  const calculateMockScore = (lead) => {
    // Simplified scoring for demo
    let score = 50;

    // Company size bonus
    const size = parseInt(lead.company_size) || 0;
    if (size >= 5000) score += 25;
    else if (size >= 1000) score += 20;
    else if (size >= 100) score += 10;

    // Industry bonus
    if (['Technology', 'SaaS', 'FinTech', 'AI/ML'].includes(lead.industry)) {
      score += 15;
    }

    // Email validity
    if (lead.contact_email && lead.contact_email.includes('@')) {
      const domain = lead.contact_email.split('@')[1];
      if (!['gmail.com', 'yahoo.com', 'outlook.com'].includes(domain)) {
        score += 10;
      }
    }

    // Revenue bonus
    const revenue = parseInt(lead.revenue) || 0;
    if (revenue >= 50000000) score += 10;
    else if (revenue >= 10000000) score += 8;

    return Math.min(100, Math.max(0, score));
  };

  const stats = {
    total: scoredLeads.length,
    high: scoredLeads.filter(l => l.quality === 'HIGH').length,
    medium: scoredLeads.filter(l => l.quality === 'MEDIUM').length,
    low: scoredLeads.filter(l => l.quality === 'LOW').length,
  };

  return (
    <div className="space-y-6">
      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard label="Total Leads" value={stats.total} color="blue" />
        <StatCard label="High Quality" value={stats.high} color="green" />
        <StatCard label="Medium" value={stats.medium} color="yellow" />
        <StatCard label="Low Quality" value={stats.low} color="red" />
      </div>

      {/* Filters */}
      <FilterPanel
        filterScore={filterScore}
        setFilterScore={setFilterScore}
        sortBy={sortBy}
        setSortBy={setSortBy}
        onGoBack={onGoBack}
      />

      {/* Leads Grid */}
      <div>
        <h2 className="text-xl font-bold text-white mb-4">
          {filteredLeads.length} Leads (Score {filterScore}+)
        </h2>

        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin">
              <svg className="w-8 h-8 text-blue-400" fill="none" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" className="opacity-25" />
                <path
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
            </div>
            <p className="text-slate-400 mt-4">Scoring leads...</p>
          </div>
        ) : filteredLeads.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredLeads.map((lead, idx) => (
              <LeadCard key={idx} lead={lead} />
            ))}
          </div>
        ) : (
          <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-8 text-center">
            <p className="text-slate-400">No leads match your filter criteria</p>
          </div>
        )}
      </div>
    </div>
  );
}

function StatCard({ label, value, color }) {
  const colorClass = {
    blue: 'bg-blue-500/20 border-blue-500/30',
    green: 'bg-green-500/20 border-green-500/30',
    yellow: 'bg-yellow-500/20 border-yellow-500/30',
    red: 'bg-red-500/20 border-red-500/30',
  }[color];

  const textColor = {
    blue: 'text-blue-400',
    green: 'text-green-400',
    yellow: 'text-yellow-400',
    red: 'text-red-400',
  }[color];

  return (
    <div className={`${colorClass} border rounded-lg p-4`}>
      <p className="text-slate-400 text-sm">{label}</p>
      <p className={`text-3xl font-bold ${textColor}`}>{value}</p>
    </div>
  );
}
