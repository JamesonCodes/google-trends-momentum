interface ErrorDisplayProps {
  error: string;
  onRetry?: () => void;
  className?: string;
}

export default function ErrorDisplay({ error, onRetry, className = '' }: ErrorDisplayProps) {
  return (
    <div className={`text-center py-12 ${className}`}>
      <div className="text-red-400 dark:text-red-600 mb-4">
        <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
        </svg>
      </div>
      <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
        Error Loading Data
      </h3>
      <p className="text-gray-600 dark:text-gray-400 mb-4">
        {error}
      </p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
        >
          Try Again
        </button>
      )}
    </div>
  );
}
