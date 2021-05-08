# Psuedo Code of Get_cam_videos

## Constants and Variables

- DIR

  - `HOME` or `PWD`
  - `UNRENAMED`
  - `RENAMED`

- `self.CAMERA_PLACE` = 'Chiayi' or 'Yunlin'
- `browser` = 'chrome'
- `os` = 'ubuntu'

  - read frome `sys`

- `DATE` = yesterday by default

## Configs

must be in .gitignore

- config.yaml
  - account
  - password

## Return a dict of time stamps of all events on `DATE`. -> dict(`events`)

1. Go to the camera page

   - Click camera
   - Remove the loading stream

2. Open the calendar

   - Confirm the calendar is completely loaded
   - 如果 `DATE` 不是在目前的月份的話，就按一下上個月；如果還沒找到，繼續按上個月。

3. Choose `DATE`

   1. Find `DATE`

      - If it is disabled: No video uploaded; return empty dict

   1. Click `DATE`

4. Find the motion events
   - Sort the list to be in chronological order
5. Return a dict:
   - TODO Refine this. 
   - Export this as yaml?
   ```
   events = {
      0: {
         time: datetime,
         status: {
            requested: None,
            generated: None,
            downloaded: None,
            renamed: None
         }
      },
      1: ...
   }
   ```

## Request videos from `events`

- DO Timeout

1. Go to the camera page

   1. Choose camera
   2. Remove the loading stream

2. for `event` in `events`:

   1. Read the `status`

      - `return None` when the `status` is in some conditions

   2. Request videos

      1. Select the `time` and request

         - Check if the selected results are expected
         - Request a 2 min video in case the `time` happens at the end of a 1 min video

      2. Read the message from the alert

         - Confirm the alert is present
         - Accept the alert

      3. `return` the new `status` depending on the message

## Download generated videos

- DO Timeout

1. Go to the video page

2. for `event` in `events`:

   1. Read the `status`

      - `return None` when the `status` is in some conditions
      - Create a .txt file when the `status` is `empty`

   2. Download videos of `events`

      1. Check if the `video is generated`

         - Make a set of `time` of all currently generated videos
           - TODO if there are no videos generated(the list is empty)
         - Check if the `time` is in the set

      2. Change the `status` to:
         1. `generated`
         2. `ungenerated`

   - Ignore when the video is ungenerated
   - The video starts at 00 second
   - HOTFIX check this twice
   - DEBUG

   - Find and download the video of the event

   - Remove the element(addSpotcam) that could block clicking

   - time.sleep(self.SLEEP_LONG) # sleep Downloading
   - HOTFIX dead loop: Chrome 沒有完成下載（檔名還有 Jhph.mp4.crdownload）

   ## Checking process

   - Wait until the video downloading is completed

   - Ignore if the downloading video does NOT exist
   - FIXME undownloaded

   - HOTFIX dead loop: Chrome 完成下載 BUT didn't leave the loop）

   ## Wait until the video is completely downloaded

   - End this checking process the video is completed

   - Rename and move the downloaded video

   ## Upload to ftp

   - HOTFIX 下載完的跟改好名字的沒正確對應

   - Make a downloading log

   ## Delete the video from the website

   1. Go to the video page

   - TODO Record what is deleted
   - Go to the video page
   - TODO solve the videos that unable to generate
