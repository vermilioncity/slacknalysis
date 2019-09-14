# slacknalysis

Small project to analyze some Slack data with the Slacker API client.  Can compile statistics on questions such as:

- Who sends the most messages?
- Who sends the longest messages?
- Which messages generated the most replies and reactions?
- Who is the most likely to use a particular reaction?
- Which reactions does a person use most?

## Scopes

channels:history
channels:read
emoji:read
reactions:read
users:read

## Using slacknalysis

It's assumed you have a utils.py file in slacknalysis of the following structure:

```python
channels = {'channel1_name': 'channel1_id',
            'channel2_name': 'channel2_id',
            'channel3_name': 'channel3_id'
            }

oath = 'your_oath'
```

### Downloading data

slacknalysis allows you to optionally fetch data from Slack for a specified timeperiod (default is 6 months).
`python -m slackanalysis.slacknalysis --refresh-data --months 6`

In addition to downloading raw JSON, it will save a cleaned pandas-friendly version, *and* analyzed output (see below).  If you choose not to redownload data, but would like to reprocess the analysis (e.g., with different flags), you can simply omit the --refresh-data flag.

### Analyzing data

Assuming you have data on hand, slacknalysis will provide top-line analyses of all messages and reactions.  If you want analyses by user or reaction, you can pass in the users/reactions of interest with a flag.
`python -m slacknalysis.slacknalysis --users "moe.howard" "larry.fine" "curly.howard" --reactions "joy" "+1"`
