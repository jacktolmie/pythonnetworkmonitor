# Basic Network Monitoring Program

This is just a basic monitoring program I wrote with A LOT of help from Gemini AI. 

It does the following:
* Ping hosts with an option for number of pings.
* Add hosts to monitor. Needs host name and IP, with optional description.
* In the Host Detail page, there is four options:
  * Change monitoring status.
  * Update ping frequency.
  * Delete specified number of pings.
  * Delete specified number of downtimes.

This was my first attempt at a full stack program. A lot of learning to get it done. Uses Django, JavaScript, Python, HTML and CSS.

It does come with Docker settings etc to get it running to test it inside a docker image. 
I will leave setting up docker and the setup to whomever is testing this.
To build it run `docker compose up --build`. That should be all you need to do.

<img title="Main Page" alt="Main Page" src="network_monitor/static/network_monitor/img/main.png">
<img title="Main Page" alt="Main Page" src="network_monitor/static/network_monitor/img/detailed.png">