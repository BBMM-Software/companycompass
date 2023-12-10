package main

import (
	"github.com/MothBbmm/companycompass/src/routers"
	"net/http"
)

func main() {
	panic(http.ListenAndServe(":8080", http.HandlerFunc(routers.Serve)))
}
