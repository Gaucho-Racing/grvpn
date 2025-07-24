package config

import (
	"os"
)

var Version = "1.0.3"
var Env = os.Getenv("ENV")
var Port = os.Getenv("PORT")

var DatabaseHost = os.Getenv("DATABASE_HOST")
var DatabasePort = os.Getenv("DATABASE_PORT")
var DatabaseUser = os.Getenv("DATABASE_USER")
var DatabasePassword = os.Getenv("DATABASE_PASSWORD")
var DatabaseName = os.Getenv("DATABASE_NAME")

var Sentinel = struct {
	Url          string
	JwksUrl      string
	ClientID     string
	ClientSecret string
	Token        string
	RedirectURI  string
}{
	Url:          os.Getenv("SENTINEL_URL"),
	JwksUrl:      os.Getenv("SENTINEL_JWKS_URL"),
	ClientID:     os.Getenv("SENTINEL_CLIENT_ID"),
	ClientSecret: os.Getenv("SENTINEL_CLIENT_SECRET"),
	Token:        os.Getenv("SENTINEL_TOKEN"),
	RedirectURI:  os.Getenv("SENTINEL_REDIRECT_URI"),
}
