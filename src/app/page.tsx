'use client';

import { useState, useMemo } from 'react';
import { FilterState } from './types';
import { useTopicsData } from './hooks/useTopicsData';
import TopicCard from './components/TopicCard';
import Filters from './components/Filters';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorDisplay from './components/ErrorDisplay';
import DataStatus from './components/DataStatus';

export default function Home() {
  const [filters, setFilters] = useState<FilterState>({
    category: '',
    sortBy: 'score'
  });

  // Fetch real data
  const { topics, categories, loading, error, lastUpdated, isStale, refreshData } = useTopicsData();

  // Filter and sort topics
  const filteredAndSortedTopics = useMemo(() => {
    const filtered = topics.filter(topic => {
      const categoryMatch = !filters.category || topic.category === filters.category;
      return categoryMatch;
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
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center px-4 py-2 rounded-full bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 text-sm font-medium mb-6">
            <div className="w-2 h-2 bg-blue-500 rounded-full mr-2 animate-pulse"></div>
            Live Trending Data
          </div>
          
          <h1 className="text-6xl font-bold text-gray-900 dark:text-white mb-6 tracking-tight">
            Rising Topics
          </h1>
          
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto mb-8 leading-relaxed">
            Discover the most trending and rising topics across AI Tools, Tech, Business, and Science categories with real-time insights
          </p>
          
          {/* Value Proposition */}
          <div className="max-w-4xl mx-auto mb-8">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
              <div className="p-6 bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
                <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/20 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <svg className="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Discover Early Trends</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">Find topics before they go mainstream and get ahead of the competition</p>
              </div>
              
              <div className="p-6 bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
                <div className="w-12 h-12 bg-green-100 dark:bg-green-900/20 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <svg className="w-6 h-6 text-green-600 dark:text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Data-Driven Insights</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">Real growth metrics and trend analysis to make informed decisions</p>
              </div>
              
              <div className="p-6 bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
                <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/20 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <svg className="w-6 h-6 text-purple-600 dark:text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Stay Updated</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">Fresh data updated regularly so you never miss emerging opportunities</p>
              </div>
            </div>
          </div>
          
          {/* Data Status */}
          <DataStatus 
            lastUpdated={lastUpdated}
            isStale={isStale}
            onRefresh={refreshData}
            loading={loading}
          />
        </div>

        {/* Filters */}
        <div className="mb-8">
          <Filters 
            filters={filters}
            onFiltersChange={setFilters}
            categories={categories}
          />
          
          {/* Results Summary */}
          <div className="mt-6 text-center">
            <div className="inline-flex items-center px-4 py-2 bg-white dark:bg-gray-800 rounded-full shadow-sm border border-gray-200 dark:border-gray-700">
              <div className="w-2 h-2 bg-blue-500 rounded-full mr-2"></div>
              <span className="text-sm text-gray-600 dark:text-gray-400">
                {filters.category ? (
                  <>
                    Showing <span className="font-semibold text-gray-900 dark:text-white">{filteredAndSortedTopics.length}</span> topics in <span className="font-semibold text-gray-900 dark:text-white">{filters.category.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())}</span>
                  </>
                ) : (
                  <>
                    Showing <span className="font-semibold text-gray-900 dark:text-white">{filteredAndSortedTopics.length}</span> featured trending topics
                  </>
                )}
              </span>
            </div>
          </div>
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
      </div>
    </div>
  );
}
