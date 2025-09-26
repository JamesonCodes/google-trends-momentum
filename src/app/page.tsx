'use client';

import { useState, useMemo } from 'react';
import { FilterState } from './types';
import { useTopicsData } from './hooks/useTopicsData';
import TopicCard from './components/TopicCard';
import Filters from './components/Filters';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorDisplay from './components/ErrorDisplay';
import DataStatus from './components/DataStatus';
import DebugInfo from './components/DebugInfo';

export default function Home() {
  const [filters, setFilters] = useState<FilterState>({
    category: '',
    minScore: 0,
    sortBy: 'score'
  });

  // Fetch real data
  const { topics, categories, loading, error, lastUpdated, isStale, refreshData, refreshKey } = useTopicsData();

  // Filter and sort topics
  const filteredAndSortedTopics = useMemo(() => {
    const filtered = topics.filter(topic => {
      const categoryMatch = !filters.category || topic.category === filters.category;
      const scoreMatch = topic.score >= filters.minScore;
      return categoryMatch && scoreMatch;
    });

    // Sort topics
    filtered.sort((a, b) => {
      if (filters.sortBy === 'score') {
        return b.score - a.score;
      } else {
        return b.percentChange - a.percentChange;
      }
    });

    return filtered;
  }, [topics, filters]);

  // Show loading state
  if (loading && topics.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
              Rising Topics
            </h1>
            <p className="text-lg text-gray-600 dark:text-gray-400">
              Discover trending topics across categories
            </p>
          </div>
          <LoadingSpinner size="lg" className="py-20" />
        </div>
      </div>
    );
  }

  // Show error state
  if (error && topics.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
              Rising Topics
            </h1>
            <p className="text-lg text-gray-600 dark:text-gray-400">
              Discover trending topics across categories
            </p>
          </div>
          <ErrorDisplay error={error} onRetry={refreshData} />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-4">
            Rising Topics
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            Discover the most trending and rising topics across all categories with real-time data and insights
          </p>
        </div>

        {/* Data Status */}
        <DataStatus 
          lastUpdated={lastUpdated}
          isStale={isStale}
          onRefresh={refreshData}
          loading={loading}
        />

        {/* Filters */}
        <Filters 
          filters={filters}
          onFiltersChange={setFilters}
          categories={categories}
        />

        {/* Results Summary */}
        <div className="mb-6">
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Showing {filteredAndSortedTopics.length} of {topics.length} topics
          </p>
        </div>

        {/* Topics Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8">
          {filteredAndSortedTopics.map((topic, index) => (
            <TopicCard key={`${topic.term}-${index}`} topic={topic} />
          ))}
        </div>

        {/* Empty State */}
        {filteredAndSortedTopics.length === 0 && !loading && (
          <div className="text-center py-12">
            <div className="text-gray-400 dark:text-gray-600 mb-4">
              <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.29-1.009-5.824-2.709M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
              No topics found
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Try adjusting your filters to see more results.
            </p>
          </div>
        )}
        
        {/* Debug Info (only in development) */}
        <DebugInfo 
          topics={topics}
          lastUpdated={lastUpdated}
          loading={loading}
          error={error}
          refreshKey={refreshKey}
        />
      </div>
    </div>
  );
}
