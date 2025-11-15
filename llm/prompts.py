from decouple import config
from mistralai import Mistral
import json

# Initialize the client with your API key
api_key = config("MISTRAL_KEY")
client = Mistral(api_key=api_key)


def generate_lambdapen_content(job_title, recent_posts):
	"""
	Generate personalized LambdaPen landing page content based on LinkedIn profile data.

	Args:
		job_title (str): User's job title/occupation from LinkedIn
		recent_posts (list): List of text content from their 2 most recent LinkedIn posts

	Returns:
		dict: {"title": str, "subtitle": str, "description": str}
	"""

	# Format posts for the prompt
	posts_text = "\n".join([f"Post {i+1}: {post}" for i, post in enumerate(recent_posts)])

	prompt = f"""You are a copywriting expert for LambdaPen, a pencil extension tool.

Product: LambdaPen extends short pencils, giving perfect grip and control. Sustainable, creative solution.

User Context:
- Job: {job_title}
- Recent Posts:
{posts_text}

Create personalized landing page content that resonates with this professional based on their role and interests shown in their recent posts.

Return ONLY valid JSON:
{{
  "title": "60 chars max - compelling headline relating to their work",
  "subtitle": "150 chars max - value proposition in their context",
  "description": "100 chars max - personal touch or urgency"
}}

Guidelines:
- Creative roles: emphasize creativity, waste reduction
- Business roles: efficiency, sustainability  
- Education: practical benefits for teaching
- Tech: precision, innovation
- Professional tone, authentic, not salesy

Return ONLY the JSON, nothing else."""

	try:
		response = client.chat.complete(
			model="mistral-small-latest",
			messages=[{"role": "user", "content": prompt}],
			temperature=0.7,
			max_tokens=500
		)

		content = response.choices[0].message.content.strip()

		# Try to extract JSON if wrapped in code blocks
		if "```json" in content:
			content = content.split("```json")[1].split("```")[0].strip()
		elif "```" in content:
			content = content.split("```")[1].split("```")[0].strip()

		result = json.loads(content)

		if not all(key in result for key in ["title", "subtitle", "description"]):
			raise ValueError("Missing required fields")

		print(f"✅ Generated LambdaPen content for: {job_title}")

		return result

	except Exception as e:
		print(f"❌ Error generating content: {e}")
		return {
			"title": "Every Pencil Deserves a Second Life",
			"subtitle": "LambdaPen extends your short pencils, giving you perfect grip and control.",
			"description": "Write more, waste less, create endlessly."
		}


def describe_image_from_url(image_url: str, prompt: str = None) -> str:


	if prompt is None:
		prompt = """
		Describe the person in the image. Age gender, hair color, ethnicity, clothing. if there is none, provide a description of a random person
		
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
