package service

import (
	"grvpn/database"
	"grvpn/model"
	"grvpn/utils"
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
	result := database.DB.Find(&clients, "user_id = ?", userID)
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
		client.ExpiresAt = time.Now().Add(time.Hour * 24)
	}

	if database.DB.Where("id = ?", client.ID).Updates(&client).RowsAffected == 0 {
		utils.SugarLogger.Infof("New client created with id: %s", client.ID)
		result := database.DB.Create(&client)
		if result.Error != nil {
			utils.SugarLogger.Errorf("Error creating client: %v", result.Error)
			return model.VpnClient{}, result.Error
		}
		// Create VPN profile
		output := CreateVpnProfile(client.ID)
		println(output)

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
	return nil
}

func DeleteAllExpiredClients() error {
	result := database.DB.Delete(&model.VpnClient{}, "expires_at < NOW()")
	if result.Error != nil {
		utils.SugarLogger.Errorf("Error deleting all expired clients: %v", result.Error)
		return result.Error
	}
	return nil
}
