# slacknalysis
Small project to analyze some Slack data with the Slacker API client.  Can compile statistics on questions such as:
- Who sends the most messages?
- Who sends the longest messages?
- Which messages generated the most replies and reactions?
- Who is the most likely to use a particular reaction?
- Which reactions does a person use most?

# Scopes
channels:history
channels:read
emoji:read
reactions:read
users:read

# Using slacknalysis
It's assumed you have a utils.py file in slacknalysis of the following structure:
```
channels = {'channel1_name': 'channel1_id',
            'channel2_name': 'channel2_id',
            'channel3_name': 'channel3_id'
            }

oath = 'your_oath'
```

download.py will download and store JSONs for as many months of messages as you specify.