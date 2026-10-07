import { useState } from "react";
import UploadForm from "@/components/UploadForm";
import LeadDashboard from "@/components/LeadDashboard";

export default function Home() {
  const [leads, setLeads] = useState([]);
  const [scores, setScores] = useState({ high: 0, medium: 0, low: 0 });
  const [uploadedCount, setUploadedCount] = useState(0);

  const handleLeadsUpdate = (newLeads) => {
    setLeads(newLeads);
    const stats = { high: 0, medium: 0, low: 0 };
    newLeads.forEach((lead) => {
      if (lead.quality === "HIGH") stats.high++;
      else if (lead.quality === "MEDIUM") stats.medium++;
      else stats.low++;
    });
    setScores(stats);
    setUploadedCount(newLeads.length);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <header className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-8 shadow-lg">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl font-bold">Lead Quality Scorer</h1>
          <p className="text-blue-100 mt-2">AI-powered lead scoring & CRM integration</p>
        </div>
      </header>

      <main className="container mx-auto px-4 py-12">
        {uploadedCount === 0 ? (
          <UploadForm onLeadsUpdate={handleLeadsUpdate} />
        ) : (
          <LeadDashboard leads={leads} stats={scores} onNewUpload={() => setUploadedCount(0)} />
        )}
      </main>

      <footer className="bg-gray-800 text-white py-6 mt-12">
        <div className="container mx-auto px-4 text-center">
          <p className="text-gray-400">Lead Quality Scoring Engine | Built with React + FastAPI</p>
        </div>
      </footer>
    </div>
  );
}
