from decouple import config
import requests

token = config('APIFY_TOKEN')

def get_posts(linkedin_url="https://www.linkedin.com/in/roxannevarza/", post_count=1):
	payload = {
		"deepScrape": False,
		"limitPerSource": post_count,
		"rawData": True,
		"urls": [
			linkedin_url
		]
	}

	url = f"https://api.apify.com/v2/acts/supreme_coder~linkedin-post/run-sync-get-dataset-items?token={token}"

	response = requests.post(url, json=payload)

	return response.json() #response.json()[0]["text"]

# [{'type': 'image', 'images': ['https://media.licdn.com/dms/image/v2/D4E22AQH1OY0i4f5syA/feedshare-shrink_800/B4EZpaept9HMAg-/0/1762454578409?e=1764806400&v=beta&t=kLUeBU2anMbNz9dCZnb6iKNwp1iFj57hHxSEnppQ1lQ'], 'isActivity': False, 'urn': 'urn:li:activity:7392270291852488704', 'url': 'https://www.linkedin.com/posts/roxannevarza_just-gonna-put-this-here-via-challenges-activity-7392270291852488704-7ZTW?utm_source=combined_share_message&utm_medium=member_desktop&rcm=ACoAABxDsfABgJsLEUdI8vdnLv9UfDiShk5adv4', 'timeSincePosted': '1w', 'shareUrn': 'urn:li:share:7392270290933874688', 'text': 'Just gonna put this here. \nVia Challenges', 'attributes': [{'start': 31, 'length': 10, 'type': 'COMPANY_NAME', 'company': {'name': 'Challenges', 'universalName': 'challenges', 'trackingId': 'Yrib2KjRTCuVWGhKF2SNkA==', 'active': True, 'showcase': False, 'entityUrn': 'urn:li:fs_miniCompany:80846', 'logoUrl': 'https://media.licdn.com/dms/image/v2/C4E0BAQE4KID6Jzqr5w/company-logo_200_200/company-logo_200_200/0/1671881075529?e=1764806400&v=beta&t=AAUmjfqSe94gTC33Vd3A_CQPt49f4ZJpqiw2BFmqoUo'}}], 'comments': [], 'reactions': [], 'numShares': 0, 'numLikes': 193, 'numComments': 9, 'canReact': True, 'canPostComments': True, 'canShare': True, 'commentingDisabled': False, 'allowedCommentersScope': 'ALL', 'rootShare': True, 'shareAudience': 'PUBLIC', 'author': {'firstName': 'Roxanne', 'lastName': 'VARZA', 'occupation': 'Director @ STATION F / Scout @ Sequoia Capital / Innovation lead for AI Summit', 'id': '10052742', 'publicId': 'roxannevarza', 'trackingId': 'wRlm+O1KRji7QaIL5II1Eg==', 'profileId': 'ACoAAACZZIYBkT_JY9FJZeU4dKd_VPKuaLfhVy4', 'picture': 'https://media.licdn.com/dms/image/v2/C4D03AQHk78uSMTKdiw/profile-displayphoto-shrink_100_100/profile-displayphoto-shrink_100_100/0/1575483889283?e=1764806400&v=beta&t=XF2cGkeNhH2t2M42_Pxt3Itfoi3j6IGUOVvLmG6_M8o', 'backgroundImage': 'https://media.licdn.com/dms/image/v2/D4E16AQGntNRcmsU7sQ/profile-displaybackgroundimage-shrink_350_1400/B4EZgZ2.C6GoAc-/0/1752780501277?e=1764806400&v=beta&t=OsFMWxI9euGkXzGi7lA4WTgzMnqiIVTKBX8BeqS76zw'}, 'authorProfileId': 'roxannevarza', 'authorProfilePicture': 'https://media.licdn.com/dms/image/v2/C4D03AQHk78uSMTKdiw/profile-displayphoto-shrink_100_100/profile-displayphoto-shrink_100_100/0/1575483889283?e=1764806400&v=beta&t=XF2cGkeNhH2t2M42_Pxt3Itfoi3j6IGUOVvLmG6_M8o', 'authorType': 'Person', 'authorHeadline': 'Director @ STATION F / Scout @ Sequoia Capital / Innovation lead for AI Summit', 'authorName': 'Roxanne VARZA', 'authorProfileUrl': 'https://www.linkedin.com/in/roxannevarza?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAACZZIYBkT_JY9FJZeU4dKd_VPKuaLfhVy4', 'authorUrn': 'urn:li:member:10052742', 'postedAtTimestamp': 1762454579318, 'postedAtISO': '2025-11-06T18:42:59.318Z', 'inputUrl': 'https://www.linkedin.com/in/roxannevarza/'}]


