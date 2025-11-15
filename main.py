#!/usr/bin/env python3
"""
Main script to enrich Redis database with LinkedIn profile data.

Usage:
    python main.py <linkedin_url>

Example:
    python main.py https://www.linkedin.com/in/roxannevarza/
"""

import sys
from scraper.linkedin_scraper import enrich_redis_with_linkedin_data
import json


def main():
    # Check if LinkedIn URL was provided
    if len(sys.argv) < 2:
        print("❌ Error: LinkedIn URL required")
        print("\nUsage:")
        print("  python main.py <linkedin_url>")
        print("\nExample:")
        print("  python main.py https://www.linkedin.com/in/roxannevarza/")
        sys.exit(1)
    
    linkedin_url = sys.argv[1]
    
    # Validate URL format
    if "linkedin.com/in/" not in linkedin_url:
        print("❌ Error: Invalid LinkedIn profile URL")
        print("URL must be in format: https://www.linkedin.com/in/username/")
        sys.exit(1)
    
    print("="*70)
    print("🚀 LinkedIn to Landing Page - AI-Powered Workflow")
    print("="*70)
    print(f"\n📍 LinkedIn Profile: {linkedin_url}")
    print()
    
    # Run the enrichment workflow
    result = enrich_redis_with_linkedin_data(linkedin_url, use_llm=True)
    
    print("\n" + "="*70)
    print("📊 RESULT")
    print("="*70)
    
    if result.get("success"):
        print("\n✅ Success! Landing page created and stored in Redis")
        print(f"\n🌐 View your personalized landing page at:")
        print(f"   http://localhost:3000?id={result['page_id']}")
        print(f"\n📄 Page Data:")
        print(json.dumps(result['data'], indent=2))
    else:
        print(f"\n❌ Failed to create landing page")
        print(f"   Error: {result.get('error', 'Unknown error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
