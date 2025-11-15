from pydantic import BaseModel
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class Feature:
	"""A product feature with icon, title, and description"""
	icon_name: str  # e.g., "Recycle", "Grip", "Wrench", "Sparkles"
	title: str
	description: str


@dataclass
class Testimonial:
	"""A customer testimonial"""
	name: str
	role: str
	content: str
	rating: int  # 1-5
	avatar_url: Optional[str] = None


@dataclass
class CompanyLogos:
	"""Company logos for social proof"""
	logo1: Optional[str] = None
	logo2: Optional[str] = None
	logo3: Optional[str] = None
	logo4: Optional[str] = None


@dataclass
class SocialProof:
	"""Social proof metrics"""
	happy_users_count: int = 10000
	items_saved_count: int = 50000
	average_rating: float = 4.9
	total_reviews: int = 2000


class LandingPage(BaseModel):
	"""
	Complete landing page template data structure.

	All customizable fields for generating a product landing page with:
	- Hero section with title, subtitle, social proof
	- Company logos
	- Testimonials section
	- Features/UVP section
	"""

	product_name: str = "LambdaPen"

	# Page ID
	page_id: str = "default"

	# HERO SECTION
	hero_title: str = "Every Pencil Deserves a Second Life"
	hero_subtitle: str = "LambdaPen extends your short pencils, giving you perfect grip and control. Write more, waste less, create endlessly."
	hero_social_proof: str = "Join thousands of satisfied users worldwide"
	hero_image_url: Optional[str] = None
	hero_cta_primary: str = "Get Your LambdaPen"
	hero_cta_secondary: str = "Learn More"

	# COMPANY LOGOS (Social Proof)
	company_logo_1: Optional[str] = None
	company_logo_2: Optional[str] = None
	company_logo_3: Optional[str] = None
	company_logo_4: Optional[str] = None

	# TESTIMONIALS SECTION
	testimonials_headline: str = "Loved By Creators Everywhere"
	testimonials: List[dict] = [
		{
			"name": "Sarah Mitchell",
			"role": "Artist & Illustrator",
			"content": "As an artist, I go through pencils quickly. LambdaPen has been a game-changer - I can use every pencil down to the last inch. It's saved me money and reduced waste significantly.",
			"rating": 5,
			"initials": "SM"
		},
		{
			"name": "James Chen",
			"role": "Architecture Student",
			"content": "The grip is perfect for long sketching sessions. I used to throw away perfectly good pencils just because they got too short. Not anymore! This is brilliant engineering.",
			"rating": 5,
			"initials": "JC"
		},
		{
			"name": "Emily Rodriguez",
			"role": "Elementary School Teacher",
			"content": "I bought these for my entire classroom. The kids love them, and we're teaching sustainability in a practical way. Parents are asking where to get them!",
			"rating": 5,
			"initials": "ER"
		},
		{
			"name": "Michael Thompson",
			"role": "Graphic Designer",
			"content": "Quality craftsmanship and it actually works as advertised. The aluminum feels premium and the twist-lock mechanism is smooth. Worth every penny.",
			"rating": 5,
			"initials": "MT"
		},
		{
			"name": "Lisa Park",
			"role": "Writer & Poet",
			"content": "I'm old-fashioned and love writing with pencils. LambdaPen lets me hold onto my favorites longer. Simple, elegant solution to a real problem.",
			"rating": 5,
			"initials": "LP"
		},
		{
			"name": "David Kumar",
			"role": "Engineering Student",
			"content": "Perfect for technical drawing. The balance is excellent even with short pencils. My drafting work has never been more precise.",
			"rating": 5,
			"initials": "DK"
		}
	]

	# FEATURES SECTION (UVP - Unique Value Propositions)
	features_headline: str = "Why Choose LambdaPen?"
	features: List[dict] = [
		{
			"icon": "Recycle",
			"title": "Eco-Friendly",
			"description": "Reduce waste by extending the life of your pencils. Each LambdaPen saves dozens of pencils from the trash."
		},
		{
			"icon": "Grip",
			"title": "Perfect Grip",
			"description": "Ergonomic design provides comfortable writing experience, even with the shortest pencils."
		},
		{
			"icon": "Wrench",
			"title": "Universal Fit",
			"description": "Works with all standard pencils. Simple twist mechanism locks your pencil securely in place."
		},
		{
			"icon": "Sparkles",
			"title": "Premium Quality",
			"description": "Crafted from durable aluminum with a smooth finish. Built to last for years of daily use."
		}
	]

	class Config:
		arbitrary_types_allowed = True
