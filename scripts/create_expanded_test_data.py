#!/usr/bin/env python3
"""
Create expanded test data with more categories and realistic topics
"""

import json
import random
from datetime import datetime, timezone

def generate_expanded_topics():
    """Generate realistic trending topics with expanded categories"""
    
    # Expanded categories with realistic trending topics
    trending_topics = {
        "ai-tech": [
            "ChatGPT-5", "Claude 3.5 Sonnet", "Midjourney v6", "Perplexity AI", 
            "Notion AI", "Jasper AI", "Copy.ai", "Runway ML", "Stable Diffusion 3", 
            "DALL-E 3", "Sora AI", "Gemini Pro", "Anthropic Claude", "OpenAI GPT-4", 
            "Character.AI", "GPT-4o", "ChatGPT Plus", "AI Art Generator", "AI Writing Tools"
        ],
        "business-finance": [
            "Remote Work", "Hybrid Teams", "Digital Nomad", "Freelance Economy", 
            "Gig Economy", "Startup Funding", "Venture Capital", "IPO Market", 
            "Cryptocurrency", "Bitcoin ETF", "NFT Market", "Web3", "Blockchain", 
            "DeFi", "Metaverse", "Business Automation", "SaaS Tools", "E-commerce Growth"
        ],
        "lifestyle-beauty": [
            "Skincare Routine", "Clean Beauty", "Sustainable Fashion", "Minimalist Living", 
            "Wellness Trends", "Mental Health", "Self-Care", "Fitness Apps", 
            "Healthy Eating", "Plant-Based Diet", "Meditation Apps", "Sleep Optimization",
            "Beauty Tech", "Anti-Aging", "Hair Care", "Makeup Trends", "Fragrance"
        ],
        "science-health": [
            "CRISPR Gene Editing", "Quantum Computing", "SpaceX Starship", 
            "James Webb Telescope", "Mars Exploration", "Climate Change", 
            "Renewable Energy", "Solar Power", "Wind Energy", "Electric Vehicles", 
            "Battery Technology", "Nuclear Fusion", "Artificial Intelligence", 
            "Machine Learning", "Neural Networks", "Biotech Breakthroughs", "Medical AI"
        ],
        "creative-design": [
            "UI/UX Design", "Graphic Design", "Web Design", "Brand Identity", 
            "Logo Design", "Typography", "Color Theory", "Design Systems", 
            "Figma", "Adobe Creative Suite", "Canva", "Design Thinking", 
            "Creative Coding", "Motion Graphics", "3D Design", "Illustration"
        ],
        "gaming-entertainment": [
            "Gaming Trends", "Esports", "Streaming", "Twitch", "YouTube Gaming", 
            "Mobile Games", "Console Games", "PC Gaming", "VR Gaming", 
            "AR Gaming", "Game Development", "Indie Games", "Gaming Hardware", 
            "Gaming Accessories", "Gaming Culture", "Gaming Communities"
        ],
        "food-travel": [
            "Food Trends", "Cooking", "Restaurant Tech", "Food Delivery", 
            "Sustainable Food", "Plant-Based", "Food Photography", "Culinary Arts", 
            "Travel Tech", "Sustainable Travel", "Digital Nomad", "Remote Work", 
            "Travel Apps", "Adventure Travel", "Cultural Tourism", "Food Tourism"
        ],
        "fitness-sports": [
            "Fitness Trends", "Home Workouts", "Gym Tech", "Wearable Tech", 
            "Fitness Apps", "Nutrition", "Sports Science", "Athletic Performance", 
            "Recovery", "Mental Training", "Sports Psychology", "Team Sports", 
            "Individual Sports", "Outdoor Activities", "Adventure Sports"
        ]
    }
    
    # Generate realistic data
    topics = []
    
    for category, terms in trending_topics.items():
        # Select 3-5 random terms from each category
        num_topics = random.randint(3, 5)
        selected_terms = random.sample(terms, min(num_topics, len(terms)))
        
        for term in selected_terms:
            # Generate realistic sparkline data
            sparkline = generate_sparkline()
            
            # Calculate realistic metrics
            volume = random.randint(500, 100000)
            percent_change = random.randint(20, 800)
            score = calculate_score(sparkline, percent_change)
            
            # Generate realistic dates
            first_seen = generate_first_seen_date()
            last_seen = datetime.now(timezone.utc).isoformat()
            
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
    first_seen = datetime.now(timezone.utc) - timedelta(days=days_ago)
    return first_seen.isoformat()

def generate_related_queries(term, category):
    """Generate realistic related queries"""
    related_queries_map = {
        "ai-tech": [
            "AI automation", "Machine learning", "Artificial intelligence", 
            "AI productivity", "Smart tools", "AI assistance", "Tech innovation"
        ],
        "business-finance": [
            "Business strategy", "Market trends", "Entrepreneurship", 
            "Business growth", "Industry news", "Business innovation", "Finance tech"
        ],
        "lifestyle-beauty": [
            "Lifestyle trends", "Beauty tips", "Wellness", "Self-care", 
            "Health trends", "Beauty products", "Lifestyle brands"
        ],
        "science-health": [
            "Scientific research", "Technology breakthrough", "Innovation", 
            "Research findings", "Scientific discovery", "Tech advancement", "Health tech"
        ],
        "creative-design": [
            "Design trends", "Creative tools", "Design inspiration", 
            "Creative process", "Design thinking", "Creative skills", "Design tools"
        ],
        "gaming-entertainment": [
            "Gaming culture", "Entertainment trends", "Gaming community", 
            "Gaming news", "Entertainment tech", "Gaming events", "Streaming"
        ],
        "food-travel": [
            "Food culture", "Travel trends", "Culinary arts", 
            "Travel experiences", "Food experiences", "Travel tech", "Food tech"
        ],
        "fitness-sports": [
            "Fitness trends", "Sports culture", "Athletic performance", 
            "Fitness community", "Sports tech", "Fitness apps", "Sports science"
        ]
    }
    
    # Get 2-3 random related queries
    available_queries = related_queries_map.get(category, ["Related topic", "Trending", "Popular"])
    num_queries = random.randint(2, 3)
    return random.sample(available_queries, min(num_queries, len(available_queries)))

def main():
    """Generate and save expanded test data"""
    print("🚀 Generating expanded trending topics...")
    
    topics = generate_expanded_topics()
    
    # Create the response structure
    response = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "totalTopics": len(topics),
        "topics": topics
    }
    
    # Save to latest.json
    output_file = "public/data/latest.json"
    with open(output_file, 'w') as f:
        json.dump(response, f, indent=2)
    
    print(f"✅ Generated {len(topics)} expanded trending topics")
    print(f"📁 Saved to {output_file}")
    
    # Print category breakdown
    categories = {}
    for topic in topics:
        cat = topic['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\n📊 Category breakdown:")
    for category, count in sorted(categories.items()):
        print(f"  {category}: {count} topics")
    
    # Print sample topics
    print("\n📊 Sample topics:")
    for i, topic in enumerate(topics[:5]):
        print(f"  {i+1}. {topic['term']} ({topic['category']}) - Score: {topic['score']}, Growth: +{topic['percentChange']}%")

if __name__ == "__main__":
    from datetime import timedelta
    main()
