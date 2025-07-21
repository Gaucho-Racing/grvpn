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
}
