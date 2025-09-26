import { TopicsResponse, Topic } from '../types';

const DATA_URL = '/data/latest.json';

export class DataService {
  private static instance: DataService;
  private cache: TopicsResponse | null = null;
  private lastFetch: number = 0;
  private readonly CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

  private constructor() {}

  static getInstance(): DataService {
    if (!DataService.instance) {
      DataService.instance = new DataService();
    }
    return DataService.instance;
  }

  async fetchTopics(forceRefresh: boolean = false): Promise<TopicsResponse> {
    const now = Date.now();
    
    // Return cached data if it's still fresh and not forcing refresh
    if (!forceRefresh && this.cache && (now - this.lastFetch) < this.CACHE_DURATION) {
      return this.cache;
    }

    try {
      const response = await fetch(DATA_URL, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        // Add cache control for development
        cache: forceRefresh ? 'no-cache' : 'default',
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch data: ${response.status} ${response.statusText}`);
      }

      const data: TopicsResponse = await response.json();
      
      // Validate data structure
      if (!data.topics || !Array.isArray(data.topics)) {
        throw new Error('Invalid data structure: topics array missing');
      }

      // Cache the data
      this.cache = data;
      this.lastFetch = now;

      return data;
    } catch (error) {
      console.error('Error fetching topics:', error);
      
      // Return cached data if available, even if stale
      if (this.cache) {
        console.warn('Returning stale cached data due to fetch error');
        return this.cache;
      }
      
      throw error;
    }
  }

  getCategories(topics: Topic[]): string[] {
    const categorySet = new Set<string>();
    topics.forEach(topic => {
      if (topic.category) {
        categorySet.add(topic.category);
      }
    });
    return Array.from(categorySet).sort();
  }

  isDataStale(): boolean {
    if (!this.cache) return true;
    const now = Date.now();
    return (now - this.lastFetch) >= this.CACHE_DURATION;
  }

  getLastUpdated(): string | null {
    return this.cache?.generatedAt || null;
  }

  clearCache(): void {
    this.cache = null;
    this.lastFetch = 0;
  }
}

export const dataService = DataService.getInstance();
