# services

Docker Compose files for self-hosted services running on `suobdesk` (HP OmniDesk, Ubuntu), accessible over [Tailscale](https://tailscale.com).

All credentials are scrubbed. Replace `CHANGE_ME` and `YOUR_TAILSCALE_IP` before use.

## Services

| Directory | Service | Port |
|---|---|---|
| `landing/` | Dashboard landing page | 8000 |
| `searxng/` | [SearXNG](https://searxng.github.io/searxng/) — meta-search | 8888 |
| `miniflux/` | [Miniflux](https://miniflux.app) — RSS reader | 8090 |
| `wikindx/` | [WIKINDX](https://wikindx.sourceforge.io) — research bibliography manager | 8091 |
| `nextcloud/` | [Nextcloud](https://nextcloud.com) — file sync | 8092 |
| `forgejo/` | [Forgejo](https://forgejo.org) — self-hosted Git | 8093 (web), 2222 (SSH) |

## Usage

```bash
cd <service>
docker compose up -d
```

Each service is independent. Bring them up or down individually.

## Notes

- SearXNG config (`settings.yml`) lives separately at `~/.searxng/` on the host — mount it at `/etc/searxng` in the container. See [`searxng/README.md`](searxng/README.md) for the AI content filter plugin and example config.
- WIKINDX requires a `config.php` mounted into the fpm container — not included here.
- Forgejo runs its first-time setup wizard on first visit.
- All services are internal-only; no ports are exposed to the public internet.
