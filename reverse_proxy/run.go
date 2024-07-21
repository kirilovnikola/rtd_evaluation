package main

import (
	"bytes"
    "fmt"
    "log"
    "net/http"   
    "net/url"
    "net/http/httputil"
	"runtime/debug"
)
func f(from string, jsonData []byte) {
var jsonbuff = bytes.NewBuffer(jsonData)
    	z, err := http.NewRequest("POST", from, jsonbuff )
		
		z.Header.Set("Content-Type", "application/json")
		client := http.Client{}
		resp, err := client.Do(z)
		jsonbuff.Reset()
		if err != nil {
		print(err)
		f(from,jsonData)
		return
		}
		fmt.Println("Response from target: "+resp.Status)
		_ = resp.Body.Close()
		return
}

type EHRReverseProxy struct {
    Proxy *httputil.ReverseProxy
}

func NewProxy(requestUrl string) (*EHRReverseProxy, error) {
    url, err := url.Parse(requestUrl)
    if err != nil {
        return nil, err
    }
    p := &EHRReverseProxy{httputil.NewSingleHostReverseProxy(url)}

    // Modify response
    p.Proxy.ModifyResponse = func(r *http.Response) error {
		method := r.Request.Method
		if method == "POST" || method == "PUT" || method == "DELETE"{
		status := r.Status
		if r.StatusCode == http.StatusOK || r.StatusCode == http.StatusCreated {
		location := r.Header.Get("Content-Location")
		message := "Sent real-time data for Request "+method+" with Response status: "+status+" location: "+location
		fmt.Println(message)

		var jsonData = []byte(`{
			"method": "`+r.Request.Method+`",
			"location": "`+r.Header.Get("Content-Location")+`"
		}`)

		go f("http://localhost:5001/",jsonData)
		}
		}
		debug.FreeOSMemory()
        return nil
    }
	debug.FreeOSMemory()
    return p, nil
}

func (p *EHRReverseProxy) ServeHTTP(rw http.ResponseWriter, req *http.Request) {
    p.Proxy.ServeHTTP(rw, req)
}

func main() {

    rev_proxy, err := NewProxy("http://localhost:8080")
    if err != nil {
        panic(err)
    }
    http.Handle("/", rev_proxy)
    log.Fatal(http.ListenAndServe(":5000", nil))
}