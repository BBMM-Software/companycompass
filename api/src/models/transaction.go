package models

import "time"

type Transaction struct {
	ID           uint
	Amount       uint
	CreationDate time.Time
	IsIncome     bool
	Description  string
}
