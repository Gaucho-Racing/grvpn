package api

import (
	"grvpn/model"
	"grvpn/service"
	"net/http"

	"github.com/gin-gonic/gin"
)

func GetAllClients(c *gin.Context) {
	clients := service.GetAllClients()
	c.JSON(http.StatusOK, clients)
}

func GetClientByID(c *gin.Context) {
	client := service.GetClientByID(c.Param("id"))
	if client.ID == "" {
		c.JSON(http.StatusNotFound, gin.H{"message": "Client not found"})
		return
	}
	c.JSON(http.StatusOK, client)
}

func GetAllClientsByUser(c *gin.Context) {
	clients := service.GetAllClientsByUser(c.Param("userID"))
	c.JSON(http.StatusOK, clients)
}

func GetAllExpiredClientsByUser(c *gin.Context) {
	clients := service.GetAllExpiredClientsByUser(c.Param("userID"))
	c.JSON(http.StatusOK, clients)
}

func CreateClient(c *gin.Context) {
	var client model.VpnClient
	if err := c.ShouldBindJSON(&client); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"message": err.Error()})
		return
	}
	client, err := service.CreateClient(client)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"message": err.Error()})
		return
	}
	c.JSON(http.StatusOK, client)
}
