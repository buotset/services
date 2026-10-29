# SearXNG

Meta-search on port 8888, with a custom plugin that removes AI-generated content from results.

## Layout

| Path | Purpose |
|---|---|
| `docker-compose.yml` | Container definition |
| `plugins/ai_filter.py` | AI content filter plugin, mounted into the container's plugin package |
| `config/settings.example.yml` | `settings.yml` template (enables the plugin) |
| `config/ai-blocklist.yml` | Hostnames removed by the plugin |

## Setup

```bash
mkdir -p ~/.searxng
cp config/settings.example.yml ~/.searxng/settings.yml   # then replace CHANGE_ME
cp config/ai-blocklist.yml ~/.searxng/
# point the /etc/searxng volume in docker-compose.yml at ~/.searxng
docker compose up -d
```

The container runs as uid 977, so files in `~/.searxng` may need `sudo chown 977:977`.

## AI content filter

The `ai_filter` plugin does two things:

- **Site blocklist (all categories):** removes results from hosts in `ai-blocklist.yml` (AI image generators, AI art galleries, AI stock imagery).
- **Image labels (images only):** removes image results whose title, description or URL mark them as AI generated ("AI generated", "Midjourney", "Stable Diffusion", "DALL-E", "made with AI", ...). Text results are not keyword-filtered, so articles about AI still appear.

**Searching for AI disables the filter.** If the query mentions AI ("ai", "artificial intelligence", "midjourney", "stable diffusion", ...), the plugin leaves results untouched for that search.

Users can turn it off under Preferences → General → "AI content filter".

### Editing

- Add hosts to `~/.searxng/ai-blocklist.yml` (one regex per line, matched against the result host), then `docker restart searxng`.
- Keyword patterns are `AI_MARKERS` (image labels) and `AI_QUERY` (query bypass) in `plugins/ai_filter.py`.

### Notes

- A `plugins:` block in `settings.yml` replaces SearXNG's default plugin list rather than merging with it, so the example repeats the defaults. Re-check them against upstream `searx/settings.yml` after major image updates.
- Unlabelled AI images on general sites (Pinterest, DeviantArt, wallpaper sites) are not caught.
