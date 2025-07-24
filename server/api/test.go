package api

import (
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
)

func TestConnection(c *gin.Context) {
	if c.ClientIP() == "35.162.142.32" || strings.Contains(c.ClientIP(), "10.8.0") {
		c.JSON(http.StatusOK, gin.H{
			"connected": true,
			"ip":        c.ClientIP(),
		})
	} else {
		c.JSON(http.StatusUnauthorized, gin.H{
			"connected": false,
			"ip":        c.ClientIP(),
		})
	}
}
