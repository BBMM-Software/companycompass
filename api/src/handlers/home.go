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

	
}
