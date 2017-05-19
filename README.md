# XMPPExchange
Connect to StackExchange Chat with XMPP/Jabber.

![](https://s.ave.zone/517.PNG)

![](https://s.ave.zone/4ce.png)

## How to set it up
- Install sleekxmpp. `pip3 install sleekxmpp`
- Clone https://github.com/Manishearth/ChatExchange somewhere.
- cd into it and run make, it'll handle everything. (well, you need to install `python3-dev` first, `apt install python3-dev`)
- go back to `XMPPExchange` folder, rename `xmppexchange.ini.example` to `xmppexchange.ini`, fill in the required spots.
- Run it. `python3 xmppexchange.py`

## Features
- XMPP and Chat.StackExchange integration and bridging between those two (only one room per instance atm, though)
- Checking user's online status and not sending when offline (if not pinged)