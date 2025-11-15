from decouple import config
import requests
from pydantic import BaseModel
from typing import List

token = config('APIFY_TOKEN')

class BasicData(BaseModel):
	first_name: str
	last_name: str
	profile_picture_url: str
	job_title: str
	last_posts_urls : List[str]
	logo_url: str

class Reactor(BaseModel):
	reaction_type: str
	name: str
	headline: str
	profile_url: str
	profile_picture_url: str

def get_basic_data(linkedin_url="https://www.linkedin.com/in/roxannevarza/", post_count=2) -> BasicData:
	"""
	Get basic data from a LinkedIn profile formatted as BasicData BaseModel.

	Args:
		linkedin_url (str): LinkedIn profile URL
		post_count (int): Number of recent posts to fetch (default: 2)

	Returns:
		BasicData: Structured profile data with first_name, last_name, profile_picture_url,
		           job_title, and last_posts_urls

	Example response structure shown in comment on line 31
	"""
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
	posts_data = response.json()

	if not posts_data or len(posts_data) == 0:
		raise ValueError(f"No posts found for LinkedIn profile: {linkedin_url}")

	# Extract data from the first post's author information
	first_post = posts_data[0]
	author = first_post.get("author", {})

	# Extract post URLs from all fetched posts
	post_urls = [post.get("url", "") for post in posts_data if post.get("url")]

	# Create and return BasicData object
	basic_data = BasicData(
		first_name=author.get("firstName", ""),
		last_name=author.get("lastName", ""),
		profile_picture_url=author.get("picture", ""),
		job_title=author.get("occupation", ""),
		logo_url=author.get("logoUrl", ""),
		last_posts_urls=post_urls
	)

	return basic_data

# [{'type': 'image', 'images': ['https://media.licdn.com/dms/image/v2/D4E22AQH1OY0i4f5syA/feedshare-shrink_800/B4EZpaept9HMAg-/0/1762454578409?e=1764806400&v=beta&t=kLUeBU2anMbNz9dCZnb6iKNwp1iFj57hHxSEnppQ1lQ'], 'isActivity': False, 'urn': 'urn:li:activity:7392270291852488704', 'url': 'https://www.linkedin.com/posts/roxannevarza_just-gonna-put-this-here-via-challenges-activity-7392270291852488704-7ZTW?utm_source=combined_share_message&utm_medium=member_desktop&rcm=ACoAABxDsfABgJsLEUdI8vdnLv9UfDiShk5adv4', 'timeSincePosted': '1w', 'shareUrn': 'urn:li:share:7392270290933874688', 'text': 'Just gonna put this here. \nVia Challenges', 'attributes': [{'start': 31, 'length': 10, 'type': 'COMPANY_NAME', 'company': {'name': 'Challenges', 'universalName': 'challenges', 'trackingId': 'Yrib2KjRTCuVWGhKF2SNkA==', 'active': True, 'showcase': False, 'entityUrn': 'urn:li:fs_miniCompany:80846', 'logoUrl': 'https://media.licdn.com/dms/image/v2/C4E0BAQE4KID6Jzqr5w/company-logo_200_200/company-logo_200_200/0/1671881075529?e=1764806400&v=beta&t=AAUmjfqSe94gTC33Vd3A_CQPt49f4ZJpqiw2BFmqoUo'}}], 'comments': [], 'reactions': [], 'numShares': 0, 'numLikes': 193, 'numComments': 9, 'canReact': True, 'canPostComments': True, 'canShare': True, 'commentingDisabled': False, 'allowedCommentersScope': 'ALL', 'rootShare': True, 'shareAudience': 'PUBLIC', 'author': {'firstName': 'Roxanne', 'lastName': 'VARZA', 'occupation': 'Director @ STATION F / Scout @ Sequoia Capital / Innovation lead for AI Summit', 'id': '10052742', 'publicId': 'roxannevarza', 'trackingId': 'wRlm+O1KRji7QaIL5II1Eg==', 'profileId': 'ACoAAACZZIYBkT_JY9FJZeU4dKd_VPKuaLfhVy4', 'picture': 'https://media.licdn.com/dms/image/v2/C4D03AQHk78uSMTKdiw/profile-displayphoto-shrink_100_100/profile-displayphoto-shrink_100_100/0/1575483889283?e=1764806400&v=beta&t=XF2cGkeNhH2t2M42_Pxt3Itfoi3j6IGUOVvLmG6_M8o', 'backgroundImage': 'https://media.licdn.com/dms/image/v2/D4E16AQGntNRcmsU7sQ/profile-displaybackgroundimage-shrink_350_1400/B4EZgZ2.C6GoAc-/0/1752780501277?e=1764806400&v=beta&t=OsFMWxI9euGkXzGi7lA4WTgzMnqiIVTKBX8BeqS76zw'}, 'authorProfileId': 'roxannevarza', 'authorProfilePicture': 'https://media.licdn.com/dms/image/v2/C4D03AQHk78uSMTKdiw/profile-displayphoto-shrink_100_100/profile-displayphoto-shrink_100_100/0/1575483889283?e=1764806400&v=beta&t=XF2cGkeNhH2t2M42_Pxt3Itfoi3j6IGUOVvLmG6_M8o', 'authorType': 'Person', 'authorHeadline': 'Director @ STATION F / Scout @ Sequoia Capital / Innovation lead for AI Summit', 'authorName': 'Roxanne VARZA', 'authorProfileUrl': 'https://www.linkedin.com/in/roxannevarza?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAACZZIYBkT_JY9FJZeU4dKd_VPKuaLfhVy4', 'authorUrn': 'urn:li:member:10052742', 'postedAtTimestamp': 1762454579318, 'postedAtISO': '2025-11-06T18:42:59.318Z', 'inputUrl': 'https://www.linkedin.com/in/roxannevarza/'}]


def get_reactions(linkedin_post_url="https://www.linkedin.com/posts/roxannevarza_just-gonna-put-this-here-via-challenges-activity-7392270291852488704-7ZTW?utm_source=combined_share_message&utm_medium=member_desktop&rcm=ACoAABxDsfABgJsLEUdI8vdnLv9UfDiShk5adv4") -> List[Reactor]:
	"""
	Get reactions from a LinkedIn post formatted as a list of Reactor BaseModel objects.

	Args:
		linkedin_post_url (str): LinkedIn post URL

	Returns:
		List[Reactor]: List of reactors with reaction_type, name, headline, profile_url, and profile_picture_url

	Example response format shown in comment on line 81
	"""
	payload = {
		"post_urls": [linkedin_post_url]
	}
	url = f"https://api.apify.com/v2/acts/apimaestro~linkedin-post-reactions/run-sync-get-dataset-items?token={token}"

	response = requests.post(url, json=payload)
	reactions_data = response.json()

	# Parse reactions and create Reactor objects
	reactors = []
	for reaction in reactions_data:
		reactor_info = reaction.get("reactor", {})
		profile_pictures = reactor_info.get("profile_pictures", {})

		reactor = Reactor(
			reaction_type=reaction.get("reaction_type", ""),
			name=reactor_info.get("name", ""),
			headline=reactor_info.get("headline", ""),
			profile_url=reactor_info.get("profile_url", ""),
			profile_picture_url=profile_pictures.get("medium", "")
		)
		reactors.append(reactor)

	return reactors
