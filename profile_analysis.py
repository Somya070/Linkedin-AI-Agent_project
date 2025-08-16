import requests

def fetch_profile(access_token: str) -> dict:
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Restli-Protocol-Version': '2.0.0'
    }

    # 1️⃣ Basic Profile
    profile_url = "https://api.linkedin.com/v2/me"
    profile_data = requests.get(profile_url, headers=headers).json()

    # 2️⃣ Skills
    skills_url = "https://api.linkedin.com/v2/skills"
    skills_data = requests.get(skills_url, headers=headers).json()

    # Optional: Fetch positions (experience)
    positions_url = "https://api.linkedin.com/v2/positions"
    positions_data = requests.get(positions_url, headers=headers).json()

    return {
        "profile": profile_data,
        "skills": skills_data,
        "positions": positions_data
    }

def analyze_profile(profile_json: dict) -> dict:
    profile = profile_json.get("profile", {})
    skills_data = profile_json.get("skills", {})
    positions_data = profile_json.get("positions", {})

    structured_profile = {
        "name": profile.get("localizedFirstName", "") + " " + profile.get("localizedLastName", ""),
        "headline": profile.get("headline", {}).get("localized", {}).get("en_US", ""),
        "location": profile.get("locationName", ""),
        "industry": profile.get("industryName", ""),
        "skills": [skill.get("name") for skill in skills_data.get("elements", [])],
        "experience": [
            {
                "role": pos.get("title", ""),
                "company": pos.get("companyName", ""),
                "duration": f"{pos.get('startDate', {}).get('year','')} - {pos.get('endDate', {}).get('year','Present')}"
            }
            for pos in positions_data.get("elements", [])
        ]
    }

    return structured_profile
