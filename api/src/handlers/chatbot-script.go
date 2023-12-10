package handlers

import(
	"os"
	"fmt"
	"net/http"
	"net/url"
	"github.com/MothBbmm/companycompass/src/services"
	"path"
	"strings"
	"strconv"
)
var API_ROUTE = "http://localhost:8080/"
var CHATBOT_API_ROUTE = "http://localhost:1280/scrape"

func GenerateChatbotScript(w http.ResponseWriter, r *http.Request) {
	content, err := os.ReadFile("static/main.js")
	if services.LogError(services.LogErrorArgs{Err: err, W: w}) {
		return
	}

	
	company_name := r.URL.Query().Get("company_name")
	company_website_url := r.URL.Query().Get("company_website_url")

	shouldCrawl := true
	should_crawl_query_param := r.URL.Query().Get("should_crawl")
	if should_crawl_query_param != ""{
		shouldCrawl, err = strconv.ParseBool(should_crawl_query_param)
		if services.LogError(services.LogErrorArgs{Err: err, W: w}) {
			shouldCrawl = true
		}
	}
	
	parsedUrl, err := url.Parse(company_website_url)
	if services.LogError(services.LogErrorArgs{Err: err, W: w}) {
		return
	}

	parts := strings.Split(parsedUrl.Hostname(), ".")
  domain := parts[len(parts)-2] + "." + parts[len(parts)-1]
	filePath := "static/"+domain+".js"
	
	company_name_pattern := "%%company_name%%"
	company_website_url_pattern := "%%company_website_url%%"

	contentString := string(content)
	contentString = strings.Replace(contentString, company_name_pattern, "'"+company_name+"'", -1)
	contentString = strings.Replace(contentString, company_website_url_pattern, "'"+company_website_url+"'", -1)

	f, err := os.Create(filePath)
	if services.LogError(services.LogErrorArgs{Err: err, W: w}) {
		return
	}
	defer f.Close()

	_, err = f.WriteString(contentString)
	if services.LogError(services.LogErrorArgs{Err: err, W: w}) {
		return
	}
	fmt.Printf(company_name)
	fmt.Fprintf(w,"<script src=\""+API_ROUTE+filePath+"></script>")

	if shouldCrawl{
		go callCrawler(company_name, company_website_url)
	}

}

func GetChatbotScript(w http.ResponseWriter, r *http.Request) {
	content, err := os.ReadFile("static/"+path.Base(r.URL.Path))
	if services.LogError(services.LogErrorArgs{Err: err, W: w}) {
		return
	}
	fmt.Fprintf(w, string(content))
}

func callCrawler(company_name string, company_website_url string){
	queryParams := url.Values{}
	queryParams.Add("company_name", company_name)
	queryParams.Add("company_website_url", company_website_url)

	_, err := http.Post(CHATBOT_API_ROUTE+"?"+queryParams.Encode(), "application/json", nil)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
}

