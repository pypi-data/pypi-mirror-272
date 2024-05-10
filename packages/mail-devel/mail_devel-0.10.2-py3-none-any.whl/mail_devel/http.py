import logging
import os
import ssl
import uuid
from email import header, message_from_bytes, message_from_string, policy
from email.errors import MessageDefect
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from importlib import resources

from aiohttp import web
from aiohttp.web import Request, Response
from pymap.backend.dict.mailbox import Message
from pymap.parsing.specials import FetchRequirement
from pymap.parsing.specials.flag import Flag

from .mailbox import TestMailboxDict

_logger = logging.getLogger(__name__)


def decode_header(value: str) -> str:
    return str(header.make_header(header.decode_header(value)))


def flags_to_api(flags: frozenset[Flag]) -> list[str]:
    return [f.value.decode().strip("\\").lower() for f in flags]


async def run_app(
    api,
    host: str | None = None,
    port: int | None = None,
    ssl_context: ssl.SSLContext | None = None,
) -> web.AppRunner:
    app = web.AppRunner(
        api,
        access_log_format='%a "%r" %s %b "%{Referer}i" "%{User-Agent}i"',
    )
    await app.setup()

    site = web.TCPSite(
        app,
        host=host,
        port=port,
        reuse_address=True,
        reuse_port=True,
        ssl_context=ssl_context,
    )
    await site.start()


