package hello

import (
    "fmt"
    "net/http"
)

func init() {
    http.HandleFunc("/", hello)
}

func hello(w http.ResponseWriter, r *http.Request) {

    form := `<form action="http://www.google.com/search">
      <input name="q">
      <input type="submit">
    </form>`

    fmt.Fprintf(w, form)
}
