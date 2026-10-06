import { useState } from 'react';
import UploadForm from '../components/UploadForm';
import LeadDashboard from '../components/LeadDashboard';

export default function Home() {
  const [leads, setLeads] = useState([]);
  const [scores, setScores] = useState({});
  const [uploadedCount, setUploadedCount] = useState(0);

  const handleUpload = (data) => {
    setLeads(data);
    setUploadedCount(data.length);
    // Score will be calculated on backend
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header */}
      <div className="bg-slate-950 border-b border-slate-700 py-6">
        <div className="max-w-7xl mx-auto px-4">
          <h1 className="text-4xl font-bold text-white mb-2">Lead Quality Scorer</h1>
          <p className="text-slate-400">AI-powered lead scoring for SaaSquatch Leads</p>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        {uploadedCount === 0 ? (
          <UploadForm onUpload={handleUpload} />
        ) : (
          <LeadDashboard leads={leads} onGoBack={() => setUploadedCount(0)} />
        )}
      </div>

      {/* Footer */}
      <div className="border-t border-slate-700 bg-slate-950 mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6 text-center text-slate-500 text-sm">
          <p>Caprae Capital - Lead Quality Scoring Engine | 5-Hour Development Challenge</p>
        </div>
      </div>
    </div>
  );
}
