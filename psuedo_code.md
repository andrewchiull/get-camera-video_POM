# Psuedo Code of Get_cam_videos

## Set environment

- DIR
  - `HOME` or `PWD`
  - `UNRENAMED`
  - `RENAMED`

- `CAMERA_PLACE` = 'Chiayi' or 'Yunlin'
- `browser` = 'chrome'
- `os` = 'ubuntu'

  - read from `sys`

- `DATE` = yesterday by default

## Configs

- must be in .gitignore
- config.yaml
  - account
  - password

## Return a dict of time stamps of all events on `DATE`. -> dict(`events`)

1. Go to the camera page

   1. Click camera
   2. Remove the loading stream

2. Choose `DATE`

   1. Open the calendar

      1. Confirm the calendar is completely loaded
         - Click previous month if needed

   2. Choose `DATE`

      1. Find `DATE`

         - If `DATE` is disabled:
           - No video uploaded; return empty dict

      2. Click `DATE`

3. Find the motion events

   - Sort the list in chronological order

4. Return a dict of objects:

   - TODO Refine this.
   - Export this as yaml (or json)?

   ```
   events = {
      0: {
         time: datetime,

         requested: bool = False
         empty_once: bool = False
         empty_twice: bool = False

         generated: bool = False
         downloaded: bool = False
         renamed: bool = False
         uploaded: bool = False
         erased: bool = False
      },
      1: ...
   }
   ```

## Request videos from `events`

- TODO Timeout

1. Go to the camera page

   1. Choose camera
   2. Remove the loading stream

2. for `event` in `events`:

   1. Read the `status`

      - Skip this loop when the `status` is in some conditions

   2. Request videos

      1. Select the `time` and request

         - Check if the selected results are expected
         - Request a 2 min video in case the `time` happens at the end of a 1 min video

      2. Read the message from the alert

         1. Confirm the alert is present
         2. Accept the alert

      3. `return` the new `status` depending on the message

## Download generated videos

- TODO Timeout

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

      3. Ignore when the video is ungenerated

      - check ungenerated twice?

      4. Find and download the video of the event
         - Remove the element(addSpotcam) that could block clicking

   3. Checking the video downloading is completed

      - HOTFIX dead loop: Chrome 沒有完成下載（檔名還有 Jhph.mp4.crdownload）

      - Wait until the video downloading is completed

      - Ignore if the downloading video does NOT exist
      - FIXME undownloaded
      - HOTFIX dead loop: Chrome 完成下載 BUT didn't leave the loop）

   4. Rename and move the downloaded video

      - HOTFIX 下載完的跟改好名字的沒正確對應
      - Make a downloading log

   5. Upload to ftp

## Erase the renamed video from the website

1.  Go to the video page

- TODO Record what is deleted
- TODO solve the videos that unable to generate
