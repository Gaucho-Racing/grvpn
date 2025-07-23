package utils

import "grvpn/config"

func VerifyConfig() {
	if config.Env == "" {
		config.Env = "PROD"
		SugarLogger.Infof("ENV is not set, defaulting to %s", config.Env)
	}
	if config.Port == "" {
		config.Port = "9999"
		SugarLogger.Infof("PORT is not set, defaulting to %s", config.Port)
	}
	if config.DatabaseHost == "" {
		config.DatabaseHost = "localhost"
		SugarLogger.Infof("DATABASE_HOST is not set, defaulting to %s", config.DatabaseHost)
	}
	if config.DatabasePort == "" {
		config.DatabasePort = "5432"
		SugarLogger.Infof("DATABASE_PORT is not set, defaulting to %s", config.DatabasePort)
	}
	if config.DatabaseUser == "" {
		config.DatabaseUser = "postgres"
		SugarLogger.Infof("DATABASE_USER is not set, defaulting to %s", config.DatabaseUser)
	}
	if config.DatabasePassword == "" {
		config.DatabasePassword = "password"
		SugarLogger.Infof("DATABASE_PASSWORD is not set, defaulting to %s", config.DatabasePassword)
	}
}
