package config

// Configurations for database
type Superdb struct{
	Path   string
	Schema string
}
type userDB struct {
	Superdb
}
type submissionDB struct {
	Superdb
}
type adminDB struct {
	Superdb
  RootUser string
  RootPassword string
}

var UserDB userDB
var SubmissionDB submissionDB
var AdminDB adminDB

func init() {
  // Create objects

	// Users
	UserDB.Path = "data/users.db"
	UserDB.Schema = `
  CREATE TABLE IF NOT EXISTS authentication (
    id INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    hash TEXT NOT NULL
  );
  `
	// Submissions
	SubmissionDB.Path = "data/submissions.db"
  SubmissionDB.Schema = `
  CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT,
    author INTEGER NOT NULL,
    title TEXT NOT NULL,
    abstract TEXT NOT NULL,
    file BLOB NOT NULL
  );
  `
	// Admin
	AdminDB.Path = "data/admins.db"
  AdminDB.Schema = `
  CREATE TABLE IF NOT EXISTS authentication (
    id INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    hash TEXT NOT NULL,
    authorization INTEGER NOT NULL
  );
  `
  AdminDB.RootUser = "root"
  AdminDB.RootPassword = "toor"
}
