package database

import (
	"database/sql"
	_ "github.com/mattn/go-sqlite3"
	"os"

	config "github.com/acheong08/ECGI/src/api/config"
	utils "github.com/acheong08/ECGI/src/api/utilities"
)

// Submission functions
type Submission struct {
	Database sql.DB
}
type Submissioner interface {
	Submit()
}

func Submit(author string, title string, abstract string, file_base64 string) bool {
	// Insert data into database
	statement, _ := self.Database.Prepare("INSERT INTO submissions(author, title, abstract, file) VALUES (?,?,?,?)")
	statement.Exec(author, title, abstract, file_base64)
	// return status
	return true
}

// Registration and login functions
type User struct {
  Database sql.DB
}
type Userer interface {
  Authenticate()
  Register()

}

func (self User) Authenticate(email string, password string) bool {
  // Hash password
  testHash := utils.GetSHA512(password)
  // Get realHash
	statement, _ := self.Database.Prepare("SELECT hash FROM authentication WHERE email = ?")
	var trueHash string
	statement.QueryRow(email).Scan(&trueHash)
	// Compare hashes
	if testHash == trueHash {
		return true
	} else {
		return false
	}
}

func (self User) Register(email string, password string) bool {
	// Hash password
	trueHash := utils.GetSHA512(password)
	// Insert hahs
	statement, _ := self.Database.Prepare("INSERT INTO authentication(email, hash) VALUES (?,?)")
	statement.Exec(email,trueHash)
	return true
}

// Administration functions
