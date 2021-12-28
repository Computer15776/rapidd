# RaPiDD

## ℹ About
RaPiDD is a lightweight, dynamic DNS (DDNS) inspired by https://github.com/tynick/PynamicDNS allowing easy connectivity to a device on an external network where no static external IP is assigned by an ISP. It uses AWS Route 53 in order to keep a record of the public IPv4 address originating from the network the device resides on. This application can either be ran manually or via an automated mechanism such as cron.

## ⚙ Configuration

> ⚠ RaPiDD assumes the hosted zone name is equal to the root domain

Only two arguments are required:
* `SUBDOMAIN` - The subdomain to assign the DNS `A` record to
* `DNS_NAME` - The base domain

A complete example is: ```$python3 rapidd.py rpi acmecorp.com```

In other words, if you want to access your device on `rpi.acmecorp.com` then you would assign `rpi` as the `SUBDOMAIN` arg and `acmecorp.com` as the `DNS_NAME` arg.

## 📜 Requirements
* Python3
    * boto3
    * requests
    * sys