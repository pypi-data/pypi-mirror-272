# nowStudio App Upload - CLI

nowgg CLI is a command-line tool that enables you to upload your app builds to nowStudio.


## Prerequisites

+ Works with Python 3.8 and above.
+ App ID
    + Used to identify the App on nowStudio.
    + Your App ID can be found under the [App Details section](https://docs.now.gg/nowstudio/publish#app-details) of nowStudio.
+ Publisher token
    * Used to identify the publisher company.
    * Your Publisher token is available under the [Account Information](https://docs.now.gg/nowstudio/start-using-nowstudio#ac-info) section of nowStudio.

## Using nowgg CLI

Open any terminal on macOS or Windows.

### Install nowgg CLI tool
```bash
  pip install nowgg
```
### Initialize nowgg CLI
```bash
  nowgg init --token "<your_publisherToken_from_nowStudio>"
```

## Upload app using nowgg CLI to NowStudio

### Upload App

```bash
  nowgg upload --app_id <your_app_id> --file_path "/directory/sample.apk" --apk_version <apk_version> --version_code <app_version_code>
```

#### add to test track after upload
To create a draft on a test track, simply suffix the track id to the app_id, for example if your app_id is 1234, and you want to create draft on t1, provide app_id as 1234_t1

### Upload App to a Test Track and trigger deployment
providing the --deploy flag, will trigger a deployment on the test track. 

```bash
  nowgg upload --app_id <your_app_id> --file_path "/directory/sample.apk" --apk_version <apk_version> --version_code <app_version_code> --deploy
```


## For Help

```bash
  nowgg -h
  nowgg init -h
  nowgg upload -h
```  

**Note**: Your app will be uploaded to the App Library within nowStudio.

## Important Information

+ While running the nowgg command, If you receive a `‘command not recognized’` error, consider adding` <python directory>\<Scripts>  `to your PATH.
+ If you receive any  `'permission-related errors'`, you should run the commands as an Administrator.