def get_reactions(linkedin_post_url="https://www.linkedin.com/posts/roxannevarza_just-gonna-put-this-here-via-challenges-activity-7392270291852488704-7ZTW?utm_source=combined_share_message&utm_medium=member_desktop&rcm=ACoAABxDsfABgJsLEUdI8vdnLv9UfDiShk5adv4"):
	payload = {
		"post_urls": [linkedin_post_url]
	}
	url = f"https://api.apify.com/v2/acts/apimaestro~linkedin-post-reactions/run-sync-get-dataset-items?token={token}"

	response = requests.post(url, json=payload)

	return response.json() # [{'reaction_type': 'LIKE', 'reactor': {'urn': 'ACoAAAoQphgBWMh5qLJjLLSZzFtDeBtSwBdrebA', 'name': 'Kevin Davoren', 'headline': 'VP Technology and Services Europe at IDA Ireland', 'profile_url': 'https://www.linkedin.com/in/ACoAAAoQphgBWMh5qLJjLLSZzFtDeBtSwBdrebA', 'profile_pictures': {'small': 'https://media.licdn.com/dms/image/v2/D4E03AQFLLI8N9boq-A/profile-displayphoto-shrink_100_100/profile-displayphoto-shrink_100_100/0/1713535057380?e=1764806400&v=beta&t=FRf_kaulMKmjCbTm_iHDKuLXN3phMpwAqK-suxof9vQ', 'medium': 'https://media.licdn.com/dms/image/v2/D4E03AQFLLI8N9boq-A/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1713535057380?e=1764806400&v=beta&t=Sg60r2DIv5A1iXjV49QXEVv-zaa3x_pRgXlGNmzjlfI', 'large': 'https://media.licdn.com/dms/image/v2/D4E03AQFLLI8N9boq-A/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1713535057380?e=1764806400&v=beta&t=z6504gmfvWgr-19LSK2jJNSVnHIXcNYyaWKuobSsqm0', 'original': 'https://media.licdn.com/dms/image/v2/D4E03AQFLLI8N9boq-A/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1713535057380?e=1764806400&v=beta&t=8oUxjeYP5WgzRFuHLDRW5qypVUhqH-ZYHb5paCP1pw8'}}, '_metadata': {'post_url': 'https://www.linkedin.com/posts/roxannevarza_just-gonna-put-this-here-via-challenges-activity-7392270291852488704-7ZTW?utm_source=combined_share_message&utm_medium=member_desktop&rcm=ACoAABxDsfABgJsLEUdI8vdnLv9UfDiShk5adv4', 'page_number': 1, 'total_reactions': 193}, 'input': 'https://www.linkedin.com/posts/roxannevarza_just-gonna-put-this-here-via-challenges-activity-7392270291852488704-7ZTW?utm_source=combined_share_message&utm_medium=member_desktop&rcm=ACoAABxDsfABgJsLEUdI8vdnLv9UfDiShk5adv4'}]


