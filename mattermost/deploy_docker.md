# Deploy Mattermost on Docker

https://docs.mattermost.com/deploy/server/deploy-containers.html


1. In a terminal window, clone the repository and enter the directory.

git clone https://github.com/mattermost/docker
cd docker
Create your .env file by copying and adjusting the env.example file.

cp env.example .env
Important

At a minimum, you must edit the DOMAIN value in the .env file to correspond to the domain for your Mattermost server.

We recommend configuring the Support Email via MM_SUPPORTSETTINGS_SUPPORTEMAIL. This is the email address your users will contact when they need help.

2. Create the required directories and set their permissions.

mkdir -p ./volumes/app/mattermost/{config,data,logs,plugins,client/plugins,bleve-indexes}
sudo chown -R 2000:2000 ./volumes/app/mattermost
(Optional) Configure TLS for NGINX. If you’re not using the included NGINX reverse proxy, you can skip this step.


