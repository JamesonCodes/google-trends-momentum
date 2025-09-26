import { Topic } from '../types';
import Sparkline from './Sparkline';

interface TopicCardProps {
  topic: Topic;
}

export default function TopicCard({ topic }: TopicCardProps) {
  const formatVolume = (volume: number) => {
    if (volume >= 1000000) return `${(volume / 1000000).toFixed(1)}M`;
    if (volume >= 1000) return `${(volume / 1000).toFixed(1)}K`;
    return volume.toString();
  };

  const formatPercentChange = (percent: number) => {
    return percent > 0 ? `+${percent.toFixed(0)}%` : `${percent.toFixed(0)}%`;
  };

  const getTrendStatus = (score: number, percentChange: number) => {
    if (score > 7 && percentChange > 100) return { label: 'RISING FAST', color: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200' };
    if (score > 5 && percentChange > 50) return { label: 'TRENDING', color: 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200' };
    if (score > 3 && percentChange > 20) return { label: 'RISING', color: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200' };
    return { label: 'STABLE', color: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200' };
  };

  const getCategoryColor = (category: string) => {
    const colors = {
      'ai-tools': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
      'tech': 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
      'business': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
      'science': 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-200',
      'default': 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
    };
    return colors[category as keyof typeof colors] || colors.default;
  };

  const trendStatus = getTrendStatus(topic.score, topic.percentChange);

  return (
    <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg p-6 hover:shadow-lg transition-all duration-200 group">
      {/* Header with trend status */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1 min-w-0">
          <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
            {topic.term}
          </h3>
          <div className="flex items-center space-x-2 mb-3">
            <span className={`inline-block px-3 py-1 text-xs font-semibold rounded-full ${getCategoryColor(topic.category)}`}>
              {topic.category.replace('-', ' ').toUpperCase()}
            </span>
            <span className={`inline-block px-3 py-1 text-xs font-semibold rounded-full ${trendStatus.color}`}>
              {trendStatus.label}
            </span>
          </div>
        </div>
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
            {formatVolume(topic.volume)}
          </div>
          <div className="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wide">
            Volume
          </div>
        </div>
        <div>
          <div className="text-2xl font-bold text-green-600 dark:text-green-400">
            {formatPercentChange(topic.percentChange)}
          </div>
          <div className="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wide">
            Growth
          </div>
        </div>
      </div>

      {/* Sparkline Chart */}
      <div className="mb-4">
        <div className="h-16 w-full">
          <Sparkline
            data={topic.sparkline}
            width={280}
            height={64}
            className="w-full h-full"
          />
        </div>
      </div>

      {/* Description placeholder */}
      <div className="text-sm text-gray-600 dark:text-gray-400 mb-4 line-clamp-2">
        Trending topic in {topic.category.replace('-', ' ')} with significant growth potential and increasing search volume.
      </div>

      {/* Footer with dates */}
      <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400 pt-3 border-t border-gray-100 dark:border-gray-700">
        <div>
          First seen: {new Date(topic.firstSeen).toLocaleDateString()}
        </div>
        <div>
          Updated: {new Date(topic.lastSeen).toLocaleDateString()}
        </div>
      </div>

      {/* Related queries if available */}
      {topic.relatedQueries && topic.relatedQueries.length > 0 && (
        <div className="mt-3 pt-3 border-t border-gray-100 dark:border-gray-700">
          <div className="text-xs text-gray-500 dark:text-gray-400 mb-2">Related:</div>
          <div className="flex flex-wrap gap-1">
            {topic.relatedQueries.slice(0, 3).map((query, index) => (
              <span key={index} className="text-xs bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 px-2 py-1 rounded">
                {query}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