def get_linkedin_profile_data(linkedin_url):
	"""
	Complete workflow to extract LinkedIn profile and engagement data.

	Given a LinkedIn profile URL, returns:
	- Author's job title and company logo
	- First 2 people who reacted to their most recent post
	- Reactors' names, job titles, and profile pictures

	Args:
		linkedin_url (str): LinkedIn profile URL (e.g., "https://www.linkedin.com/in/username/")

	Returns:
		dict: Structured JSON with author info and reactors
	"""
	result = {
		"success": False,
		"author": {
			"job_title": None,
			"company_logo_url": None
		},
		"reactors": []
	}

	try:
		# Step 1: Get posts from the profile
		print(f"Fetching posts from {linkedin_url}...")
		posts_data = get_posts(linkedin_url=linkedin_url, post_count=2)

		if not posts_data or len(posts_data) == 0:
			result["error"] = "No posts found for this profile"
			return result

		first_post = posts_data[0]

		# Step 2: Extract author job title
		author_job_title = first_post.get("author", {}).get("occupation", "")
		result["author"]["job_title"] = author_job_title

		# Step 3: Extract company logo URL from attributes (if company is mentioned)
		attributes = first_post.get("attributes", [])
		company_logo_url = None
		for attr in attributes:
			if attr.get("type") == "COMPANY_NAME":
				company = attr.get("company", {})
				company_logo_url = company.get("logoUrl")
				if company_logo_url:
					break

		result["author"]["company_logo_url"] = company_logo_url

		# Step 4: Get the post URL
		post_url = first_post.get("url")
		if not post_url:
			result["error"] = "Post URL not found"
			return result

		# Step 5: Get reactions to the post
		print(f"Fetching reactions from post: {post_url}...")
		reactions_data = get_reactions(linkedin_post_url=post_url)

		if not reactions_data or len(reactions_data) == 0:
			result["error"] = "No reactions found for this post"
			result["success"] = True  # Still a success, just no reactions
			return result

		# Step 6: Extract first 2 reactors with their data
		reactors_list = []
		for reaction in reactions_data[:2]:  # Get only first 2 reactors
			reactor_data = reaction.get("reactor", {})

			reactor_info = {
				"name": reactor_data.get("name", ""),
				"job_title": reactor_data.get("headline", ""),
				"profile_picture": reactor_data.get("profile_pictures", {}).get("medium", "")
			}

			reactors_list.append(reactor_info)

		result["reactors"] = reactors_list
		result["success"] = True

		print(f"✅ Successfully extracted data for {author_job_title}")
		print(f"   Company logo: {company_logo_url}")
		print(f"   Found {len(reactors_list)} reactors")

		return result

	except Exception as e:
		result["error"] = str(e)
		print(f"❌ Error: {str(e)}")
		return result


