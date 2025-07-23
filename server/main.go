package main

import (
	"grvpn/config"
	"grvpn/database"
	"grvpn/model"
	"grvpn/service"
	"grvpn/utils"
)

func main() {
	config.PrintStartupBanner()
	utils.InitializeLogger()
	utils.VerifyConfig()
	defer utils.Logger.Sync()

	database.InitializeDB()
	service.InitializeKeys()
	service.PingSentinel()

	service.CreateClient(model.VpnClient{})

	// router := api.SetupRouter()
	// api.InitializeRoutes(router)
	// err := router.Run(":" + config.Port)
	// if err != nil {
	// 	utils.SugarLogger.Fatalln(err)
	// }
}
