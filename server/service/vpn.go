package service

import (
	"grvpn/utils"
	"os/exec"
)

func GetVpnProfile(clientID string) string {
	cmd := exec.Command("sudo", "./openvpn-helper.sh", "view", clientID)
	output, err := cmd.CombinedOutput()
	if err != nil {
		utils.SugarLogger.Errorf("Error executing command: %v", err)
		return ""
	}
	return string(output)
}

func CreateVpnProfile(clientID string) string {
	cmd := exec.Command("sudo", "./openvpn-helper.sh", "add", clientID)
	output, err := cmd.CombinedOutput()
	if err != nil {
		utils.SugarLogger.Errorf("Error executing command: %v", err)
		return ""
	}
	return string(output)
}

func RevokeVpnProfile(clientID string) string {
	cmd := exec.Command("sudo", "./openvpn-helper.sh", "revoke", clientID)
	output, err := cmd.CombinedOutput()
	if err != nil {
		utils.SugarLogger.Errorf("Error executing command: %v", err)
		return ""
	}
	return string(output)
}
