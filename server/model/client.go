package model

import "time"

type VpnClient struct {
	ID              string    `json:"id" gorm:"primaryKey"`
	UserID          string    `json:"user_id"`
	ProfileText     string    `json:"profile_text"`
	ProfileLocation string    `json:"profile_location"`
	ExpiresAt       time.Time `json:"expires_at"`
	CreatedAt       time.Time `json:"created_at" gorm:"autoCreateTime"`
}
