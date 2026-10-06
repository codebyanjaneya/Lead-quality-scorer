import { useState } from 'react';
import Papa from 'papaparse';

export default function UploadForm({ onUpload }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const files = e.dataTransfer.files;
    if (files && files[0]) {
      processFile(files[0]);
    }
  };

  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      processFile(e.target.files[0]);
    }
  };

  const processFile = (file) => {
    if (!file.name.endsWith('.csv')) {
      setError('Please upload a CSV file');
      return;
    }

    setLoading(true);
    setError('');

    Papa.parse(file, {
      header: true,
      skipEmptyLines: true,
      complete: (results) => {
        if (results.data && results.data.length > 0) {
          onUpload(results.data);
          setFile(file);
          setLoading(false);
        } else {
          setError('CSV file is empty');
          setLoading(false);
        }
      },
      error: (error) => {
        setError(`Error parsing CSV: ${error.message}`);
        setLoading(false);
      },
    });
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
      {/* Upload Section */}
      <div className="md:col-span-2">
        <div
          className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
            dragActive
              ? 'border-blue-500 bg-blue-500/10'
              : 'border-slate-600 bg-slate-800/50 hover:border-slate-500'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <div className="mb-4">
            <svg
              className="mx-auto h-12 w-12 text-slate-400"
              stroke="currentColor"
              fill="none"
              viewBox="0 0 48 48"
            >
              <path
                d="M28 8H12a4 4 0 00-4 4v20m32-12v8a4 4 0 01-4 4H12a4 4 0 01-4-4V12a4 4 0 014-4h16l8 8z"
                strokeWidth={2}
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </div>

          <label className="block cursor-pointer">
            <span className="text-lg font-semibold text-white mb-2">
              {loading ? 'Processing...' : 'Drop CSV here or click to select'}
            </span>
            <input
              type="file"
              accept=".csv"
              onChange={handleChange}
              disabled={loading}
              className="hidden"
            />
          </label>

          <p className="text-sm text-slate-400 mt-2">
            Supported format: CSV with columns: company_name, contact_email, contact_phone, company_size, industry, revenue
          </p>

          {file && (
            <p className="text-green-400 text-sm mt-4">
              ✓ File loaded: {file.name}
            </p>
          )}
        </div>

        {error && (
          <div className="mt-4 p-4 bg-red-500/10 border border-red-500 rounded text-red-400 text-sm">
            {error}
          </div>
        )}
      </div>

      {/* Info Cards */}
      <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-white mb-4">How It Works</h3>
        <ul className="space-y-3 text-slate-300 text-sm">
          <li className="flex items-start">
            <span className="text-blue-400 mr-3">1.</span>
            <span>Upload your CSV file with leads</span>
          </li>
          <li className="flex items-start">
            <span className="text-blue-400 mr-3">2.</span>
            <span>Our AI analyzes each lead</span>
          </li>
          <li className="flex items-start">
            <span className="text-blue-400 mr-3">3.</span>
            <span>Get scores and quality ratings</span>
          </li>
          <li className="flex items-start">
            <span className="text-blue-400 mr-3">4.</span>
            <span>Filter and export high-quality leads</span>
          </li>
        </ul>
      </div>

      <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-white mb-4">Scoring Formula</h3>
        <div className="space-y-2 text-sm text-slate-300">
          <div className="flex justify-between">
            <span>Authority (Company):</span>
            <span className="text-blue-400 font-semibold">40%</span>
          </div>
          <div className="flex justify-between">
            <span>Engagement (Contact):</span>
            <span className="text-green-400 font-semibold">35%</span>
          </div>
          <div className="flex justify-between">
            <span>Conversion (Probability):</span>
            <span className="text-purple-400 font-semibold">25%</span>
          </div>
          <div className="border-t border-slate-700 pt-2 mt-2 flex justify-between font-semibold">
            <span>Final Score:</span>
            <span className="text-white">0-100</span>
          </div>
        </div>
      </div>
    </div>
  );
}
