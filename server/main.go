package main

import (
	"grvpn/api"
	"grvpn/config"
	"grvpn/database"
	"grvpn/jobs"
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

	jobs.RegisterExpireJob()

	router := api.SetupRouter()
	api.InitializeRoutes(router)
	err := router.Run(":" + config.Port)
	if err != nil {
		utils.SugarLogger.Fatalln(err)
	}
}
