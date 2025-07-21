package api

import (
	"grvpn/config"
	"net/http"

	"github.com/gin-gonic/gin"
)

func Ping(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{"message": "grvpn server v" + config.Version + " is online!"})
}
