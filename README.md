# API
- Backend project that uses Golang
  - Dependencies
    - GORM and MySql driver
  - To start the api
    - ``go mod vendor`` for installing the dependencies
    - ``go run main.go`` 

# Client
- React
  - Dependencies
    - React-Router-DOM
    - Zustand
    - MUI
    - Sass
    - Axios

# ML-Approve-Events
- Python Tensorflow model to predict if a submitted event is real or not

# Structure
- PytonApi(question) -> Answer
  - (CompanyWebsite)-> Populate DB
- UI(Company) -> ``<script src="golang"> </script>``
- Golang -> ``<script>fetch(pythonAPI, companyId)</script>``

# Db
- Table CompanyBot
  - company_id - string
  - embedding - blob
  - sraped - blob

# Chatbot-API
- data/embeddings/
  - soleadify_id.csv
- data/scraped/
  - soleadify_id.csv

# API Key - saved in env vars
VERIDION_MATCH_API_KEY
VERIDION_SEARCH_API_KEY
OPENAI_API_KEY