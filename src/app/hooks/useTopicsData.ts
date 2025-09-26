'use client';

import { useState, useEffect, useCallback } from 'react';
import { DataState } from '../types';
import { dataService } from '../services/dataService';

export function useTopicsData() {
  const [dataState, setDataState] = useState<DataState>({
    topics: [],
    categories: [],
    loading: true,
    error: null,
    lastUpdated: null,
  });
  const [refreshKey, setRefreshKey] = useState(0);

  const fetchData = useCallback(async (forceRefresh: boolean = false) => {
    try {
      console.log('useTopicsData: Starting fetch, forceRefresh:', forceRefresh);
      setDataState(prev => ({ ...prev, loading: true, error: null }));
      
      const response = await dataService.fetchTopics(forceRefresh);
      console.log('useTopicsData: Received response:', response);
      const categories = dataService.getCategories(response.topics);
      
      setDataState({
        topics: response.topics,
        categories,
        loading: false,
        error: null,
        lastUpdated: response.generatedAt,
      });
      console.log('useTopicsData: State updated with', response.topics.length, 'topics');
    } catch (error) {
      console.error('Error fetching topics data:', error);
      setDataState(prev => ({
        ...prev,
        loading: false,
        error: error instanceof Error ? error.message : 'Failed to fetch data',
      }));
    }
  }, []);

  const refreshData = useCallback(async () => {
    console.log('useTopicsData: refreshData called');
    setRefreshKey(prev => prev + 1); // Force re-render
    await fetchData(true);
  }, [fetchData]);

  // Initial data fetch
  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // Auto-refresh if data is stale
  useEffect(() => {
    const checkStaleness = () => {
      if (dataService.isDataStale() && !dataState.loading) {
        console.log('Data is stale, refreshing...');
        fetchData(true);
      }
    };

    // Check every minute
    const interval = setInterval(checkStaleness, 60000);
    
    return () => clearInterval(interval);
  }, [dataState.loading, fetchData]);

  return {
    ...dataState,
    refreshData,
    isStale: dataService.isDataStale(),
    refreshKey, // Include refresh key to force re-renders
  };
}
