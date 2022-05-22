# Web development

## Deadlines

- [ ]  DDL 1 (June 10th): prototype completion
- [ ]  DDL 2 (June 22nd): Basic information & web pages
- [ ]  DDL 3 (June 25th): final completion

## Task list

- [ ]  Create flask web page handlers
    - [ ]  Homepage
        - [ ]  Basic info
        - [ ]  Deadlines
    - [ ]  Essay questions & submissions portal
    - [ ]  FAQ
        - [ ]  Terms and conditions
        - [ ]  Participation requirement
        - [ ]  Competition details
        - [ ]  Judging Criteria
- [ ]  Create Go API handlers
    - [ ]  Submissions portal
- [ ]  Write HTML, CSS, and JavaScript

## Basic plan

### Frameworks

Web Framework: Python Flask

API & database: Go

```go
// Native
import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

// Third party
import (
	"github.com/gorilla/mux"
)
```

Database: Local SQLite3 database

### Content

Markdown for FAQ

Use https://github.com/jekyll/jekyll to build static pages