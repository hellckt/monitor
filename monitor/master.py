import webbrowser
from datetime import datetime

from mitmproxy import addons, controller, http, master
from mitmproxy.addons import termlog, wsgiapp

from monitor.app.ext.database import DBSession
from monitor.app.models import Ban, Flow
from monitor.manage import app


class MonitorError(Exception):
    pass


class MonitorMaster(master.Master):
    def __init__(self, options, server, with_termlog=False) -> None:
        master.Master.__init__(self, options, server)
        self.has_errored = False
        self.monitor_host = 'monitor.zkt'
        self.monitor_port = 80
        # TODO: 考虑用tornado替代flask以减少冗余依赖
        # 将Flask的实例注入mitmproxy
        self.addons.add(wsgiapp.WSGIApp(app, self.monitor_host,
                                        self.monitor_port))
        self.db_session = DBSession()
        if with_termlog:
            self.addons.add(termlog.TermLog())
        self.addons.add(*addons.default_addons())
        if not self.options.no_server:
            self.add_log(
                "代理服务运行于 http://{}".format(server.address),
                "info"
            )

    @controller.handler
    def log(self, e):
        if e.level == "error":
            self.has_errored = True

    @controller.handler
    def request(self, f):
        # 过滤掉请求的本地服务，否则会导致错误产生
        is_monitor = (f.request.pretty_host, f.request.port) == (
            self.monitor_host, self.monitor_port)
        is_onboarding = (f.request.pretty_host, f.request.port) == (
            self.options.onboarding_host, self.options.onboarding_port)
        if is_monitor or is_onboarding or not isinstance(f, http.HTTPFlow):
            return f
        flow = Flow(f.request.scheme, f.request.host, f.request.port,
                    f.request.path)
        try:
            flow.create_timestamp = datetime.now()
            self.db_session.add(flow)
            self.db_session.commit()
            self.db_session.flush()
        except Exception as e:
            self.add_log("请求写入失败：{}".format(e), "error")

        ban = self.db_session.query(Ban).filter_by(
            netloc=f.request.host).first()
        if not ban:
            return f

        if ban.only_netloc:
            self._make_ban_response(f)
        else:
            path = ban.path.filter_by(
                full_path=f.request.path).first()
            if path:
                self._make_ban_response(f)

    @staticmethod
    def _make_ban_response(f, text: bytes = None):
        # TODO: 添加用户自定义功能
        if not text:
            text = """
            <!DOCTYPE html>
            <html>
            <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>FORBIDDEN</title>
            </head>
            <body>
            <header>
            <h1>FORBIDDEN BY MONITOR!</h1>
            </header>
            </body>
            </html>"""
        f.response = http.HTTPResponse.make(200, text.encode(),
                                            {"Content-Type": "text/html"})

    def run(self):  # pragma: no cover
        app_url = "http://{}:{}/".format(self.monitor_host, self.monitor_port)
        self.add_log("Web 服务运行于 {}".format(app_url), "info")

        success = open_browser(app_url)
        if not success:
            self.add_log("浏览器未打开，请打开浏览器并访问该地址 {}".format(app_url), "info")
        super().run()


def open_browser(url: str) -> bool:
    """
    Open a URL in a browser window.
    In contrast to webbrowser.open, we limit the list of suitable browsers.
    This gracefully degrades to a no-op on headless servers, where webbrowser.open
    would otherwise open lynx.

    Returns:
        True, if a browser has been opened
        False, if no suitable browser has been found.
    """
    browsers = (
        "windows-default", "macosx",
        "google-chrome", "chrome", "chromium", "chromium-browser",
        "firefox", "opera", "safari",
    )
    for browser in browsers:
        try:
            b = webbrowser.get(browser)
        except webbrowser.Error:
            pass
        else:
            b.open(url)
            return True
    return False
