###### self.chosen_camera = 'BIME-ChiaYi'
###### self.chosen_browser = 'firefox'
###### self.chosen_os = 'ubuntu'
###### TEST change today to a given date
###### self.today = self.today.replace(month=4, day=1) b
###### Create a "unrenamed" folder to keep the downloaded videos.
###### Create a folder to keep the renamed videos.


## Get the dict of time stamps of all alerts on yesterday.

### Go to the camera page.
###### Choose camera.
###### Remove the loading stream

### Open the calendar.
###### Confirm the calendar is completely loaded.
###### 如果 yesterday 不是在目前的月份的話，就按一下上個月；如果還沒找到，繼續按上個月。
###### HOTFIX

### Choose yesterday.
###### Find yesterday; if it is disabled, quit.

###### Click yesterday.

### Find the event alerts.

### Build a dict (self.alert) with time stamps and default status.

###### TEST use only some videos
###### alerts_list = alerts_list[3:7]
##  Generate videos of the given time stamps.
### Reload the camera page.
###### Choose camera.
###### Remove the loading stream

### Generate videos from self.alerts.

### IGNORE this loop when the status is NOT in these conditions.

### Select the time of the event.

###### DONE Check if the selected results are correct.

###### Generate a 2 min video in case the alert happens in the end of 1 min video.

###### time.sleep(self.SLEEP_SHORT) # sleep 按太快會 empty

### Read the message from the alert-box; accept the alert-box.
###### Confirm the alert box is present

### Record the new status depending on the message.
##  Download videos, and then delete them.
### Generate videos from self.alerts.
###### DO Timeout
### IGNORE this loop when the status IS in these conditions.
###### Create a .txt file when the video is empty.

## Check if the video is generated.
### Go to the video page.

###### Make a list of time stamps of all generated_videos.

###### Ignore if there are no videos generated video (the list is empty).

###### Ignore when the video is ungenerated.
###### The video starts at 00 second.
###### HOTFIX check this twice
###### DEBUG

###### Find and download the video of the alert.

###### Remove the element(addSpotcam) that could block clicking

###### Firefox: Browser plays automatically, so clicking 'play' is not needed.

## Firefox: There will be a alert after clickng download.
###### if self.chosen_browser == 'firefox':
######     self.wait_and_accept_alert()
######     downloading = self.find('//*[@id="loadingimg_r"]')
######     # Firefox: There will be a downloading image after accepting alert.
######     while True:
######         if 'none' in downloading.get_attribute("style"):
######             break

###### TEST Unable to click due to display
###### self.xpath['closeWindow'] = f'//*[contains(@class,"fancybox-close")]'
###### self.click(self.xpath['closeWindow'])

###### time.sleep(self.SLEEP_LONG) # sleep Downloading
###### HOTFIX dead loop: Chrome 沒有完成下載（檔名還有Jhph.mp4.crdownload）
## Checking process
###### Wait until the video downloading is completed.

###### Ignore if the downloading video does NOT exist.
###### FIXME undownloaded

###### HOTFIX dead loop: Chrome 完成下載 BUT didn't leave the loop）
###### # Wait until the video is completely downloaded.
###### while any('crdownload' in f for f in files):
######     time.sleep(self.SLEEP_SHORT) # sleep Downloading
###### End this checking process the video is completed.

###### Rename and move the downloaded video.

## Upload to ftp                  


###### HOTFIX 下載完的跟改好名字的沒正確對應

###### Make a downloading log.

### Go to the video page.
###### Delete the video from the website.
###### TODO Record what is deleted.
###### Go to the video page.

###### logging.info(
######     f'Wait {self.SLEEP_LONG} secs for requesting progress...')
###### time.sleep(self.SLEEP_LONG) # sleep
###### TODO solve the videos that unable to generate.


###### self.delete_all()