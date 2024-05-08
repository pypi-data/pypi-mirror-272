from wbg.sharepoint import paths

_OUTDIR = paths.Paths.PROJS.value
EMAIL_OUTDIR = _OUTDIR.joinpath('email-notifications-attachment')
TEAMS_OUTDIR = _OUTDIR.joinpath('teams-notifications')
