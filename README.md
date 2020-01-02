This bot was written using the Discord.py API

PyBot scans incoming messages and pushes them into appropriate text channels based on whether they contain
- Text
- Images
- Links

If the wrong type of message is sent to a channel, PyBot will delete the message from the incorrect channel and forward it
to the appropriate channel. PyBot will also send a useful message which mentions the original sender.
