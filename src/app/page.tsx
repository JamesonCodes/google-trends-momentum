'use client';

import { useState, useMemo } from 'react';
import { Topic, FilterState } from './types';
import { mockTopics, categories } from './mockData';
import TopicCard from './components/TopicCard';
import Filters from './components/Filters';

export default function Home() {
  const [filters, setFilters] = useState<FilterState>({
    category: '',
    minScore: 0,
    sortBy: 'score'
  });

  // Filter and sort topics
  const filteredAndSortedTopics = useMemo(() => {
    let filtered = mockTopics.filter(topic => {
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
  }, [filters]);

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
            Exploding Topics
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-400">
            Discover trending topics across categories
          </p>
        </div>

        {/* Filters */}
        <Filters 
          filters={filters}
          onFiltersChange={setFilters}
          categories={categories}
        />

        {/* Results Summary */}
        <div className="mb-6">
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Showing {filteredAndSortedTopics.length} of {mockTopics.length} topics
          </p>
        </div>

        {/* Topics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredAndSortedTopics.map((topic, index) => (
            <TopicCard key={`${topic.term}-${index}`} topic={topic} />
          ))}
        </div>

        {/* Empty State */}
        {filteredAndSortedTopics.length === 0 && (
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
