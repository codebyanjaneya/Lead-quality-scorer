export default function FilterPanel({ filterScore, setFilterScore, sortBy, setSortBy, onGoBack }) {
  return (
    <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Score Filter */}
        <div>
          <label className="block text-sm font-semibold text-white mb-3">
            Minimum Score: {filterScore}
          </label>
          <input
            type="range"
            min="0"
            max="100"
            value={filterScore}
            onChange={(e) => setFilterScore(parseInt(e.target.value))}
            className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
          />
          <div className="flex justify-between text-xs text-slate-500 mt-2">
            <span>Low 🔴</span>
            <span>Medium 🟡</span>
            <span>High 🟢</span>
          </div>
        </div>

        {/* Sort By */}
        <div>
          <label className="block text-sm font-semibold text-white mb-3">Sort By</label>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="w-full bg-slate-700 text-white px-3 py-2 rounded border border-slate-600 focus:border-blue-500 focus:outline-none"
          >
            <option value="score_desc">Score (High to Low)</option>
            <option value="score_asc">Score (Low to High)</option>
            <option value="company_az">Company (A-Z)</option>
          </select>
        </div>

        {/* Quick Score Buttons */}
        <div>
          <label className="block text-sm font-semibold text-white mb-3">Quick Filter</label>
          <div className="flex gap-2">
            <button
              onClick={() => setFilterScore(0)}
              className="flex-1 bg-slate-700 hover:bg-slate-600 text-white text-sm py-2 rounded transition"
            >
              All
            </button>
            <button
              onClick={() => setFilterScore(50)}
              className="flex-1 bg-yellow-600/30 hover:bg-yellow-600/40 text-yellow-300 text-sm py-2 rounded transition border border-yellow-600/50"
            >
              Medium+
            </button>
            <button
              onClick={() => setFilterScore(75)}
              className="flex-1 bg-green-600/30 hover:bg-green-600/40 text-green-300 text-sm py-2 rounded transition border border-green-600/50"
            >
              High Only
            </button>
          </div>
        </div>
      </div>

      {/* Bottom Actions */}
      <div className="mt-6 pt-6 border-t border-slate-700 flex justify-between items-center">
        <button
          onClick={onGoBack}
          className="text-slate-400 hover:text-white transition text-sm"
        >
          ← Upload New File
        </button>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded transition">
          📥 Export All
        </button>
      </div>
    </div>
  );
}
