"""
Script to save a fictional shampoo product landing page to Redis.
The frontend will load this data when accessing: http://localhost:3000?id=eco-shampoo
"""

import redis
import json
from main import LandingPage


def save_shampoo_landing_page():
    """Generate and save a fictional shampoo product landing page to Redis"""
    
    # Create fictional shampoo landing page data
    shampoo_page = LandingPage(
        product_name="Shampoo",
        page_id="eco-shampoo",
        
        # Hero Section
        hero_title="Transform Your Hair, Naturally",
        hero_subtitle="EcoShine Organic Shampoo uses 100% natural ingredients to give you salon-quality results while caring for the planet. Experience the difference of truly clean beauty.",
        hero_social_proof="Join over 50,000 happy customers worldwide",
        hero_cta_primary="Shop Now",
        hero_cta_secondary="Learn More",
        
        # Testimonials Section
        testimonials_headline="Loved By Beauty Enthusiasts Everywhere",
        testimonials=[
            {
                "name": "Emma Thompson",
                "role": "Beauty Blogger",
                "content": "This is hands down the best shampoo I've ever used! My hair has never been softer, and I love that it's completely natural. The scent is divine too!",
                "rating": 5,
                "initials": "ET"
            },
            {
                "name": "Marcus Chen",
                "role": "Hairstylist",
                "content": "I recommend EcoShine to all my clients. It's gentle enough for daily use but powerful enough to remove product buildup. A true game-changer in natural hair care.",
                "rating": 5,
                "initials": "MC"
            },
            {
                "name": "Sofia Rodriguez",
                "role": "Yoga Instructor",
                "content": "Finally, a shampoo that aligns with my values! No harsh chemicals, cruelty-free, and it leaves my hair feeling amazing. I'm never going back to conventional shampoo.",
                "rating": 5,
                "initials": "SR"
            },
            {
                "name": "David Park",
                "role": "Environmental Scientist",
                "content": "The packaging is fully recyclable and the ingredients are sustainably sourced. It's rare to find a product that performs this well while being truly eco-friendly.",
                "rating": 5,
                "initials": "DP"
            },
            {
                "name": "Isabella Martinez",
                "role": "Fitness Coach",
                "content": "I wash my hair daily after workouts, and this shampoo never dries it out. My hair feels healthier and looks shinier than ever. Worth every penny!",
                "rating": 5,
                "initials": "IM"
            },
            {
                "name": "Oliver Williams",
                "role": "Organic Lifestyle Advocate",
                "content": "EcoShine proves that natural products can outperform synthetic ones. My whole family uses it now. It's gentle on kids' hair too!",
                "rating": 5,
                "initials": "OW"
            }
        ],
        
        # Features Section
        features_headline="Why Choose EcoShine?",
        features=[
            {
                "icon": "Leaf",
                "title": "100% Natural",
                "description": "Made with organic botanicals and essential oils. No sulfates, parabens, or synthetic fragrances. Just pure, plant-powered goodness."
            },
            {
                "icon": "Sparkles",
                "title": "Salon Results",
                "description": "Professional-grade formula that cleanses deeply while nourishing your hair. Get that salon-fresh feeling at home."
            },
            {
                "icon": "Heart",
                "title": "All Hair Types",
                "description": "Perfect for straight, wavy, curly, or coily hair. Our gentle formula works beautifully on every texture and color."
            },
            {
                "icon": "Globe",
                "title": "Planet-Friendly",
                "description": "Biodegradable formula in 100% recycled packaging. Cruelty-free and vegan. Beauty that doesn't cost the earth."
            }
        ]
    )
    
    # Convert to dict for Redis storage (matches API format)
    redis_data = {
        "id": shampoo_page.page_id,
        "productName": shampoo_page.product_name,
        "title": shampoo_page.hero_title,
        "subtitle": shampoo_page.hero_subtitle,
        "description": shampoo_page.hero_social_proof,
        "companyLogos": {
            "logo1": shampoo_page.company_logo_1,
            "logo2": shampoo_page.company_logo_2,
            "logo3": shampoo_page.company_logo_3,
            "logo4": shampoo_page.company_logo_4
        },
        "testimonial1": shampoo_page.testimonials[0] if len(shampoo_page.testimonials) > 0 else None,
        "testimonial2": shampoo_page.testimonials[1] if len(shampoo_page.testimonials) > 1 else None,
        "features": shampoo_page.features,
        "featuresHeadline": shampoo_page.features_headline,
        "testimonialsHeadline": shampoo_page.testimonials_headline,
        "allTestimonials": shampoo_page.testimonials
    }
    
    # Connect to Redis
    try:
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        r.ping()
        print("✅ Connected to Redis")
    except redis.ConnectionError:
        print("❌ Failed to connect to Redis. Make sure Redis is running.")
        print("   Start Redis with: docker-compose up -d redis")
        return
    
    # Save to Redis with key format: page:{page_id}
    redis_key = f"page:{shampoo_page.page_id}"
    r.set(redis_key, json.dumps(redis_data))
    
    print(f"\n✅ Successfully saved shampoo landing page to Redis!")
    print(f"   Redis key: {redis_key}")
    print(f"   Page ID: {shampoo_page.page_id}")
    print(f"\n🌐 View the page at:")
    print(f"   http://localhost:3000?id={shampoo_page.page_id}")
    print(f"\n📋 Page Details:")
    print(f"   Title: {shampoo_page.hero_title}")
    print(f"   Subtitle: {shampoo_page.hero_subtitle[:80]}...")
    print(f"   Features: {len(shampoo_page.features)}")
    print(f"   Testimonials: {len(shampoo_page.testimonials)}")


if __name__ == "__main__":
    save_shampoo_landing_page()
