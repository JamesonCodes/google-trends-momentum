interface DataStatusProps {
  lastUpdated: string | null;
  isStale: boolean;
  onRefresh: () => void;
  loading: boolean;
}

export default function DataStatus({ lastUpdated, isStale, onRefresh, loading }: DataStatusProps) {
  const formatLastUpdated = (timestamp: string | null) => {
    if (!timestamp) return 'Never';
    
    try {
      const date = new Date(timestamp);
      const now = new Date();
      const diffMs = now.getTime() - date.getTime();
      const diffMins = Math.floor(diffMs / (1000 * 60));
      const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
      
      if (diffMins < 1) return 'Just now';
      if (diffMins < 60) return `${diffMins}m ago`;
      if (diffHours < 24) return `${diffHours}h ago`;
      
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    } catch (error) {
      console.error('formatLastUpdated error:', error);
      return 'Unknown';
    }
  };

  return (
    <div className="flex items-center justify-center space-x-4 text-sm text-gray-500 dark:text-gray-400">
      <div className="flex items-center space-x-2">
        <div className={`w-2 h-2 rounded-full ${isStale ? 'bg-yellow-500' : 'bg-green-500'}`} />
        <span>
          Last updated: {formatLastUpdated(lastUpdated)}
        </span>
        {isStale && (
          <span className="text-yellow-600 dark:text-yellow-400">
            (Stale)
          </span>
        )}
        {loading && (
          <span className="text-blue-600 dark:text-blue-400">
            (Refreshing...)
          </span>
        )}
      </div>
      
      <button
        onClick={() => {
          console.log('DataStatus: Refresh button clicked at', new Date().toISOString());
          onRefresh();
        }}
        disabled={loading}
        className="flex items-center space-x-1 px-3 py-1 text-sm text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-md transition-colors"
      >
        {loading ? (
          <>
            <div className="w-3 h-3 border border-current border-t-transparent rounded-full animate-spin" />
            <span>Refreshing...</span>
          </>
        ) : (
          <>
            <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <span>Refresh</span>
          </>
        )}
      </button>
    </div>
  );
}
