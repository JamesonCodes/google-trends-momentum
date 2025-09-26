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

  const handleMinScoreChange = (minScore: number) => {
    onFiltersChange({ ...filters, minScore });
  };

  const handleSortChange = (sortBy: 'score' | 'percentChange') => {
    onFiltersChange({ ...filters, sortBy });
  };

  return (
    <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl p-6 mb-8 shadow-sm">
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
        {/* Left side - Filters */}
        <div className="flex flex-col sm:flex-row gap-4 flex-1">
          {/* Category Filter */}
          <div className="min-w-[160px]">
            <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
              Category
            </label>
            <select
              value={filters.category}
              onChange={(e) => handleCategoryChange(e.target.value)}
              className="w-full px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-medium"
            >
              <option value="">All Categories</option>
              {categories.map((category) => (
                <option key={category} value={category}>
                  {category.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Right side - Sort Options */}
        <div className="flex gap-2">
          <button
            onClick={() => handleSortChange('score')}
            className={`px-4 py-2.5 text-sm font-semibold rounded-lg transition-all duration-200 ${
              filters.sortBy === 'score'
                ? 'bg-blue-600 text-white shadow-md'
                : 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'
            }`}
          >
            Score
          </button>
          <button
            onClick={() => handleSortChange('percentChange')}
            className={`px-4 py-2.5 text-sm font-semibold rounded-lg transition-all duration-200 ${
              filters.sortBy === 'percentChange'
                ? 'bg-blue-600 text-white shadow-md'
                : 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'
            }`}
          >
            Growth
          </button>
        </div>
      </div>

      {/* Min Score Filter */}
      <div className="mt-4 pt-4 border-t border-gray-100 dark:border-gray-700">
        <div className="flex items-center justify-between">
          <label className="text-sm font-semibold text-gray-700 dark:text-gray-300">
            Minimum Score: {filters.minScore}
          </label>
          <div className="w-48">
            <input
              type="range"
              min="0"
              max="10"
              step="0.1"
              value={filters.minScore}
              onChange={(e) => handleMinScoreChange(parseFloat(e.target.value))}
              className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer"
            />
          </div>
        </div>
      </div>
    </div>
  );
}
