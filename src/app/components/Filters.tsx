import { FilterState } from '../types';

interface FiltersProps {
  filters: FilterState;
  onFiltersChange: (filters: FilterState) => void;
  categories: string[];
}

export default function Filters({ filters, onFiltersChange, categories }: FiltersProps) {
  const handleCategoryChange = (category: string) => {
    onFiltersChange({ ...filters, category });
  };


  const handleSortChange = (sortBy: 'score' | 'percentChange') => {
    onFiltersChange({ ...filters, sortBy });
  };

  return (
    <div className="flex flex-col sm:flex-row items-center justify-between gap-4 mb-8">
      {/* Category Filter */}
      <div className="flex items-center gap-3">
        <span className="text-sm font-medium text-gray-600 dark:text-gray-400">Filter by:</span>
        <select
          value={filters.category}
          onChange={(e) => handleCategoryChange(e.target.value)}
          className="px-4 py-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors min-w-[140px]"
        >
          <option value="">All Categories</option>
          {categories.map((category) => (
            <option key={category} value={category}>
              {category.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())}
            </option>
          ))}
        </select>
      </div>

      {/* Sort Options */}
      <div className="flex items-center gap-2">
        <span className="text-sm font-medium text-gray-600 dark:text-gray-400">Sort by:</span>
        <div className="flex bg-gray-100 dark:bg-gray-800 rounded-lg p-1">
          <button
            onClick={() => handleSortChange('score')}
            className={`px-3 py-1.5 text-sm font-medium rounded-md transition-all duration-200 ${
              filters.sortBy === 'score'
                ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
            }`}
          >
            Score
          </button>
          <button
            onClick={() => handleSortChange('percentChange')}
            className={`px-3 py-1.5 text-sm font-medium rounded-md transition-all duration-200 ${
              filters.sortBy === 'percentChange'
                ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
            }`}
          >
            Growth
          </button>
        </div>
      </div>
    </div>
  );
}
