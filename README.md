# speedtest

tasks:

- an app to monitor your bandwidth using speedtest-cli tool (based on speedtest.net)
- based on Flask/Nginx + Postgres
- works as API - client who wants to be monitored has a script in his cron (like your router on openwrt)
- access through api key - each user can display his own graph/stats
- site task: deploy the app using docker

![graph](https://i.imgur.com/v43k2FC.png)
![manual](https://i.imgur.com/30xk5Qr.png)
![userpanel](https://i.imgur.com/QsG9nFN.png)