class Frontend:
    def __init__(
        self,
        mailboxes: TestMailboxDict,
        user: str,
        host: str = "",
        port: int = 8080,
        devel: str = "",
        flagged_seen: bool = False,
        client_max_size: int = 1 << 20,
        multi_user: bool = False,
    ):
        self.mailboxes: TestMailboxDict = mailboxes
        self.api: web.Application | None = None
        self.host: str = host
        self.port: int = port
        self.user: str = user
        self.devel: str = devel
        self.flagged_seen: bool = flagged_seen
        self.client_max_size: int = client_max_size
        self.multi_user: bool = multi_user

    def load_resource(self, resource: str) -> str:
        if self.devel:  # pragma: no cover
            with open(os.path.join(self.devel, resource), encoding="utf-8") as fp:
                return fp.read()

        package = f"{__package__}.resources"
        res = resources.files(package).joinpath(resource)
        if not res.is_file():
            raise FileNotFoundError()

        return res.read_text(encoding="utf-8")

    async def start(self) -> None:
        self.api = web.Application(client_max_size=self.client_max_size)

        self.api.add_routes(
            [
                web.get("/", self._page_index),
                web.get("/config", self._api_config),
                web.get(r"/{static:.*\.(css|js)}", self._page_static),
                web.post(r"/api/{account:\d+}/{mailbox:\d+}", self._api_post),
                web.post(r"/api/upload/{account:\d+}/{mailbox:\d+}", self._api_upload),
                web.get(r"/api", self._api_index),
                web.get(r"/api/{account:\d+}", self._api_account),
                web.get(r"/api/{account:\d+}/{mailbox:\d+}", self._api_mailbox),
                web.get(
                    r"/api/{account:\d+}/{mailbox:\d+}/{uid:\d+}",
                    self._api_message,
                ),
                web.get(
                    r"/api/{account:\d+}/{mailbox:\d+}/{uid:\d+}/reply",
                    self._api_reply,
                ),
                web.get(
                    r"/api/{account:\d+}/{mailbox:\d+}/{uid:\d+}/attachment/{attachment}",
                    self._api_attachment,
                ),
                web.get(
                    r"/api/{account:\d+}/{mailbox:\d+}/{uid:\d+}/flags", self._api_flag
                ),
                web.put(
                    r"/api/{account:\d+}/{mailbox:\d+}/{uid:\d+}/flags/{flag:[a-z]+}",
                    self._api_flag,
                ),
                web.delete(
                    r"/api/{account:\d+}/{mailbox:\d+}/{uid:\d+}/flags/{flag:[a-z]+}",
                    self._api_flag,
                ),
            ]
        )

        return await run_app(
            self.api,
            host=self.host or None,
            port=self.port,
        )

    async def _page_index(self, request: Request) -> Response:  # pylint: disable=W0613
        try:
            return Response(
                body=self.load_resource("index.html"),
                content_type="text/html",
            )
        except FileNotFoundError as e:  # pragma: no cover
            _logger.error("File 'index.html' not in resources")
            raise web.HTTPNotFound() from e

    async def _page_static(self, request: Request) -> Response:
        static = request.match_info["static"]
        if static.endswith(".js"):
            mimetype = "text/javascript"
        elif static.endswith(".css"):
            mimetype = "text/css"
        else:  # pragma: no cover
            raise web.HTTPNotFound()

        try:
            return Response(body=self.load_resource(static), content_type=mimetype)
        except FileNotFoundError as e:  # pragma: no cover
            _logger.error(f"File {static!r} not in resources")
            raise web.HTTPNotFound() from e

    async def _message_content(self, msg: Message) -> bytes:
        return bytes((await msg.load_content(FetchRequirement.CONTENT)).content)

    async def _convert_message(self, msg: Message, full: bool = False) -> dict:
        content = await self._message_content(msg)

        message = message_from_bytes(content)
        result = {
            "uid": msg.uid,
            "flags": flags_to_api(msg.permanent_flags),
            "header": {k.lower(): decode_header(v) for k, v in message.items()},
            "date": msg.internal_date.isoformat(),
        }

        if not full:
            return result

        result["attachments"] = []
        if message.is_multipart():
            for part in message.walk():
                ctype = part.get_content_type()
                cdispo = part.get_content_disposition()

                if cdispo == "attachment":
                    result["attachments"].append(part.get_filename())
                elif ctype == "text/plain":
                    result["body_plain"] = part.get_payload(decode=True).decode()
                elif ctype == "text/html":
                    result["body_html"] = part.get_payload(decode=True).decode()
        elif message.get_content_type() == "text/html":
            result["body_html"] = message.get_payload(decode=True).decode()
        else:
            result["body_plain"] = message.get_payload(decode=True).decode()

        result["content"] = bytes(content).decode()
        return result

    async def _api_config(self, request: Request) -> Response:  # pylint: disable=W0613
        return web.json_response(
            {
                "multi_user": self.multi_user,
                "flagged_seen": self.flagged_seen,
            }
        )

    async def _api_index(self, request: Request) -> Response:  # pylint: disable=W0613
        accounts = await self.mailboxes.list()
        return web.json_response(
            {self.mailboxes.id_of_user(user): user for user in accounts}
        )

    async def _api_account(self, request: Request) -> Response:  # pylint: disable=W0613
        try:
            account_id = int(request.match_info["account"])
            account = await self.mailboxes.get_by_id(account_id)
        except KeyError as e:  # pragma: no cover
            raise web.HTTPNotFound() from e

        mailboxes = await account.list_mailboxes()
        return web.json_response(
            {account.id_of_mailbox(e.name): e.name for e in mailboxes.list()}
        )

    async def _api_upload(self, request: Request) -> Response:  # pylint: disable=W0613
        try:
            account_id = int(request.match_info["account"])
            account = self.mailboxes.user_mapping[account_id]
            mailbox_id = int(request.match_info["mailbox"])
            mailbox = self.mailboxes[account].get_mailbox_name(mailbox_id)
        except KeyError as e:  # pragma: no cover
            raise web.HTTPNotFound() from e

        data = await request.json()
        if not isinstance(data, list):
            raise web.HTTPBadRequest()

        compat_strict = policy.compat32.clone(raise_on_defect=True)
        for mail in data:
            try:
                msg = message_from_string(mail["data"], policy=compat_strict)
                await self.mailboxes.append(
                    msg,
                    flags=frozenset({Flag(b"\\Seen")} if self.flagged_seen else []),
                    mailbox=mailbox,
                )
            except MessageDefect:
                continue

        return web.json_response({})

    async def _api_post(self, request: Request) -> Response:
        try:
            account_id = int(request.match_info["account"])
            account = self.mailboxes.user_mapping[account_id]
            mailbox_id = int(request.match_info["mailbox"])
            mailbox = self.mailboxes[account].get_mailbox_name(mailbox_id)
        except KeyError as e:  # pragma: no cover
            raise web.HTTPNotFound() from e

        data = await request.json()
        if not isinstance(data, dict):
            raise web.HTTPBadRequest()

        header, body = map(data.get, ("header", "body"))
        if not isinstance(header, dict) or not isinstance(body, str):
            raise web.HTTPBadRequest()

        message = MIMEMultipart()
        message.attach(MIMEText(body))

        for key, value in header.items():
            if key.strip() and value.strip():
                message.add_header(key.title(), value)

        for att in data.get("attachments", []):
            part = MIMEBase(*(att["mimetype"] or "text/plain").split("/"))
            part.set_payload(att["content"])
            part.add_header("Content-Transfer-Encoding", "base64")
            part.add_header(
                "Content-Disposition",
                f'attachment; filename="{att["name"]}"',  # noqa: B907
            )
            message.attach(part)

        await self.mailboxes.append(
            message,
            flags=frozenset({Flag(b"\\Seen")} if self.flagged_seen else []),
            mailbox=mailbox,
        )
        return web.json_response({"status": "ok"})

    async def _api_mailbox(self, request: Request) -> Response:
        try:
            account_id = int(request.match_info["account"])
            account = self.mailboxes.user_mapping[account_id]
            mailbox_id = int(request.match_info["mailbox"])
            mailbox = await self.mailboxes[account].get_mailbox_by_id(mailbox_id)
        except KeyError as e:  # pragma: no cover
            raise web.HTTPNotFound() from e

        result = []
        async for msg in mailbox.messages():
            result.append(await self._convert_message(msg))
        result.sort(key=lambda x: x["date"], reverse=True)
        return web.json_response(result)

    async def _api_message(self, request: Request) -> Response:
        try:
            account_id = int(request.match_info["account"])
            account = self.mailboxes.user_mapping[account_id]
            mailbox_id = int(request.match_info["mailbox"])
            uid = int(request.match_info["uid"])
            mailbox = await self.mailboxes[account].get_mailbox_by_id(mailbox_id)
        except (IndexError, KeyError) as e:  # pragma: no cover
            raise web.HTTPNotFound() from e

        async for msg in mailbox.messages():
            if msg.uid == uid:
                return web.json_response(await self._convert_message(msg, True))

        raise web.HTTPNotFound()

    async def _api_reply(self, request: Request) -> Response:
        try:
            account_id = int(request.match_info["account"])
            mailbox_id = int(request.match_info["mailbox"])
            uid = int(request.match_info["uid"])
            account = await self.mailboxes.get_by_id(account_id)
            mailbox = await account.get_mailbox_by_id(mailbox_id)
        except (IndexError, KeyError) as e:  # pragma: no cover
            raise web.HTTPNotFound() from e

        async for msg in mailbox.messages():
            if msg.uid == uid:
                message = await self._convert_message(msg, True)
                headers = message["header"]
                headers["subject"] = f"RE: {headers['subject']}"
                msg_id = headers.get("message-id", None)
                if msg_id:
                    headers["in-reply-to"] = msg_id
                    headers["references"] = f"{msg_id} {headers.get('references', '')}"
                headers["message-id"] = f"{uuid.uuid4()}@mail-devel"
                headers["to"] = headers["from"]
                headers["from"] = self.user
                headers.pop("content-type", None)
                for key in list(headers):
                    if key.startswith("x-"):
                        headers.pop(key, None)
                return web.json_response(message)

        raise web.HTTPNotFound()

    async def _api_attachment(self, request: Request) -> Response:
        try:
            account_id = int(request.match_info["account"])
            mailbox_id = int(request.match_info["mailbox"])
            uid = int(request.match_info["uid"])
            attachment = request.match_info["attachment"]
            account = await self.mailboxes.get_by_id(account_id)
            mailbox = await account.get_mailbox_by_id(mailbox_id)
        except (IndexError, KeyError) as e:  # pragma: no cover
            raise web.HTTPNotFound() from e

        message = None
        async for msg in mailbox.messages():
            if msg.uid == uid:
                content = await self._message_content(msg)
                message = message_from_bytes(content)

        if not message or not message.is_multipart():
            raise web.HTTPNotFound()

        for part in message.walk():
            if (
                part.get_content_disposition() == "attachment"
                and part.get_filename() == attachment
            ):
                cte = part.get("Content-Transfer-Encoding")
                body = part.get_payload(decode=bool(cte))
                return web.Response(
                    body=body,
                    headers={
                        "Content-Type": part.get("Content-Type"),
                        "Content-Disposition": part.get("Content-Disposition"),
                    },
                )

        raise web.HTTPNotFound()

    async def _api_flag(self, request: Request) -> Response:
        try:
            account_id = int(request.match_info["account"])
            mailbox_id = int(request.match_info["mailbox"])
            account = await self.mailboxes.get_by_id(account_id)
            mailbox = await account.get_mailbox_by_id(mailbox_id)
            uid = int(request.match_info["uid"])

            if request.method in ("DELETE", "PUT"):
                flags = [Flag(b"\\" + request.match_info["flag"].title().encode())]
            else:
                flags = []
        except (IndexError, KeyError) as e:  # pragma: no cover
            raise web.HTTPNotFound() from e

        async for msg in mailbox.messages():
            if msg.uid != uid:
                continue

            if request.method == "DELETE":
                msg.permanent_flags = msg.permanent_flags.difference(flags)
            elif request.method == "PUT":
                msg.permanent_flags = msg.permanent_flags.union(flags)

            return web.json_response(flags_to_api(msg.permanent_flags))

        raise web.HTTPNotFound()
