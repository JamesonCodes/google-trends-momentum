import { Topic } from '../types';
import Sparkline from './Sparkline';

interface TopicCardProps {
  topic: Topic;
}

export default function TopicCard({ topic }: TopicCardProps) {
  const formatScore = (score: number) => {
    return score > 0 ? `+${score.toFixed(1)}` : score.toFixed(1);
  };

  const formatPercentChange = (percent: number) => {
    return percent > 0 ? `+${percent.toFixed(1)}%` : `${percent.toFixed(1)}%`;
  };

  const getScoreColor = (score: number) => {
    if (score > 2) return 'text-green-600 dark:text-green-400';
    if (score > 0) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-red-600 dark:text-red-400';
  };

  const getPercentColor = (percent: number) => {
    if (percent > 0) return 'text-green-600 dark:text-green-400';
    return 'text-red-600 dark:text-red-400';
  };

  return (
    <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1 min-w-0">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white truncate">
            {topic.term}
          </h3>
          <span className="inline-block px-2 py-1 text-xs font-medium bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-full mt-1">
            {topic.category}
          </span>
        </div>
        <div className="flex flex-col items-end ml-2">
          <span className={`text-lg font-bold ${getScoreColor(topic.score)}`}>
            {formatScore(topic.score)}
          </span>
          <span className={`text-sm ${getPercentColor(topic.percentChange)}`}>
            {formatPercentChange(topic.percentChange)}
          </span>
        </div>
      </div>
      
      <div className="flex items-center justify-between">
        <div className="flex-1 mr-3">
          <Sparkline 
            data={topic.sparkline} 
            width={120} 
            height={24}
            className="opacity-80"
          />
        </div>
        <div className="text-xs text-gray-500 dark:text-gray-400 text-right">
          <div>First: {new Date(topic.firstSeen).toLocaleDateString()}</div>
          <div>Last: {new Date(topic.lastSeen).toLocaleDateString()}</div>
        </div>
      </div>
    </div>
  );
}
