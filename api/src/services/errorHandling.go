package services

import (
	"log"
	"net/http"
)

func LogError(args LogErrorArgs) bool {
	if args.Err != nil {
		if len(args.Message) > 0 {
			displayError(args.Message, args.W, args.Fatal)
		} else {
			displayError(args.Err.Error(), args.W, args.Fatal)
		}
		return true
	}
	return false
}

type LogErrorArgs struct {
	Err     error
	Message string ""
	Fatal   bool
	W       http.ResponseWriter
}

func displayError(message string, w http.ResponseWriter, fatal bool) {
	if fatal {
		if w != nil {
			http.Error(w, "500 Internal Server Error", http.StatusInternalServerError)
		}
		log.Fatal(message)
	} else {
		if w != nil {
			http.Error(w, "400 Bad Request", http.StatusBadRequest)
		}
		log.Print(message)
	}
}
