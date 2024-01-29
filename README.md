# template-python-project

## To Deploy
This template requires a Google Service Account and project:

```bash
SERVICE_NAME=%%{{ModuleName.lowerCase}}%%
ENV=dev
PROJECT=inquest-$SERVICE_NAME-$ENV
SERV_ACCNT_NAME="cassius-service-account"
DEV_INGRESS_IP=127.0.0.1  # change me
DNS_ZONE_NAME='inquest-devops'  # change me
gcloud projects create $PROJECT

gcloud beta iam service-accounts create $SERV_ACCNT_NAME \
    --display-name "Generated service account for Cassius" \
    --project $PROJECT
    
gcloud projects add-iam-policy-binding $PROJECT \
  --member serviceAccount:$SERV_ACCNT_NAME@$PROJECT.iam.gserviceaccount.com \
  --role roles/editor
    
gcloud iam service-accounts keys create ~/dev-key.json \
  --iam-account $SERV_ACCNT_NAME@$PROJECT.iam.gserviceaccount.com \
  --project $PROJECT

ENV=prod
PROJECT=inquest-$SERVICE_NAME-$ENV
PROD_INGRESS_IP=127.0.0.1  #change me
DNS_ZONE_NAME='inquest-devops'  #change me for PROD
gcloud projects create $PROJECT

gcloud beta iam service-accounts create $SERV_ACCNT_NAME \
    --display-name "Generated service account for Cassius" \
    --project $PROJECT
    
gcloud projects add-iam-policy-binding $PROJECT \
  --member serviceAccount:$SERV_ACCNT_NAME@$PROJECT.iam.gserviceaccount.com \
  --role roles/editor
    
gcloud iam service-accounts keys create ~/prod-key.json \
  --iam-account $SERV_ACCNT_NAME@$PROJECT.iam.gserviceaccount.com \
  --project $PROJECT
 
```

Note the location of the key (for me it is ~/key.json)

```bash
cassius secret create --secretName %%{{ModuleName.lowerCase}}%%-dev-gcloud-credentials --file ~/dev-key.json
cassius secret create --secretName %%{{ModuleName.lowerCase}}%%-prod-gcloud-credentials --file ~/prod-key.json

```

## Setup Datastore (if service needs a DB)

Open the following url in a browser
```
echo https://console.cloud.google.com/datastore/setup?project=$PROJECT
```

The enable the datastore API

```bash
gcloud services enable datastore.googleapis.com --project $PROJECT
```

## Setup Authentication and Authorization for new service

### (optional) create the service account.
```bash
mercury client create --clientId %%{{ModuleName.lowerCase}}%%-dev-svc --grant client_credentials --path http://rabbit-dev.inquestdevops.com/auth/merc/complete
mercury client create --clientId %%{{ModuleName.lowerCase}}%%-dev-svc --grant client_credentials --path http://rabbit-dev.inquestdevops.com/auth/merc/complete
```
**Note:** Take note of the generated service account secret

```bash
cassius secret create --secretName %%{{ModuleName.lowerCase}}%%-dev-service-account-secret --strContent <string from above>
cassius secret create --secretName %%{{ModuleName.lowerCase}}%%-dev-service-account-secret --strContent <string from above>

cassius secret create --secretName %%{{ModuleName.lowerCase}}%%-dev-rabbit-admin-token --strContent insecure   #dev admin tokens are not secure
cassius secret create --secretName %%{{ModuleName.lowerCase}}%%-prod-rabbit-admin-token --strContent <secure password>
```

### Create a Deployment Bundle for Cassius to Track images

```
cassius deployment-bundle create --name %%{{ModuleName.lowerCase}}%%-dev --type image
```


### grant permissions needed by your service:

**Eg**: (the following is not actually needed to run a cardinal service)

```
cardsharp policy create --name "%%{{ModuleName.lowerCase}}%%-integ-testing-perms-policy" \
--description "A policy granting the integ testing service account access to all APIs and resources for this service" \
--permission "%%{{ModuleName}}%%.*" \
--resource "*" \
--account "%%{{ModuleName.lowerCase}}%%-dev-svc"

```

Finally, you may want to register a user account for testing (not required):

```
mercury account register --display-name TestUser --email test@inquestdevops.com --fname Test --lname User --password insecure
```
