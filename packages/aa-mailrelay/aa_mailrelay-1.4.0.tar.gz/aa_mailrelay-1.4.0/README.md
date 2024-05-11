# Mailrelay

An app for relaying Eve mails to Discord.

[![release](https://img.shields.io/pypi/v/aa-mailrelay?label=release)](https://pypi.org/project/aa-mailrelay/)
[![python](https://img.shields.io/pypi/pyversions/aa-mailrelay)](https://pypi.org/project/aa-mailrelay/)
[![django](https://img.shields.io/pypi/djversions/aa-mailrelay?label=django)](https://pypi.org/project/aa-mailrelay/)
[![pipeline](https://gitlab.com/ErikKalkoken/aa-mailrelay/badges/master/pipeline.svg)](https://gitlab.com/ErikKalkoken/aa-mailrelay/-/pipelines)
[![codecov](https://codecov.io/gl/ErikKalkoken/aa-mailrelay/branch/master/graph/badge.svg?token=ZTGEX30YIN)](https://codecov.io/gl/ErikKalkoken/aa-mailrelay)
[![license](https://img.shields.io/badge/license-MIT-green)](https://gitlab.com/ErikKalkoken/aa-mailrelay/-/blob/master/LICENSE)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![chat](https://img.shields.io/discord/790364535294132234)](https://discord.gg/mevDXbxp4R)

## Contents

- [Overview](#overview)
- [Installation](#installation)
- [Settings](#settings)
- [Change Log](CHANGELOG.md)

## Overview

This app can automatically forwards eve mails to Discord channels. This can e.g. be useful to include people in all hands communications, who do not check their eve mails that often, but still can be reached via Discord.

You can choose to just forward corporation or alliance mails only or all mails that a character receives.

This app is an add-on to [Member Audit](https://gitlab.com/ErikKalkoken/aa-memberaudit) and requires you to have Member Audit installed and running. You can choose to forward mails from any character that is registered on Member Audit.

## Installation

### Step 1 - Check preconditions

Please make sure you have the following applications installed and running before attempting to install the Mail Relay app:

- [Alliance Auth](https://allianceauth.readthedocs.io/en/latest/installation/auth/allianceauth/)
- [AA Discord service](https://allianceauth.readthedocs.io/en/v2.9.3/features/services/discord.html)
- [Member Audit](https://gitlab.com/ErikKalkoken/aa-memberaudit)
- [Discord Proxy](https://gitlab.com/ErikKalkoken/discordproxy)

### Step 2 - Install app

Make sure you are in the virtual environment (venv) of your Alliance Auth installation. Then install the newest release from PyPI:

```bash
pip install aa-mailrelay
```

### Step 3 - Configure settings

Configure your Auth settings (`local.py`) as follows:

- Add `'mailrelay'` to `INSTALLED_APPS`
- Add below lines to your settings file:

```python
CELERYBEAT_SCHEDULE['mailrelay_forward_new_mails'] = {
    'task': 'mailrelay.tasks.forward_new_mails',
    'schedule': crontab(minute='*/5'),
}
```

- Optional: Add additional settings if you want to change any defaults. See [Settings](#settings) for the full list.

### Step 4 - Finalize installation

Run migrations & copy static files

```bash
python manage.py migrate
python manage.py collectstatic
```

Restart your supervisor services for Auth

...

### Step 5 - Setup mail relays

To setup your first mail relay go to the admin site / Mail Relay / RelayConfig.

Update the known Discord channels by clicking the button: "UPDATE DISCORD CHANNELS".

Click on "ADD RELAY CONFIG" to create your first mail relay configuration.

## Settings

Here is a list of available settings for this app. They can be configured by adding them to your AA settings file (`local.py`).

Note that all settings are optional and the app will use the documented default settings if they are not used.

Name|Description|Default
--|--|--
`DISCORDPROXY_HOST`|Port used to communicate with Discord Proxy.|`localhost`
`DISCORDPROXY_PORT`|Host used to communicate with Discord Proxy.|`50051`
`MAILRELAY_DISCORDPROXY_TIMEOUT`|Timeout for sending request to DISCORDPROXY in seconds.|`30`
`MAILRELAY_OLDEST_MAIL_HOURS`|Oldest mail to be forwarded in hours. Set to 0 to disable.|`2`
`MAILRELAY_RELAY_GRACE_MINUTES`|Max time in minutes since last successful relay before service is reported as down.|`30`
