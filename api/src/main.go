package main

import (
	"github.com/MothBbmm/companycompass/src/routers"
	"github.com/MothBbmm/companycompass/src/services"
	"net/http"
)

func main() {
	services.Init()
	panic(http.ListenAndServe(":8080", http.HandlerFunc(routers.Serve)))
}
