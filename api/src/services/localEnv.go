package services

import (
	"os"
)

func EnvironmentInit(){
	os.Setenv("dbUsername","adrian")
	os.Setenv("dbPassword","Access4Adrian")
	os.Setenv("dbUrl","moth5002.go.ro:3306")
	os.Setenv("dbName","HubA")
}
