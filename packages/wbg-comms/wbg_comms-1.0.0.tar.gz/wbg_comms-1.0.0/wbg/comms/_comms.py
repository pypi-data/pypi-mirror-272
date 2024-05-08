from __future__ import annotations
import json
import shutil
import uuid
import typing
from collections.abc import (
    Iterable,
)
from dataclasses import (
    dataclass,
    asdict,
)

from pathlib import Path

from wbg.core import env as env_

from . import _paths, _email_accounts


@dataclass(kw_only=True, frozen=True)
class Payload:
    """PowerAutomate notification container."""

    email: str
    name: str
    message: str


@dataclass
class Attachment:
    name: str
    file_system_path: Path

    def __post_init__(self) -> None:
        self.id = uuid.uuid1()

    @property
    def hash_name(self) -> str:
        return f'{self.id}-{self.name}'


@dataclass(kw_only=True, frozen=True)
class EmailPayload(Payload):
    """PowerAutomate Email notification container."""

    email: str
    name: str
    subject: str
    message: str
    ccList: str = ''
    emailAccount: str = _email_accounts.ZZ_AUTOMATION


def teams_notify(payload: Payload, env: env_.Env) -> str:
    """Send MS Teams notification."""
    filename = _outfile(_paths.TEAMS_OUTDIR, payload, env)

    return _notify(payload, [], filename, env)


def email_notify(
    payload: EmailPayload, env: env_.Env, attachments: Iterable[Attachment] = tuple()
) -> str:
    """Send Outlook notification."""
    out = _paths.EMAIL_OUTDIR
    attachment_outdir = out.joinpath('attachments')

    for attachment in attachments:
        shutil.copy(
            attachment.file_system_path,
            attachment_outdir.joinpath(attachment.hash_name),
        )

    filename = _outfile(out, payload, env)

    return _notify(payload, attachments, filename, env)


def _outfile(outdir: Path, payload: Payload, env: env_.Env) -> Path:
    id_ = uuid.uuid1()
    return outdir.joinpath(env.value, f"{payload.name}-{id_}.json")


def _notify(
    payload: Payload, attachments: Iterable[Attachment], filename: Path, env: env_.Env
) -> str:
    json_dump = _make_json_dump(payload, attachments)

    with open(filename, "w") as f:
        json.dump(json_dump, f, indent=2)
    max_msg = 50
    if len(payload.message) < max_msg:
        msg = payload.message
    else:
        msg = f"{payload.message[: max_msg]}..."
    return f"({env}) Notified {payload.email}: {msg}"


def _make_json_dump(payload: Payload, attachments: Iterable[Attachment]) -> _JSONDump:
    json_dump = asdict(payload)

    json_dump['attachments'] = [
        _attachment_to_json(attachment) for attachment in attachments
    ]
    return json_dump


class _JSONDump(typing.TypedDict):
    email: str
    name: str
    subject: str
    message: str
    ccList: str
    emailAccount: str
    attachments: Iterable[_AttachmentSchema]


class _AttachmentSchema(typing.TypedDict):
    name: str
    filePath: str


def _attachment_to_json(attachment: Attachment) -> _AttachmentSchema:
    return {'name': attachment.name, 'filePath': attachment.hash_name}


def generic_email_notification(
    to: Iterable[str],
    subject: str,
    msg: str = '',
    cc: Iterable[str] = tuple(),
    env: env_.Env = env_.Env.TST,
) -> str:
    """Helper function to send emails."""
    payload = EmailPayload(
        email=';'.join(to), name='', message=msg, subject=subject, ccList=';'.join(cc)
    )
    return email_notify(payload, env)
