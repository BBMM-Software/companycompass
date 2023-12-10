import pandas as pd
import numpy as np
from ast import literal_eval
from urllib.parse import urlparse
from embeddings_utils import *
import service_parse_veridion

CONTEXT_LENGTH = 1800

class AskService:
	def __init__(self, company_name, company_site, client):
		self.company_name = company_name
		self.company_site = company_site
		self.client = client

		self.data = pd.read_csv('data/embeddings/' + urlparse(self.company_site).netloc + ".csv", index_col=0)
		self.data['embeddings'] = self.data['embeddings'].apply(literal_eval).apply(np.array)
		self.data.head()
		self.max_tokens = 500

	def create_context(
			self, question, max_len
	):
		"""
		Create a context for a question by finding the most similar context from the dataframe
		"""

		# Get the embeddings for the question
		q_embeddings = self.client.embeddings.create(input=question, model='text-embedding-ada-002').data[0].embedding

		# Get the distances from the embeddings
		self.data['distances'] = distances_from_embeddings(q_embeddings, self.data['embeddings'].values, distance_metric='cosine')

		returns = []
		cur_len = 0

		# Sort by distance and add the text to the context until the context is too long
		for i, row in self.data.sort_values('distances', ascending=True).iterrows():
				
				# Add the length of the text to the current length
				cur_len += row['n_tokens'] + 4
				
				# If the context is too long, break
				if cur_len > max_len:
						break
				
				# Else add it to the text that is being returned
				returns.append(row["text"])

		# Return the context
		return "\n\n###\n\n".join(returns)

	def ask_question(self, question):
		"""
		Answer a question based on the most similar context from the dataframe texts
		"""
		context = self.create_context(
			question,
			max_len=CONTEXT_LENGTH,
		)
		message = [
			{"role": "system", "content": "You will be answering questions exclusively about the following company: "+service_parse_veridion.get_hr_parsed(self.company_name, self.company_site)+". Act like a bot helping a user that visits the company website by providing information about the specified company. The information from the website is summarized using only the provided description and the following context. Limit your knowledge and do not answer questions outside this scope.\n\n"},
			{"role": "system", "content": "Context: " + context + "\n\n"},
			{"role": "user", "content": question + "\n"},
		]
		try:
			response = self.client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=message,
            temperature=0,
            max_tokens=self.max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
        )
			return response.choices[0].message.content.strip()
		except Exception as e:
			print(e)
			return ""