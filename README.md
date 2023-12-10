![](./miscellaneous/companycompasslogo.jpg)
# API
- Backend project that uses Golang
  - To start the api
    - ``go mod vendor`` for installing the dependencies
    - ``go run main.go`` 

# Structure
- PytonApi(question) -> Answer
  - (CompanyWebsite)-> Persist data
- UI(Company) -> ``<script src="golang"> </script>``
- Golang -> ``<script>fetch(pythonAPI, companyId)</script>``

# API Key - saved in env vars
VERIDION_MATCH_API_KEY
VERIDION_SEARCH_API_KEY
OPENAI_API_KEY