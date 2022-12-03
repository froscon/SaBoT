from contextlib import contextmanager
from enum import Enum
from pathlib import Path
from typing import Optional, List, Dict, Union

# This module is intended to encapsulate our needs of RT functionality
# We will will if with python-rt for the moment being. This will make
# this whole project be (together) licensed unter the terms of the GPLv3
# Even though the SaBoT code itself is licensed unter the terms of the MIT
# license.
# If this is problematic to you, we encourage to just exchange the implementation
# here.

from django.conf import settings
import rt
from requests.auth import HTTPBasicAuth


class TicketStatus(Enum):
    NEW = "new"
    OPEN = "open"
    RESOLVED = "resolved"
    STALLED = "stalled"


class Attachment:
    def __init__(self, name: str, location: Path):
        self._name = name
        self._location = location

    @property
    def name(self):
        return self._name

    @property
    def binary_file(self):
        return self._location.open("rb")


@contextmanager
def attachment_files(attachments):
    list = []
    try:
        list = [(attachment.name, attachment.binary_file) for attachment in attachments]
        yield list
    finally:
        for (_, binary_file) in list:
            binary_file.close()


class SabotRtException(Exception):
    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return self._msg


class SabotRtWrapper:
    def __init__(self):
        self._rt = rt.Rt(
            settings.RT_URL,
            http_auth=HTTPBasicAuth(settings.RT_USER, settings.RT_PASSWORD),
        )
        if not self._rt.login():
            raise SabotRtException("Unable to login to RT. Check credentials")

    def create_ticket(
        self,
        queue: str,
        owner: str,
        subject: str,
        requestor: str,
        text: str,
        status: Optional[TicketStatus] = None,
        attachments: Optional[List[Attachment]] = None,
        send_mail: bool = False,
        rt_parameters: Optional[Dict[str, str]] = None,
    ) -> int:
        params = rt_parameters if rt_parameters is not None else {}
        if send_mail:
            params["CF.{Mail Customer}"] = "yes"
        if status is not None:
            params["Status"] = status.value
        params["Owner"] = owner
        params["Requestor"] = requestor
        params["Subject"] = subject
        params["Text"] = text
        with attachment_files(attachments) as attachment_tuples:
            result = self._rt.create_ticket(queue, files=attachment_tuples, **params)
        if result == -1:
            raise SabotRtException("Unable to create RT ticket")
        return result

    def update_status(self, ticket_id: Union[str, int], new_status: TicketStatus):
        self._rt.edit_ticket(ticket_id, Status=new_status.value)

    def check_correspondance(self, ticket_id: Union[str, int]):
        short_history = self._rt.get_short_history(ticket_id)
        return any(
            [
                "correspondence added" in history_entry[1].lower()
                for history_entry in short_history
            ]
        )
