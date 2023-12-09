package handlers

import (
	"fmt"
	// "github.com/MothBbmm/companycompass/src/services"
	"net/http"
	// "strconv"
)

func HomePost(w http.ResponseWriter, r *http.Request) {
	amountString := r.URL.Query().Get("amount")
	// amountValue, err := strconv.Atoi(amountString)
	// if services.LogError(services.LogErrorArgs{Err: err, W: w}) {
	// 	return
	// }else{
	// 	// TODO: LogResponse() HTTP.OK
	// }
	fmt.Printf(amountString)

}
func HomeGet(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w,"<p id=\"demo\"></p>")
	fmt.Fprintf(w,"<script>function test(){ navigator.clipboard.readText().then(text => {document.getElementById(\"demo\").innerHTML = text;})}</script>")
	fmt.Fprintf(w,"<button onclick=\"test()\">Paste & Submit</button>")
}
