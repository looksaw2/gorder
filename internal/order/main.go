package main

import (
	"fmt"
	"log"

	"github.com/looksaw/gorder-v2/common/config"
	"github.com/spf13/viper"
)

func init() {
	if err := config.NewViperConfig(); err != nil {
		log.Fatal("Failed to load config: ", err)
	}
}
func main() {
	fmt.Printf("Service_name: %v\n", viper.Get("order.service-name"))
}
