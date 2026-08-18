# Polaris Roadmap

## Vision

Polaris is a lightweight, plugin-driven automation bot that monitors important services and delivers actionable notifications through Discord.

Core principles:

- One plugin execution returns zero or one Event.
- Services communicate with external APIs.
- Plugins contain business logic.
- Scheduler owns execution timing.
- Plugins may request schedule changes through the scheduler interface.
- Every plugin should have unit tests.

---

# Current Features (v1)

- Plugin discovery
- APScheduler-based scheduling
- Discord notifications
- Embedded Discord messages
- Structured JSON logging
- Weather Forecast plugin
- Weather Alert plugin
- Alert persistence
- Adaptive weather polling

---

# Planned Improvements

## Weather

- Better forecast embeds
- Rich weather alert formatting
- Store alert metadata instead of only IDs
- Alert severity filtering
- Quiet hours

## Monitoring

- Internet speed monitor
- External service health monitor
- Website uptime checks
- SSL certificate expiration monitor

## Information

- RSS feeds
- Daily quotes
- Calendar reminders
- News headlines

## Home

- Home Assistant integration
- Synology monitoring
- UPS monitoring
- Local network device monitoring

## Charity

- DonorDrive integration
- Extra Life donation notifications
- Donation milestones
- Team progress tracking

## Developer Experience

- Increase unit test coverage
- GitHub Actions CI
- Docker image
- Configuration validation
- Plugin documentation

---

# Long-Term Goals

- Slack notifications
- Email notifications
- Web dashboard
- Plugin marketplace
- Multiple notification channels