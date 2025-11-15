from decouple import config
from mistralai import Mistral
import json

# Initialize the client with your API key
api_key = config("MISTRAL_KEY")
client = Mistral(api_key=api_key)


def describe_person_from_url(image_url: str, prompt: str = None) -> str:
	if prompt is None:
		prompt = """
		Describe the person in the image. Age gender, hair color, ethnicity, clothing. and facial traits. if there is none, provide a description of a random person
		
		Give enough details to sketch him for a portrait robot
		
		The answer must be in this format :
		
		"A man in his twenties, with blonde hair, European, with blue jacket..."
		
		"""

	try:
		# Use Mistral's Pixtral vision model
		response = client.chat.complete(
			model="pixtral-12b-2409",
			messages=[
				{
					"role": "user",
					"content": [
						{
							"type": "text",
							"text": prompt
						},
						{
							"type": "image_url",
							"image_url": image_url
						}
					]
				}
			],
			temperature=0.3,
			max_tokens=1000
		)

		description = response.choices[0].message.content.strip()

		print(f"✅ Successfully described image from: {image_url}")

		return description

	except Exception as e:
		print(f"❌ Error describing image: {e}")
		raise


def generate_image_prompt(product_description: str, lead_description: str) -> str:
	"""
	Generate a detailed image prompt for text-to-image generation.

	Args:
		product_description: Description of the product
		lead_description: Description of the person (from describe_image_from_url)

	Returns:
		Detailed prompt for image generation
	"""
	prompt = f"{lead_description}, happy and satisfied while using a product like : {product_description}, professional product photography, high quality, natural lighting, lifestyle shot"

	return prompt


def generate_landing_page_content(product_description: str, job_title: str) -> dict:
	"""
	Generate complete landing page content tailored to the product and target audience.

	Args:
		product_description: Description of the product
		job_title: Job title of the target lead

	Returns:
		Dictionary with landing page content structured for LandingPage model
	"""
	prompt = f"""You are a professional copywriter specializing in landing pages. Generate compelling landing page content for the following product, tailored to appeal to someone with the job title "{job_title}".

Product Description: {product_description}

Generate a complete landing page with:

1. A catchy product name (short, memorable)
2. Hero section:
   - A compelling headline (emotional, benefit-focused)
   - A descriptive subtitle (explain what it does, how it helps)
   - Social proof text
   - Primary CTA button text
   - Secondary CTA button text

3. Four features with:
   - Icon name (choose from: Recycle, Grip, Wrench, Sparkles, Heart, Globe, Leaf, Zap, Shield, Star)
   - Feature title
   - Feature description

4. Six testimonials from different personas that would use this product (including someone with job title similar to "{job_title}"):
   - Name (realistic full name)
   - Role/job title
   - Content (specific, authentic testimonial)
   - Initials (derived from name)

5. Testimonials section headline

Return ONLY valid JSON in this exact structure, no additional text:
{{
  "product_name": "ProductName",
  "hero_title": "...",
  "hero_subtitle": "...",
  "hero_social_proof": "...",
  "hero_cta_primary": "...",
  "hero_cta_secondary": "...",
  "features_headline": "...",
  "features": [
    {{"icon": "IconName", "title": "...", "description": "..."}},
    {{"icon": "IconName", "title": "...", "description": "..."}},
    {{"icon": "IconName", "title": "...", "description": "..."}},
    {{"icon": "IconName", "title": "...", "description": "..."}}
  ],
  "testimonials_headline": "...",
  "testimonials": [
    {{"name": "...", "role": "...", "content": "...", "rating": 5, "initials": "..."}},
    {{"name": "...", "role": "...", "content": "...", "rating": 5, "initials": "..."}},
    {{"name": "...", "role": "...", "content": "...", "rating": 5, "initials": "..."}},
    {{"name": "...", "role": "...", "content": "...", "rating": 5, "initials": "..."}},
    {{"name": "...", "role": "...", "content": "...", "rating": 5, "initials": "..."}},
    {{"name": "...", "role": "...", "content": "...", "rating": 5, "initials": "..."}}
  ]
}}"""

	response = client.chat.complete(
		model="mistral-large-latest",
		messages=[
			{
				"role": "user",
				"content": prompt
			}
		],
		temperature=0.7,
		max_tokens=4000,
		response_format={"type": "json_object"}
	)

	content = response.choices[0].message.content
	return json.loads(content)
