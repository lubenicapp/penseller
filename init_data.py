#!/usr/bin/env python3
"""
Initialize sample data in Redis for the landing page application.
This script populates the Redis database with example page content.
"""

import redis
import json
import sys

def init_sample_data():
    """Initialize Redis with sample page content"""
    try:
        # Connect to Redis
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        
        # Test connection
        r.ping()
        print("✓ Connected to Redis successfully")
        
        # Sample page contents
        pages = [
            {
                "id": "default",
                "title": "Every Pencil Deserves a Second Life",
                "subtitle": "LambdaPen extends your short pencils, giving you perfect grip and control. Write more, waste less, create endlessly.",
                "description": "Join thousands of satisfied users worldwide!"
            },
            {
                "id": "123456",
                "title": "Welcome to Your Custom Landing Page",
                "subtitle": "This content is loaded dynamically from Redis based on the URL parameter ?id=123456",
                "description": "You can customize this content for any ID you want!",
                "testimonial1": {
                    "name": "Alex Johnson",
                    "role": "Professional Designer",
                    "avatarUrl": "https://api.dicebear.com/7.x/avataaars/svg?seed=Alex"
                },
                "testimonial2": {
                    "name": "Maria Garcia",
                    "role": "Creative Director",
                    "avatarUrl": "https://api.dicebear.com/7.x/avataaars/svg?seed=Maria"
                },
                "companyLogos": {
                    "logo1": "https://logo.clearbit.com/google.com",
                    "logo2": "https://logo.clearbit.com/microsoft.com",
                    "logo3": "https://logo.clearbit.com/apple.com",
                    "logo4": "https://logo.clearbit.com/amazon.com"
                }
            },
            {
                "id": "promo-2024",
                "title": "Special Promotion 2024",
                "subtitle": "Get 50% off on all LambdaPen products this month only!",
                "description": "Limited time offer - Don't miss out on this amazing deal!",
                "testimonial1": {
                    "name": "Robert Chen",
                    "role": "Tech Entrepreneur",
                    "avatarUrl": "https://api.dicebear.com/7.x/avataaars/svg?seed=Robert"
                },
                "testimonial2": {
                    "name": "Emma Williams",
                    "role": "UX Designer"
                }
            },
            {
                "id": "education",
                "title": "LambdaPen for Education",
                "subtitle": "Perfect for schools and universities. Reduce waste, increase sustainability.",
                "description": "Bulk discounts available for educational institutions.",
                "testimonial1": {
                    "name": "Dr. Jennifer Smith",
                    "role": "University Professor"
                },
                "testimonial2": {
                    "name": "Michael Brown",
                    "role": "School Principal",
                    "avatarUrl": "https://api.dicebear.com/7.x/avataaars/svg?seed=Michael"
                }
            }
        ]
        
        # Store each page in Redis
        for page in pages:
            key = f"page:{page['id']}"
            r.set(key, json.dumps(page))
            print(f"✓ Created page: {page['id']}")
            print(f"  Title: {page['title']}")
            print(f"  URL: http://localhost:3000?id={page['id']}")
            print()
        
        print(f"\n✅ Successfully initialized {len(pages)} pages in Redis")
        print("\nYou can now access the landing page with different content by using:")
        print("  • http://localhost:3000 (default content)")
        print("  • http://localhost:3000?id=123456")
        print("  • http://localhost:3000?id=promo-2024")
        print("  • http://localhost:3000?id=education")
        
        return True
        
    except redis.ConnectionError:
        print("❌ Error: Could not connect to Redis")
        print("Make sure Redis is running: docker-compose up -d redis")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = init_sample_data()
    sys.exit(0 if success else 1)
