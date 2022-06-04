package main

import (
	"database/sql"
	_ "github.com/mattn/go-sqlite3"
	"os"
	"fmt"
	"reflect"

	config "github.com/acheong08/ECGI/src/api/config"
	utils "github.com/acheong08/ECGI/src/api/utilities"
)

func main() {
	// Delete database files
	os.Remove(config.UserDB.Path)
	os.Remove(config.SubmissionDB.Path)
	os.Remove(config.AdminDB.Path)
	// Create new database
	userDB, _ := sql.Open("sqlite3", config.UserDB.Path)
	submissionDB, _ := sql.Open("sqlite3", config.SubmissionDB.Path)
	adminDB, _ := sql.Open("sqlite3", config.AdminDB.Path)
	// DEBUG: Database type
	fmt.Println(reflect.TypeOf(userDB))
	// Execute schema
	userDB.Exec(config.UserDB.Schema)
	submissionDB.Exec(config.SubmissionDB.Schema)
	adminDB.Exec(config.AdminDB.Schema)
	// Add admin data
	addAdminSQL := `INSERT INTO authentication(username, hash, authorization) VALUES (?,?,?)`
	statement, _ := adminDB.Prepare(addAdminSQL)
	statement.Exec(config.AdminDB.RootUser, utils.GetSHA512(config.AdminDB.RootPassword), 777)
	// Save databases
	userDB.Close()
	submissionDB.Close()
  adminDB.Close()
}
