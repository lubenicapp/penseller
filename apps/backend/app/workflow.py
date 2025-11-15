"""
Workflow for generating landing pages from LinkedIn data and product descriptions.
"""
from app.fal.text_to_image import generate_image
from app.llm.prompts import describe_person_from_url, generate_image_prompt, generate_landing_page_content
from app.scraper.linkedin_scraper import get_basic_data, get_reactions, BasicData, Reactor
from typing import List
import redis
import json
import os


def fetch_linkedin_data(linkedin_url: str) -> tuple[BasicData, List[Reactor]]:
    """
    Fetch basic data and reactors from a LinkedIn profile.

    Args:
        linkedin_url: LinkedIn profile URL

    Returns:
        Tuple of (BasicData, List[Reactor])
    """
    # Get basic profile data and recent posts
    basic_data = get_basic_data(linkedin_url, post_count=2)

    # Get reactors from the most recent post (if available)
    reactors = []
    if basic_data.last_posts_urls:
        most_recent_post = basic_data.last_posts_urls[0]
        try:
            reactors = get_reactions(most_recent_post)
        except Exception:
            reactors = []

    return basic_data, reactors


def workflow(product_description, linkedin_url):
	base_data, reactors = fetch_linkedin_data(linkedin_url)
	lead_description = describe_person_from_url(base_data.profile_picture_url)
	image_prompt = generate_image_prompt(lead_description, product_description)
	image = generate_image(image_prompt)
	lp = generate_landing_page_content(product_description, base_data.job_title)

	# Use reactors for testimonials instead of generated ones
	testimonials = []
	for reactor in reactors[:6]:  # Take first 6 reactors
		# Extract initials from name
		name_parts = reactor.name.split()
		initials = ''.join([part[0] for part in name_parts if part])

		testimonials.append({
			"name": reactor.name,
			"role": reactor.headline,
			"content": lp["testimonials"][len(testimonials)]["content"] if len(testimonials) < len(lp["testimonials"]) else "Great product!",
			"rating": 5,
			"initials": initials,
			"profile_picture_url": reactor.profile_picture_url
		})

	# Replace generated testimonials with reactor-based ones
	lp["testimonials"] = testimonials
	lp["hero_image_url"] = image

	# Extract LinkedIn username from URL
	# URL format: https://www.linkedin.com/in/username/
	username = linkedin_url.rstrip('/').split('/')[-1]

	# Prepare data for Redis (matching API format)
	redis_data = {
		"id": username,
		"productName": lp.get("product_name"),
		"title": lp.get("hero_title"),
		"subtitle": lp.get("hero_subtitle"),
		"description": lp.get("hero_social_proof"),
		"ctaPrimary": lp.get("hero_cta_primary"),
		"ctaSecondary": lp.get("hero_cta_secondary"),
		"heroImageUrl": image,
		"companyLogos": {
			"logo1": base_data.logo_url
		},
		"features": lp.get("features"),
		"featuresHeadline": lp.get("features_headline"),
		"testimonialsHeadline": lp.get("testimonials_headline"),
		"allTestimonials": testimonials
	}

	# Save to Redis (use 'redis' as host when running in Docker)
	redis_host = os.getenv('REDIS_HOST', 'redis')
	r = redis.Redis(host=redis_host, port=6379, decode_responses=True)
	redis_key = f"page:{username}"
	r.set(redis_key, json.dumps(redis_data))

	# Log the URL to access the generated landing page
	landing_page_url = f"http://localhost:8000/landing?id={username}"
	print(f"\n✅ Landing page generated and saved to Redis!")
	print(f"📍 Access it at: {landing_page_url}\n")

	return lp

if __name__ == "__main__":
	product = ("keyboards made out of bamboo")
	linkedin = "https://www.linkedin.com/in/roxannevarza/"

	workflow(product, linkedin)
