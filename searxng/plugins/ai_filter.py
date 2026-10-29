# SPDX-License-Identifier: AGPL-3.0-or-later
"""Remove AI generated content from results, unless the query is about AI.

- Results from hosts listed in ``ai-blocklist.yml`` (next to ``settings.yml``)
  are removed from every category.
- Image results whose title, description or URL mark them as AI generated are
  removed, which catches AI images hosted on otherwise legitimate sites.

If the query itself mentions AI (e.g. "midjourney prompts", "ai art"), the
plugin does nothing, so searching for AI content still works.
"""

import re
import typing as t

from searx.plugins import Plugin, PluginInfo
from searx.settings_loader import get_yaml_cfg

if t.TYPE_CHECKING:
    import flask
    from searx.search import SearchWithPlugins
    from searx.extended_types import SXNG_Request
    from searx.result_types import Result
    from searx.plugins import PluginCfg

AI_MARKERS = re.compile(
    r"\b("
    r"ai[\s-]?(generated|created|made|art|artwork|artist|image|images|illustration|render|photo|picture|wallpaper)s?"
    r"|(generated|created|made)\s+(with|by|using)\s+(an?\s+)?ai"
    r"|generative\s+ai|gen[\s-]?ai"
    r"|midjourney|stable[\s-]?diffusion|sdxl|dall[\s·-]?e|dalle"
    r"|leonardo\s?ai|nightcafe|novelai|adobe\s+firefly|ideogram|flux\.1"
    r"|text[\s-]to[\s-]image|ai\s+generator"
    r")\b",
    re.IGNORECASE,
)

AI_QUERY = re.compile(r"\b(ai|a\.i\.|artificial\s+intelligence|civitai|lexica|craiyon)\b", re.IGNORECASE)

BLOCKED_HOSTS: set[re.Pattern[str]] = set()


@t.final
class SXNGPlugin(Plugin):
    """Remove AI generated content from results, unless the query is about AI."""

    id = "ai_filter"

    def __init__(self, plg_cfg: "PluginCfg") -> None:
        super().__init__(plg_cfg)
        self.info = PluginInfo(
            id=self.id,
            name="AI content filter",
            description="Remove AI generated images and AI content sites, unless searching for AI",
            preference_section="general",
        )

    def on_result(self, request: "SXNG_Request", search: "SearchWithPlugins", result: "Result") -> bool:
        query = search.search_query.query
        if AI_QUERY.search(query) or AI_MARKERS.search(query):
            return True

        if result.parsed_url and any(p.search(result.parsed_url.netloc) for p in BLOCKED_HOSTS):
            return False

        if getattr(result, "template", None) != "images.html":
            return True
        text = " ".join(str(getattr(result, f, "") or "") for f in ("title", "content", "url", "img_src"))
        return not AI_MARKERS.search(text)

    def init(self, app: "flask.Flask") -> bool:  # pylint: disable=unused-argument
        global BLOCKED_HOSTS  # pylint: disable=global-statement
        try:
            BLOCKED_HOSTS = {re.compile(p) for p in get_yaml_cfg("ai-blocklist.yml") or []}
        except FileNotFoundError:
            self.log.warning("ai-blocklist.yml not found, only filtering image results")
        return True