def enrich_redis_with_linkedin_data(linkedin_url, redis_host='localhost', redis_port=6379, use_llm=True):
	"""
	Enriches Redis database with LinkedIn profile data.

	Workflow:
	1. Fetches LinkedIn profile data (author + reactors)
	2. Extracts username from LinkedIn URL
	3. Generates personalized content using LLM (optional)
	4. Creates structured page content with:
	   - AI-generated title, subtitle, description (if use_llm=True)
	   - Reactors as testimonials (first 2)
	   - Author's company logo as first company logo
	5. Stores in Redis with key: page:{username}

	Args:
		linkedin_url (str): LinkedIn profile URL
		redis_host (str): Redis host (default: localhost)
		redis_port (int): Redis port (default: 6379)
		use_llm (bool): Whether to use LLM for content generation (default: True)

	Returns:
		dict: Status and created page data
	"""
	import redis
	import json
	import re
	from llm.prompts import generate_lambdapen_content

	result = {
		"success": False,
		"page_id": None,
		"data": None
	}

	try:
		# Step 1: Get LinkedIn profile data
		print(f"📥 Fetching LinkedIn data...")
		linkedin_data = get_linkedin_profile_data(linkedin_url)

		if not linkedin_data.get("success"):
			result["error"] = linkedin_data.get("error", "Failed to fetch LinkedIn data")
			return result

		# Step 2: Extract username from LinkedIn URL
		# URL format: https://www.linkedin.com/in/username/ or https://www.linkedin.com/in/username
		username_match = re.search(r'linkedin\.com/in/([^/]+)', linkedin_url)
		if not username_match:
			result["error"] = "Could not extract username from LinkedIn URL"
			return result

		username = username_match.group(1)
		result["page_id"] = username

		# Step 3: Build page content structure
		author = linkedin_data.get("author", {})
		reactors = linkedin_data.get("reactors", [])

		# Step 3a: Generate personalized content with LLM
		if use_llm:
			print(f"🤖 Generating AI-powered content...")
			try:
				# Get the post texts from the 2 most recent posts
				posts_data = get_posts(linkedin_url=linkedin_url, post_count=2)
				recent_posts = []
				if posts_data:
					for post in posts_data[:2]:  # Ensure we get at most 2 posts
						post_text = post.get("text", "")
						if post_text:
							recent_posts.append(post_text)
				
				# If no posts found, use empty list
				if not recent_posts:
					recent_posts = [""]
				
				# Generate personalized content
				generated_content = generate_lambdapen_content(
					job_title=author.get("job_title", "Professional"),
					recent_posts=recent_posts
				)

				page_content = {
					"id": username,
					"title": generated_content.get("title"),
					"subtitle": generated_content.get("subtitle"),
					"description": generated_content.get("description")
				}
			except Exception as e:
				print(f"⚠️ LLM generation failed, using default content: {e}")
				page_content = {
					"id": username,
					"title": f"Connect with {username.replace('-', ' ').title()}",
					"subtitle": author.get("job_title", "Professional on LinkedIn"),
					"description": "Explore my latest work and connect with my network"
				}
		else:
			page_content = {
				"id": username,
				"title": f"Connect with {username.replace('-', ' ').title()}",
				"subtitle": author.get("job_title", "Professional on LinkedIn"),
				"description": "Explore my latest work and connect with my network"
			}

		# Add testimonials from reactors
		if len(reactors) >= 1:
			page_content["testimonial1"] = {
				"name": reactors[0].get("name", ""),
				"role": reactors[0].get("job_title", ""),
				"avatarUrl": reactors[0].get("profile_picture", "")
			}

		if len(reactors) >= 2:
			page_content["testimonial2"] = {
				"name": reactors[1].get("name", ""),
				"role": reactors[1].get("job_title", ""),
				"avatarUrl": reactors[1].get("profile_picture", "")
			}

		# Add company logo as first logo
		if author.get("company_logo_url"):
			page_content["companyLogos"] = {
				"logo1": author.get("company_logo_url")
			}

		# Step 4: Connect to Redis and store data
		print(f"💾 Connecting to Redis at {redis_host}:{redis_port}...")
		r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

		# Test connection
		r.ping()

		# Store in Redis
		redis_key = f"page:{username}"
		r.set(redis_key, json.dumps(page_content))

		result["success"] = True
		result["data"] = page_content

		print(f"✅ Successfully enriched Redis!")
		print(f"   Redis key: {redis_key}")
		print(f"   Page URL: http://localhost:3000?id={username}")
		print(f"   Title: {page_content['title']}")
		print(f"   Subtitle: {page_content['subtitle']}")
		if page_content.get("testimonial1"):
			print(f"   Testimonial 1: {page_content['testimonial1']['name']}")
		if page_content.get("testimonial2"):
			print(f"   Testimonial 2: {page_content['testimonial2']['name']}")
		if page_content.get("companyLogos"):
			print(f"   Company logo: {page_content['companyLogos']['logo1']}")

		return result

	except redis.ConnectionError:
		result["error"] = "Could not connect to Redis. Make sure Redis is running."
		print(f"❌ {result['error']}")
		return result
	except Exception as e:
		result["error"] = str(e)
		print(f"❌ Error: {str(e)}")
		return result

import json

# Example usage
if __name__ == "__main__":
	# Test the workflow
	linkedin_url = "https://www.linkedin.com/in/roxannevarza/"

	redis_result = enrich_redis_with_linkedin_data(linkedin_url)

	print("\nRedis Enrichment Result:")
	print(json.dumps(redis_result, indent=2))

	if redis_result.get("success"):
		print(f"\n🎉 Success! Visit: http://localhost:3000?id={redis_result['page_id']}")
