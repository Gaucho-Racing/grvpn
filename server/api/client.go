package api

import (
	"grvpn/model"
	"grvpn/service"
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
)

func GetAllClients(c *gin.Context) {
	Require(c, RequestUserHasRole(c, "d_admin"))

	clients := service.GetAllClients()
	c.JSON(http.StatusOK, clients)
}

func GetClientByID(c *gin.Context) {
	client := service.GetClientByID(c.Param("id"))
	if client.ID == "" {
		c.JSON(http.StatusNotFound, gin.H{"message": "Client not found"})
		return
	}

	Require(c, Any(
		RequestUserHasRole(c, "d_admin"),
		RequestUserHasID(c, client.UserID),
	))

	c.JSON(http.StatusOK, client)
}

func GetAllClientsByUser(c *gin.Context) {
	Require(c, Any(
		RequestUserHasRole(c, "d_admin"),
		RequestUserHasID(c, c.Param("userID")),
	))

	clients := service.GetAllClientsByUser(c.Param("userID"))
	c.JSON(http.StatusOK, clients)
}

func GetAllExpiredClientsByUser(c *gin.Context) {
	Require(c, Any(
		RequestUserHasRole(c, "d_admin"),
		RequestUserHasID(c, c.Param("userID")),
	))

	clients := service.GetAllExpiredClientsByUser(c.Param("userID"))
	c.JSON(http.StatusOK, clients)
}

func CreateClient(c *gin.Context) {
	var client model.VpnClient
	if err := c.ShouldBindJSON(&client); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"message": err.Error()})
		return
	}

	Require(c, Any(
		RequestUserHasRole(c, "d_admin"),
		RequestUserHasID(c, client.UserID),
	))

	client, err := service.CreateClient(client)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"message": err.Error()})
		return
	}
	c.JSON(http.StatusOK, client)
}

func DeleteClient(c *gin.Context) {
	client := service.GetClientByID(c.Param("id"))
	if client.ID == "" {
		c.JSON(http.StatusNotFound, gin.H{"message": "Client not found"})
		return
	}

	Require(c, Any(
		RequestUserHasRole(c, "d_admin"),
		RequestUserHasID(c, client.UserID),
	))

	err := service.DeleteClient(client.ID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"message": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"message": "Client deleted"})
}

func DownloadClientProfile(c *gin.Context) {
	client := service.GetClientByID(c.Param("id"))
	if client.ID == "" {
		c.JSON(http.StatusNotFound, gin.H{"message": "Client not found"})
		return
	}

	Require(c, Any(
		RequestUserHasRole(c, "d_admin"),
		RequestUserHasID(c, client.UserID),
	))

	profile := service.GetVpnProfile(client.ID)
	if strings.Contains(profile, "not found") {
		c.JSON(http.StatusNotFound, gin.H{"message": "Profile not found"})
		return
	}
	c.Header("Content-Disposition", "attachment; filename=grvpn.ovpn")
	c.Data(http.StatusOK, "application/octet-stream", []byte(profile))
}
