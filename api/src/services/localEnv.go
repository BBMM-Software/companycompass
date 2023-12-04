package services

import (
	"os"
)

func EnvironmentInit(){
	os.Setenv("dbUsername","")
	os.Setenv("dbPassword","")
	os.Setenv("dbUrl","")
	os.Setenv("dbName","")
}
