import requests
import json
import os

# Search companies by name return large array
# For now used for testing
def search_company_data(company_name):
	url = 'https://data.veridion.com/search/v1/companies'
	headers = {
			'x-api-key': os.getenv("VERIDION_SEARCH_API_KEY"),
			'Content-type': 'application/json',
	}
	data = {
    'filters': [
        {
            'attribute': 'company_name',
            'relation': 'matches',
            'value': company_name,
        }
    ]
	}

	response = requests.post(url, headers=headers, data=json.dumps(data))
	if response.status_code == 200:
		return response.json()
	

def get_company_data(company_name, website):
	url = 'https://data.veridion.com/match/v4/companies'
	headers = {
			'x-api-key': os.getenv("VERIDION_MATCH_API_KEY"),
			'Content-type': 'application/json',
	}
	data = {
			'commercial_names': [company_name],
			'website': website,
	}

	response = requests.post(url, headers=headers, data=json.dumps(data))

	if response.status_code == 200:
		return response.json()


def describe_company(data):
    description = ""
    if 'company_name' in data and data['company_name']:
        description += f"The company, {data['company_name']},"
    if 'company_commercial_names' in data and data['company_commercial_names']:
        description += f" also known as {', '.join(data['company_commercial_names'])},"
    if 'company_legal_names' in data and data['company_legal_names']:
        description += f" is legally registered as {', '.join(data['company_legal_names'])}. "
    if all(key in data for key in ['main_city', 'main_region', 'main_country', 'main_street_number', 'main_street', 'main_postcode']):
        description += f"It is primarily located in {data['main_city']}, {data['main_region']}, {data['main_country']} at {data['main_street_number']} {data['main_street']}, {data['main_postcode']}. "
    if 'primary_phone' in data and data['primary_phone']:
        description += f"The company's main phone number is {data['primary_phone']}"
    if 'primary_email' in data and data['primary_email']:
        description += f" and the main email is {data['primary_email']}. "
    if 'website_url' in data and data['website_url']:
        description += f"The company's website is {data['website_url']}. "
    if 'main_industry' in data and data['main_industry']:
        description += f"The company's industry is {data['main_industry']},"
    if 'main_sector' in data and data['main_sector']:
        description += f" and it operates in the {data['main_sector']} sector. "
    if 'naics_2022' in data and data['naics_2022']:
        description += f"The company's NAICS code is {data['naics_2022']['primary']['code']}"
    if 'nace_rev2' in data and data['nace_rev2']:
        description += f" and the NACE code is {data['nace_rev2'][0]['code']}. "
    if 'year_founded' in data and data['year_founded']:
        description += f"The company was incorporated on {data['year_founded']}"
    if 'employee_count' in data and data['employee_count']:
        description += f" and has {data['employee_count']} employees. "
    if 'short_description' in data and data['short_description']:
        description += f"The company's short description is {data['short_description']}"
    if 'long_description' in data and data['long_description']:
        description += f" and the long description is {data['long_description']}. "
    if 'business_tags' in data and data['business_tags']:
        description += f"The company's business tags are {', '.join(data['business_tags'])}. "
    if 'main_business_category' in data and data['main_business_category']:
        description += f"The company's main business category is {data['main_business_category']}. "
    if 'sic' in data and data['sic']:
        description += f"The company's SIC code is {data['sic'][0]['code']}"
    if 'isic_v4' in data and data['isic_v4']:
        description += f" and the ISIC code is {data['isic_v4'][0]['code']}. "
    if 'technologies' in data and data['technologies']:
        description += f"The company's technologies are {', '.join(data['technologies'])}. "
    
    if 'locations' in data and len(data['locations']) > 1:
        description += "The company also has other locations: "
        for location in data['locations'][1:]:
            description += f"{location['city']}, {location['region']}, {location['country']}; "
    
    return description

print(describe_company(get_company_data("Apple Inc.", "apple.com")))