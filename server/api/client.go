package api

import (
	"grvpn/model"
	"grvpn/service"
	"net/http"
	"strings"

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

func DeleteClient(c *gin.Context) {
	err := service.DeleteClient(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"message": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"message": "Client deleted"})
}

func DownloadClientProfile(c *gin.Context) {
	profile := service.GetVpnProfile(c.Param("id"))
	if strings.Contains(profile, "not found") {
		c.JSON(http.StatusNotFound, gin.H{"message": "Profile not found"})
		return
	}
	c.Header("Content-Disposition", "attachment; filename=grvpn.ovpn")
	c.Data(http.StatusOK, "application/octet-stream", []byte(profile))
}
