# ToothTube

## Pre-requisites
`pip install --user --upgrade google-api-python-client`

`pip install --user --upgrade google-auth google-auth-oauthlib google-auth-httplib2`

You also need to enable the youtube API. From Google's documentation: 
- Use this [wizard](https://console.developers.google.com/start/api?id=youtube) to create or select a project in the Google Developers Console and automatically turn on the API. Click Continue, then Go to credentials.
- On the Add credentials to your project page, click the Cancel button.
- At the top of the page, select the OAuth consent screen tab. Select an Email address, enter a Product name if not already set, and click the Save button.
- Select the Credentials tab, click the Create credentials button and select OAuth client ID.
- Select the application type Other, enter the name "YouTube Data API Quickstart", and click the Create button.
- Click OK to dismiss the resulting dialog.
- Click the file_download (Download JSON) button to the right of the client ID.
- Move the downloaded file to your working directory and rename it client_secret.json.