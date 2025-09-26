export interface Topic {
  term: string;
  category: string;
  score: number;
  percentChange: number;
  sparkline: number[];
  firstSeen: string;
  lastSeen: string;
  volume: number;
  relatedQueries?: string[];
}

export interface FilterState {
  category: string;
  minScore: number;
  sortBy: 'score' | 'percentChange';
}

export interface SeedsData {
  categories: {
    [key: string]: {
      weight: number;
      terms: string[];
    };
  };
  globalSettings: {
    maxTopicsPerCategory: number;
    minVolumeThreshold: number;
    timeframe: string;
    geo: string;
    gprop: string;
  };
}

export interface TopicsResponse {
  generatedAt: string;
  totalTopics: number;
  topics: Topic[];
}

export interface DataState {
  topics: Topic[];
  categories: string[];
  loading: boolean;
  error: string | null;
  lastUpdated: string | null;
}
