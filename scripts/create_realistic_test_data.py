#!/usr/bin/env python3
"""
Create realistic test data with actual trending topic names
"""

import json
import random
from datetime import datetime, timedelta

def generate_realistic_topics():
    """Generate realistic trending topics with actual names"""
    
    # Real trending topics by category
    trending_topics = {
        "ai-tools": [
            "ChatGPT-5",
            "Claude 3.5 Sonnet",
            "Midjourney v6",
            "Perplexity AI",
            "Notion AI",
            "Jasper AI",
            "Copy.ai",
            "Runway ML",
            "Stable Diffusion 3",
            "DALL-E 3",
            "Sora AI",
            "Gemini Pro",
            "Anthropic Claude",
            "OpenAI GPT-4",
            "Character.AI"
        ],
        "tech": [
            "Apple Vision Pro",
            "Meta Quest 3",
            "Tesla Cybertruck",
            "iPhone 16 Pro",
            "Samsung Galaxy S24",
            "Google Pixel 8",
            "MacBook Pro M3",
            "iPad Pro 2024",
            "AirPods Pro 3",
            "Apple Watch Series 9",
            "PlayStation 5 Pro",
            "Xbox Series X",
            "Nintendo Switch 2",
            "Steam Deck OLED",
            "Meta Ray-Ban"
        ],
        "business": [
            "Remote Work",
            "Hybrid Teams",
            "Digital Nomad",
            "Freelance Economy",
            "Gig Economy",
            "Startup Funding",
            "Venture Capital",
            "IPO Market",
            "Cryptocurrency",
            "Bitcoin ETF",
            "NFT Market",
            "Web3",
            "Blockchain",
            "DeFi",
            "Metaverse"
        ],
        "science": [
            "CRISPR Gene Editing",
            "Quantum Computing",
            "SpaceX Starship",
            "James Webb Telescope",
            "Mars Exploration",
            "Climate Change",
            "Renewable Energy",
            "Solar Power",
            "Wind Energy",
            "Electric Vehicles",
            "Battery Technology",
            "Nuclear Fusion",
            "Artificial Intelligence",
            "Machine Learning",
            "Neural Networks"
        ]
    }
    
    # Generate realistic data
    topics = []
    topic_id = 1
    
    for category, terms in trending_topics.items():
        # Select 2-4 random terms from each category
        num_topics = random.randint(2, 4)
        selected_terms = random.sample(terms, min(num_topics, len(terms)))
        
        for term in selected_terms:
            # Generate realistic sparkline data
            sparkline = generate_sparkline()
            
            # Calculate realistic metrics
            volume = random.randint(500, 50000)
            percent_change = random.randint(20, 500)
            score = calculate_score(sparkline, percent_change)
            
            # Generate realistic dates
            first_seen = generate_first_seen_date()
            last_seen = datetime.now().isoformat()
            
            # Generate related queries
            related_queries = generate_related_queries(term, category)
            
            topic = {
                "term": term,
                "category": category,
                "score": round(score, 1),
                "percentChange": percent_change,
                "sparkline": sparkline,
                "firstSeen": first_seen,
                "lastSeen": last_seen,
                "volume": volume,
                "relatedQueries": related_queries
            }
            
            topics.append(topic)
            topic_id += 1
    
    # Sort by score (highest first)
    topics.sort(key=lambda x: x['score'], reverse=True)
    
    return topics

def generate_sparkline():
    """Generate realistic sparkline data"""
    # Start with a base value
    base_value = random.randint(10, 50)
    sparkline = [base_value]
    
    # Generate 7 more data points with realistic trends
    for i in range(7):
        # Add some randomness but generally trending upward
        change = random.randint(-5, 15)
        new_value = max(5, sparkline[-1] + change)
        sparkline.append(new_value)
    
    # Ensure the last value is the highest (trending up)
    sparkline[-1] = max(sparkline) + random.randint(5, 20)
    
    return sparkline

def calculate_score(sparkline, percent_change):
    """Calculate a realistic score based on sparkline and percent change"""
    # Base score from percent change
    base_score = min(10, percent_change / 50)
    
    # Add score for trend consistency
    trend_score = 0
    for i in range(1, len(sparkline)):
        if sparkline[i] > sparkline[i-1]:
            trend_score += 0.5
    
    # Add score for recent growth
    recent_growth = (sparkline[-1] - sparkline[-3]) / sparkline[-3] if sparkline[-3] > 0 else 0
    growth_score = min(3, recent_growth * 2)
    
    total_score = base_score + trend_score + growth_score
    return min(10, max(1, total_score))

def generate_first_seen_date():
    """Generate a realistic first seen date"""
    # Random date between 6 months ago and 2 years ago
    days_ago = random.randint(180, 730)
    first_seen = datetime.now() - timedelta(days=days_ago)
    return first_seen.isoformat()

def generate_related_queries(term, category):
    """Generate realistic related queries"""
    related_queries_map = {
        "ai-tools": [
            "AI automation",
            "Machine learning",
            "Artificial intelligence",
            "AI productivity",
            "Smart tools",
            "AI assistance"
        ],
        "tech": [
            "Technology trends",
            "Innovation",
            "Digital transformation",
            "Tech news",
            "Future tech",
            "Tech reviews"
        ],
        "business": [
            "Business strategy",
            "Market trends",
            "Entrepreneurship",
            "Business growth",
            "Industry news",
            "Business innovation"
        ],
        "science": [
            "Scientific research",
            "Technology breakthrough",
            "Innovation",
            "Research findings",
            "Scientific discovery",
            "Tech advancement"
        ]
    }
    
    # Get 2-3 random related queries
    available_queries = related_queries_map.get(category, ["Related topic", "Trending", "Popular"])
    num_queries = random.randint(2, 3)
    return random.sample(available_queries, min(num_queries, len(available_queries)))

def main():
    """Generate and save realistic test data"""
    print("🚀 Generating realistic trending topics...")
    
    topics = generate_realistic_topics()
    
    # Create the response structure
    response = {
        "generatedAt": datetime.now().isoformat(),
        "totalTopics": len(topics),
        "topics": topics
    }
    
    # Save to latest.json
    output_file = "public/data/latest.json"
    with open(output_file, 'w') as f:
        json.dump(response, f, indent=2)
    
    print(f"✅ Generated {len(topics)} realistic trending topics")
    print(f"📁 Saved to {output_file}")
    
    # Print sample topics
    print("\n📊 Sample topics:")
    for i, topic in enumerate(topics[:3]):
        print(f"  {i+1}. {topic['term']} ({topic['category']}) - Score: {topic['score']}, Growth: +{topic['percentChange']}%")

if __name__ == "__main__":
    main()
