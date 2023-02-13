# External tools

## Ngrok

A tunneling service like [ngrok](https://ngrok.com/), might help you with your work and to install your app on a Saleor Cloud developer instance - it exposes a port on your local machine to the world on an Ngrok url, via that url a Cloud Saleor instance can reach the application on your local environment.

``` mermaid
sequenceDiagram
  participant SAL as Saleor
  participant NGR as Ngrok
  participant LOC as Local

  LOC ->> NGR: Request URL / Setup tunnel
  NGR ->> LOC: Tunnel setup

  SAL ->> NGR: Request your.ngrok.url
  NGR ->> LOC: Request your designated port
  LOC ->> NGR: Response
  NGR ->> SAL: Response
```
