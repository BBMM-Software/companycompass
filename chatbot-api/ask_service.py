from embeddings_utils import *
import pandas as pd
import numpy as np
from ast import literal_eval
from urllib.parse import urlparse

CONTEXT_LENGTH = 1800

class AskService:
  def __init__(company_name, company_site, client):
		self.company_name = company_name
		self.company_site = company_site
		self.client = client
  
		self.data = pd.read_csv('data/embeddings/' + urlparse(self.company_site).netloc + ".csv", index_col=0)
		self.data['embeddings'] = self.data['embeddings'].apply(literal_eval).apply(np.array)
		self.data.head()

	def create_context(
			question, max_len
	):
		"""
		Create a context for a question by finding the most similar context from the dataframe
		"""

		# Get the embeddings for the question
		q_embeddings = client.embeddings.create(input=question, model='text-embedding-ada-002').data[0].embedding

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

	def ask_question(
    question,
):
		"""
    Answer a question based on the most similar context from the dataframe texts
    """
    context = create_context(
        question,
        max_len=CONTEXT_LENGTH,
    )
    # If debug, print the raw model response
    message = [
        {"role": "system", "content": "Answer the question based on the context below\n\n"},
        {"role": "system", "content": "Context: " + context + "\n\n"},
        {"role": "user", "content": question + "\n"},
    ]

    try:
        # Create a chat completion using the question and context
        response = self.client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=message,
            temperature=0,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(e)
        return ""