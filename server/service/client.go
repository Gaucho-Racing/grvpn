package service

import (
	"errors"
	"grvpn/database"
	"grvpn/model"
	"grvpn/utils"
	"strings"
	"time"

	"github.com/google/uuid"
)

func GetAllClients() []model.VpnClient {
	var clients []model.VpnClient
	result := database.DB.Find(&clients)
	if result.Error != nil {
		utils.SugarLogger.Errorf("Error getting all clients: %v", result.Error)
		return []model.VpnClient{}
	}
	return clients
}

func GetAllExpiredClients() []model.VpnClient {
	var clients []model.VpnClient
	result := database.DB.Find(&clients, "expires_at < NOW()")
	if result.Error != nil {
		utils.SugarLogger.Errorf("Error getting all expired clients: %v", result.Error)
		return []model.VpnClient{}
	}
	return clients
}

func GetClientByID(id string) model.VpnClient {
	var client model.VpnClient
	result := database.DB.First(&client, "id = ?", id)
	if result.Error != nil {
		utils.SugarLogger.Errorf("Error getting client by ID: %v", result.Error)
		return model.VpnClient{}
	}
	return client
}

func GetAllClientsByUser(userID string) []model.VpnClient {
	var clients []model.VpnClient
	result := database.DB.Find(&clients, "user_id = ? AND expires_at >= NOW()", userID)
	if result.Error != nil {
		utils.SugarLogger.Errorf("Error getting all clients by user: %v", result.Error)
		return []model.VpnClient{}
	}
	return clients
}

func GetAllExpiredClientsByUser(userID string) []model.VpnClient {
	var clients []model.VpnClient
	result := database.DB.Find(&clients, "user_id = ? AND expires_at < NOW()", userID)
	if result.Error != nil {
		utils.SugarLogger.Errorf("Error getting all expired clients by user: %v", result.Error)
		return []model.VpnClient{}
	}
	return clients
}

func CreateClient(client model.VpnClient) (model.VpnClient, error) {
	if client.ID == "" {
		client.ID = uuid.New().String()
		client.ExpiresAt = time.Now().Add(time.Hour * 8)
	}

	if database.DB.Where("id = ?", client.ID).Updates(&client).RowsAffected == 0 {
		// Create VPN profile
		output := CreateVpnProfile(client.ID)
		output2 := GetVpnProfile(client.ID)
		if strings.Contains(output2, "not found") {
			utils.SugarLogger.Errorf("Error creating VPN profile: %v", output)
			return model.VpnClient{}, errors.New("error creating VPN profile: " + output)
		}
		utils.SugarLogger.Infof("VPN profile created: %v", output2)
		client.ProfileText = output2
		client.ProfileLocation = "/home/ubuntu/" + client.ID + ".ovpn"

		utils.SugarLogger.Infof("New client created with id: %s", client.ID)
		result := database.DB.Create(&client)
		if result.Error != nil {
			utils.SugarLogger.Errorf("Error creating client: %v", result.Error)
			return model.VpnClient{}, result.Error
		}

		return client, nil
	} else {
		utils.SugarLogger.Infof("Client id: %s has been updated", client.ID)
	}
	return client, nil
}

func DeleteClient(id string) error {
	result := database.DB.Delete(&model.VpnClient{}, "id = ?", id)
	if result.Error != nil {
		utils.SugarLogger.Errorf("Error deleting client: %v", result.Error)
		return result.Error
	}
	RevokeVpnProfile(id)
	return nil
}

func DeleteAllExpiredClients() {
	deletedCount := 0
	clients := GetAllExpiredClients()
	for _, client := range clients {
		err := DeleteClient(client.ID)
		if err != nil {
			utils.SugarLogger.Errorf("Error deleting expired client: %v", err)
		} else {
			deletedCount++
		}
	}
	utils.SugarLogger.Infof("Deleted %d expired clients", deletedCount)
}
