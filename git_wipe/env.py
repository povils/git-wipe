import os

# Github access token used for git-wipe cli tool
GIT_WIPE_TOKEN = os.environ.get('GIT_WIPE_TOKEN')

# Github requester timeout in seconds
GIT_WIPE_TIMEOUT = os.environ.get('GIT_WIPE_TIMEOUT')
if GIT_WIPE_TIMEOUT is None:
    GIT_WIPE_TIMEOUT = 30
else:
    GIT_WIPE_TIMEOUT = int(GIT_WIPE_TOKEN)
