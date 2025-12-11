# SkySpark Authentication for n8n Integration

**Status:** ✅ Tested and Working (2025-12-09)

## Authentication Method

SkySpark on `http://mbcx.iconergyco.com` uses **session cookie authentication**.

### Cookie Details

- **Cookie Name:** `skyarc-auth-80`
- **Obtained via:** Browser login
- **Usage:** Include in HTTP request headers

### How to Get Cookie

1. Login at http://mbcx.iconergyco.com/ui/ (auto-remembers credentials)
2. Open DevTools (F12) → Application tab → Cookies → http://mbcx.iconergyco.com
3. Copy value of `skyarc-auth-80` cookie
4. Use in n8n HTTP nodes

## n8n Configuration

### HTTP Request Node

```json
{
  "method": "GET",
  "url": "http://mbcx.iconergyco.com/api/demo/read",
  "authentication": "none",
  "headers": {
    "Cookie": "skyarc-auth-80=<cookie-value-here>",
    "Accept": "application/json"
  }
}
```

### Alternative: Use Credentials

Create an n8n credential to store the cookie:

1. Go to Credentials → Add Credential → Header Auth
2. Name: `SkySpark Session`
3. Header Name: `Cookie`
4. Header Value: `skyarc-auth-80=<cookie-value>`

## Available API Endpoints

Base: `http://mbcx.iconergyco.com/api/demo/`

| Endpoint | Method | Purpose | Example |
|----------|--------|---------|---------|
| `/about` | GET | Server info | `/api/demo/about` |
| `/ops` | GET | Available operations | `/api/demo/ops` |
| `/read` | GET | Query records | `/api/demo/read?filter=site` |
| `/eval` | GET | Axon expression | `/api/demo/eval?expr=readAll(site)` |
| `/hisRead` | GET/POST | Historical data | `/api/demo/hisRead` |

## Common Queries

### Get All Sites
```
GET /api/demo/read?filter=site
```

### Get All Points
```
GET /api/demo/read?filter=point
```

### Evaluate Axon
```
GET /api/demo/eval?expr=readAll(equip and ahu)
```

## Important Notes

- ✅ Project `demo` works
- ❌ Projects `default`, `db`, `site` return 404
- Cookie may expire - need to re-login periodically
- No automated login available (web POST returns 501)

## Test Script

Located at: `.claude/skills/n8n-automation/scripts/skyspark_auth_cookie.py`

Run with:
```bash
python .claude/skills/n8n-automation/scripts/skyspark_auth_cookie.py
```

## n8n Workflow Test

**Status:** ✅ Successfully tested (2025-12-09)

### Test Workflow

Located at: `n8n/workflows/skyspark_api_test.json`

**Import into n8n:**

1. Open n8n at <http://localhost:5678>
2. Create new workflow → Click three dots menu (⋯) → Import from File
3. Select `skyspark_api_test.json`
4. Execute workflow (manual trigger)

**Workflow includes 4 test nodes:**

- ✅ Get Server Info (`/about`) - Returns SkySpark server details
- ✅ Get All Sites (`/read?filter=site`) - Returns list of sites
- ✅ Get Temperature Points (`/read?filter=point and temp and sensor`) - Returns temp sensors
- ✅ Count AHUs (`/eval?expr=readAll(equip and ahu).size()`) - Axon query example

**Verification:**

- All 4 HTTP Request nodes execute successfully
- Green connecting lines with "1 item" labels
- Click any node to view JSON response data
- Confirmed working on 2025-12-09

## Troubleshooting

**401 Unauthorized:**
- Cookie expired → Re-login and get new cookie

**404 Not Found:**
- Using wrong project → Use `demo` not `default`

**Connection refused:**
- VPN not connected (if required)
- Server down

## Related Documentation

- **Quick Reference:** `User-Files/work-tracking/reference-docs/skyspark-auth-guide.md`
- **SkySpark Access Config:** `User-Files/work-tracking/reference-docs/skyspark-access-config.md`
- **n8n Skill Overview:** `.claude/skills/n8n-automation/SKILL.md`
