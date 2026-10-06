export default function LeadCard({ lead }) {
  const getQualityColor = () => {
    if (lead.quality === 'HIGH') return 'border-green-500 bg-green-500/5';
    if (lead.quality === 'MEDIUM') return 'border-yellow-500 bg-yellow-500/5';
    return 'border-red-500 bg-red-500/5';
  };

  const getScoreBgColor = () => {
    if (lead.quality === 'HIGH') return 'bg-green-500/20 text-green-300';
    if (lead.quality === 'MEDIUM') return 'bg-yellow-500/20 text-yellow-300';
    return 'bg-red-500/20 text-red-300';
  };

  const getQualityEmoji = () => {
    if (lead.quality === 'HIGH') return '🟢';
    if (lead.quality === 'MEDIUM') return '🟡';
    return '🔴';
  };

  return (
    <div className={`border rounded-lg p-4 transition-all hover:shadow-lg hover:border-opacity-100 ${getQualityColor()}`}>
      {/* Header */}
      <div className="flex justify-between items-start mb-3">
        <div>
          <h3 className="font-bold text-white text-lg truncate">
            {lead.company_name}
          </h3>
          <p className="text-slate-400 text-sm">
            {lead.industry} • {lead.company_size} employees
          </p>
        </div>
        <span className={`text-2xl px-2 py-1 rounded`}>
          {getQualityEmoji()}
        </span>
      </div>

      {/* Score */}
      <div className="mb-4">
        <div className="flex justify-between items-end mb-2">
          <span className="text-slate-300 text-sm font-semibold">Quality Score</span>
          <span className={`text-2xl font-bold ${getScoreBgColor()} px-3 py-1 rounded`}>
            {lead.final_score.toFixed(1)}
          </span>
        </div>
        <div className="w-full bg-slate-700 rounded-full h-2">
          <div
            className={`h-2 rounded-full transition-all ${
              lead.quality === 'HIGH' ? 'bg-green-500' :
              lead.quality === 'MEDIUM' ? 'bg-yellow-500' :
              'bg-red-500'
            }`}
            style={{ width: `${lead.final_score}%` }}
          />
        </div>
      </div>

      {/* Contact Info */}
      <div className="space-y-2 mb-4 border-t border-slate-700 pt-3">
        <div className="text-sm">
          <p className="text-slate-400 text-xs">Contact Email</p>
          <p className="text-white truncate">{lead.contact_email}</p>
        </div>
        <div className="text-sm">
          <p className="text-slate-400 text-xs">Phone</p>
          <p className="text-white">{lead.contact_phone}</p>
        </div>
      </div>

      {/* Actions */}
      <div className="flex gap-2 pt-2 border-t border-slate-700">
        <button className="flex-1 bg-blue-600 hover:bg-blue-700 text-white text-sm py-2 rounded transition">
          View Details
        </button>
        <button className="flex-1 bg-slate-700 hover:bg-slate-600 text-white text-sm py-2 rounded transition">
          Export
        </button>
      </div>
    </div>
  );
}
