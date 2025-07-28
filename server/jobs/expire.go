package jobs

import (
	"grvpn/utils"
	"strconv"
	"sync"
	"time"

	"grvpn/service"

	"github.com/robfig/cron/v3"
)

var expireSchedule = "* * * * *"

func RegisterExpireJob() {
	c := cron.New()
	entryID, err := c.AddFunc(expireSchedule, func() {
		utils.SugarLogger.Infoln("Starting expire job...")
		var wg sync.WaitGroup
		wg.Add(1)
		go func() {
			defer wg.Done()
			for _, client := range service.GetAllExpiredClients() {
				service.RevokeVpnProfile(client.ID)
				if time.Since(client.ExpiresAt).Hours() > 24 {
					service.DeleteClient(client.ID)
				}
			}
		}()
		wg.Wait()
		utils.SugarLogger.Infoln("Finished expire job!")
	})
	if err != nil {
		utils.SugarLogger.Errorln("Error registering CRON Job: " + err.Error())
		return
	}
	c.Start()
	utils.SugarLogger.Infoln("Registered CRON Job: " + strconv.Itoa(int(entryID)) + " scheduled with cron expression: " + expireSchedule)
}
