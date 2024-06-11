package main

import (
	"encoding/json"
	"log"
	"math/rand"
	"net/http"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/emicklei/go-restful/v3"
)

type User struct {
	Account string 						`json:"account"`
	ID   	int 						`json:"id"`
	Name 	string 						`json:"name"`
}

type Item struct {
	ID    	int      					`json:"id"`
	Title 	string   					`json:"title"`
	Tags 	[]map[string]interface{} 	`json:"tags"`
	URL   	string   					`json:"url"`
	R18   	int      					`json:"r18"`
	User  	User 						`json:"user"`
}	

type CustomResponse struct {
	Data struct {
		ID       int     			 	`json:"id"`
		Title    string  			 	`json:"title"`
		Tags []map[string]interface{} 	`json:"tags"`
		URL      string   				`json:"url"`
		ProxyURL string   				`json:"proxy_url"`
		R18      int      				`json:"r18"`
		User     User 					`json:"user"`
	} `json:"data"`
	Index int `json:"index"`
}

func readItemsFromFile(filename string) ([]Item, error) {
	data, err := os.ReadFile(filename)
	if err != nil {
		return nil, err
	}

	var items []Item
	err = json.Unmarshal(data, &items)
	if err != nil {
		return nil, err
	}

	return items, nil
}

func getRandomItem(request *restful.Request, response *restful.Response) {
	items, err := readItemsFromFile("../metadata.json")
	if err != nil {
		response.WriteErrorString(http.StatusInternalServerError, err.Error())
		return
	}

	// Parameters
	r18Query := request.QueryParameter("r18")
	formatQuery := request.QueryParameter("format")
	r18, _ := strconv.Atoi(r18Query)
	if r18Query == "" {
		r18 = 0
	}

	// Filter R18
	var filteredItems []Item
	for _, item := range items {
		if item.R18 == r18 {
			filteredItems = append(filteredItems, item)
		}
	}

	// Select a random item
	rand.Seed(time.Now().UnixNano())
	index := rand.Intn(len(filteredItems))
	selectedItem := filteredItems[index]

	// Transform the URL
	proxyURL := selectedItem.URL
	proxyURL = replace(proxyURL, "i.pximg.net", "i.pixiv.re")

	// Create the custom response
	customResponse := CustomResponse{
		Index: index,
	}
	customResponse.Data.ID = selectedItem.ID
	customResponse.Data.Title = selectedItem.Title
	customResponse.Data.Tags = selectedItem.Tags
	customResponse.Data.URL = selectedItem.URL
	customResponse.Data.ProxyURL = proxyURL
	customResponse.Data.R18 = selectedItem.R18
	customResponse.Data.User = selectedItem.User

	if formatQuery == "image" {
		http.Redirect(response, request.Request, proxyURL, http.StatusFound)
	} else {
		response.WriteAsJson(customResponse)
	}
}

func replace(s, old, new string) string {
	return strings.Replace(s, old, new, -1)
}

func main() {
	ws := new(restful.WebService)
	ws.Route(ws.GET("/").To(getRandomItem))

	restful.Add(ws)
	log.Println("Starting server on :8000")
	log.Fatal(http.ListenAndServe(":8000", nil))
}