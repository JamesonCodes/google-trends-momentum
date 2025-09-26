/**
 * @jest-environment jsdom
 */

import { DataService } from '../dataService';

// Mock fetch
global.fetch = jest.fn();

describe('DataService', () => {
  let dataService: DataService;

  beforeEach(() => {
    dataService = DataService.getInstance();
    dataService.clearCache();
    jest.clearAllMocks();
  });

  afterEach(() => {
    dataService.clearCache();
  });

  it('should fetch topics successfully', async () => {
    const mockData = {
      generatedAt: '2024-01-01T00:00:00.000Z',
      totalTopics: 2,
      topics: [
        {
          term: 'test-topic-1',
          category: 'ai-tools',
          score: 5.0,
          percentChange: 10.0,
          sparkline: [1, 2, 3, 4, 5],
          firstSeen: '2024-01-01T00:00:00.000Z',
          lastSeen: '2024-01-01T00:00:00.000Z',
          volume: 100,
          relatedQueries: ['related1', 'related2']
        }
      ]
    };

    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockData,
    });

    const result = await dataService.fetchTopics();

    expect(fetch).toHaveBeenCalledWith('/data/latest.json', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      cache: 'default',
    });

    expect(result).toEqual(mockData);
  });

  it('should return cached data when not forcing refresh', async () => {
    const mockData = {
      generatedAt: '2024-01-01T00:00:00.000Z',
      totalTopics: 1,
      topics: []
    };

    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockData,
    });

    // First fetch
    await dataService.fetchTopics();
    
    // Second fetch should use cache
    const result = await dataService.fetchTopics();

    expect(fetch).toHaveBeenCalledTimes(1);
    expect(result).toEqual(mockData);
  });

  it('should force refresh when requested', async () => {
    const mockData = {
      generatedAt: '2024-01-01T00:00:00.000Z',
      totalTopics: 1,
      topics: []
    };

    (fetch as jest.Mock).mockResolvedValue({
      ok: true,
      json: async () => mockData,
    });

    // First fetch
    await dataService.fetchTopics();
    
    // Force refresh
    await dataService.fetchTopics(true);

    expect(fetch).toHaveBeenCalledTimes(2);
  });

  it('should handle fetch errors gracefully', async () => {
    (fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'));

    await expect(dataService.fetchTopics()).rejects.toThrow('Network error');
  });

  it('should return stale cache on error if available', async () => {
    const mockData = {
      generatedAt: '2024-01-01T00:00:00.000Z',
      totalTopics: 1,
      topics: []
    };

    // First successful fetch
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockData,
    });

    await dataService.fetchTopics();

    // Second fetch fails
    (fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'));

    const result = await dataService.fetchTopics();

    expect(result).toEqual(mockData);
  });

  it('should extract categories correctly', () => {
    const topics = [
      { 
        category: 'ai-tools', 
        term: 'test1',
        score: 5,
        percentChange: 10,
        sparkline: [1, 2, 3],
        firstSeen: '2024-01-01T00:00:00.000Z',
        lastSeen: '2024-01-01T00:00:00.000Z',
        volume: 100,
        relatedQueries: []
      },
      { 
        category: 'tech', 
        term: 'test2',
        score: 5,
        percentChange: 10,
        sparkline: [1, 2, 3],
        firstSeen: '2024-01-01T00:00:00.000Z',
        lastSeen: '2024-01-01T00:00:00.000Z',
        volume: 100,
        relatedQueries: []
      },
      { 
        category: 'ai-tools', 
        term: 'test3',
        score: 5,
        percentChange: 10,
        sparkline: [1, 2, 3],
        firstSeen: '2024-01-01T00:00:00.000Z',
        lastSeen: '2024-01-01T00:00:00.000Z',
        volume: 100,
        relatedQueries: []
      },
      { 
        category: 'business', 
        term: 'test4',
        score: 5,
        percentChange: 10,
        sparkline: [1, 2, 3],
        firstSeen: '2024-01-01T00:00:00.000Z',
        lastSeen: '2024-01-01T00:00:00.000Z',
        volume: 100,
        relatedQueries: []
      }
    ];

    const categories = dataService.getCategories(topics);

    expect(categories).toEqual(['ai-tools', 'business', 'tech']);
  });

  it('should detect stale data correctly', () => {
    // Mock Date.now to control time
    const originalNow = Date.now;
    const mockNow = jest.fn();

    Date.now = mockNow;

    // Set up cache with old timestamp
    mockNow.mockReturnValue(1000);
    dataService['lastFetch'] = 1000;

    // Check if data is stale after cache duration
    mockNow.mockReturnValue(1000 + 6 * 60 * 1000); // 6 minutes later
    expect(dataService.isDataStale()).toBe(true);

    // Check if data is fresh within cache duration
    mockNow.mockReturnValue(1000 + 2 * 60 * 1000); // 2 minutes later
    expect(dataService.isDataStale()).toBe(false);

    Date.now = originalNow;
  });
});
