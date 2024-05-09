# cloudflare-python

## Table of commands

|`GET`   |`PUT`   |`POST`  |`PATCH` |`DELETE`|API call|
|--------|--------|--------|--------|--------|:-------|
|`GET`   |-       |`PUT`   |-       |-       | /accounts |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/access/apps |
|`GET`   |`POST`  |-       |-       |`DELETE`| /accounts/:id/access/apps/:id/ca |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/access/apps/:id/policies |
|-       |`POST`  |-       |-       |-       | /accounts/:id/access/apps/:id/revoke_tokens |
|`GET`   |-       |-       |-       |-       | /accounts/:id/access/apps/:id/user_policy_checks |
|`GET`   |-       |-       |-       |-       | /accounts/:id/access/apps/ca |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/access/certificates |
|`GET`   |-       |`PUT`   |-       |-       | /accounts/:id/access/certificates/settings |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/access/custom_pages |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/access/groups |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/access/identity_providers |
|`GET`   |-       |`PUT`   |-       |-       | /accounts/:id/access/keys |
|-       |`POST`  |-       |-       |-       | /accounts/:id/access/keys/rotate |
|`GET`   |-       |-       |-       |-       | /accounts/:id/access/logs/access_requests |
|`GET`   |`POST`  |`PUT`   |-       |-       | /accounts/:id/access/organizations |
|-       |`POST`  |-       |-       |-       | /accounts/:id/access/organizations/revoke_user |
|-       |-       |-       |`PATCH` |-       | /accounts/:id/access/seats |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/access/service_tokens |
|-       |`POST`  |-       |-       |-       | /accounts/:id/access/service_tokens/:id/refresh |
|-       |`POST`  |-       |-       |-       | /accounts/:id/access/service_tokens/:id/rotate |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/access/tags |
|`GET`   |-       |-       |-       |-       | /accounts/:id/access/users |
|`GET`   |-       |-       |-       |-       | /accounts/:id/access/users/:id/active_sessions |
|`GET`   |-       |-       |-       |-       | /accounts/:id/access/users/:id/failed_logins |
|`GET`   |-       |-       |-       |-       | /accounts/:id/access/users/:id/last_seen_identity |
|`GET`   |`POST`  |-       |`PATCH` |`DELETE`| /accounts/:id/addressing/address_maps |
|-       |-       |`PUT`   |-       |`DELETE`| /accounts/:id/addressing/address_maps/:id/accounts |
|-       |-       |`PUT`   |-       |`DELETE`| /accounts/:id/addressing/address_maps/:id/ips |
|-       |-       |`PUT`   |-       |`DELETE`| /accounts/:id/addressing/address_maps/:id/zones |
|-       |`POST`  |-       |-       |-       | /accounts/:id/addressing/loa_documents |
|`GET`   |-       |-       |-       |-       | /accounts/:id/addressing/loa_documents/:id/download |
|`GET`   |`POST`  |-       |`PATCH` |`DELETE`| /accounts/:id/addressing/prefixes |
|`GET`   |-       |-       |`PATCH` |-       | /accounts/:id/addressing/prefixes/:id/bgp/prefixes |
|`GET`   |-       |-       |`PATCH` |-       | /accounts/:id/addressing/prefixes/:id/bgp/status |
|`GET`   |`POST`  |-       |-       |`DELETE`| /accounts/:id/addressing/prefixes/:id/bindings |
|`GET`   |`POST`  |-       |-       |`DELETE`| /accounts/:id/addressing/prefixes/:id/delegations |
|`GET`   |-       |-       |-       |-       | /accounts/:id/addressing/services |
|-       |`POST`  |-       |-       |-       | /accounts/:id/ai/run |
|-       |`POST`  |-       |-       |-       | /accounts/:id/ai/run/proxy |
|`GET`   |-       |-       |-       |-       | /accounts/:id/alerting/v3/available_alerts |
|`GET`   |-       |-       |-       |-       | /accounts/:id/alerting/v3/destinations/eligible |
|`GET`   |-       |-       |-       |`DELETE`| /accounts/:id/alerting/v3/destinations/pagerduty |
|`GET`   |`POST`  |-       |-       |-       | /accounts/:id/alerting/v3/destinations/pagerduty/connect |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/alerting/v3/destinations/webhooks |
|`GET`   |-       |-       |-       |-       | /accounts/:id/alerting/v3/history |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/alerting/v3/policies |
|`GET`   |-       |-       |-       |-       | /accounts/:id/audit_logs |
|-       |`POST`  |-       |-       |-       | /accounts/:id/brand-protection/submit |
|`GET`   |-       |-       |-       |-       | /accounts/:id/brand-protection/url-info |
|`GET`   |`POST`  |-       |`PATCH` |`DELETE`| /accounts/:id/cfd_tunnel |
|`GET`   |-       |`PUT`   |-       |-       | /accounts/:id/cfd_tunnel/:id/configurations |
|`GET`   |-       |-       |-       |`DELETE`| /accounts/:id/cfd_tunnel/:id/connections |
|`GET`   |-       |-       |-       |-       | /accounts/:id/cfd_tunnel/:id/connectors |
|-       |`POST`  |-       |-       |-       | /accounts/:id/cfd_tunnel/:id/management |
|`GET`   |-       |-       |-       |-       | /accounts/:id/cfd_tunnel/:id/token |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/challenges/widgets |
|-       |`POST`  |-       |-       |-       | /accounts/:id/challenges/widgets/:id/rotate_secret |
|`GET`   |`POST`  |-       |-       |`DELETE`| /accounts/:id/custom_ns |
|`GET`   |-       |-       |-       |-       | /accounts/:id/custom_ns/availability |
|`GET`   |-       |`PUT`   |-       |-       | /accounts/:id/custom_pages |
|`GET`   |`POST`  |-       |-       |`DELETE`| /accounts/:id/d1/database |
|-       |`POST`  |-       |-       |-       | /accounts/:id/d1/database/:id/query |
|`GET`   |-       |-       |-       |-       | /accounts/:id/devices |
|`GET`   |-       |-       |-       |-       | /accounts/:id/devices/:id/override_codes |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/devices/dex_tests |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/devices/networks |
|`GET`   |-       |-       |-       |-       | /accounts/:id/devices/policies |
|`GET`   |`POST`  |-       |`PATCH` |`DELETE`| /accounts/:id/devices/policy |
|`GET`   |-       |`PUT`   |-       |-       | /accounts/:id/devices/policy/:id/exclude |
|`GET`   |-       |`PUT`   |-       |-       | /accounts/:id/devices/policy/:id/fallback_domains |
|`GET`   |-       |`PUT`   |-       |-       | /accounts/:id/devices/policy/:id/include |
|`GET`   |-       |`PUT`   |-       |-       | /accounts/:id/devices/policy/exclude |
|`GET`   |-       |`PUT`   |-       |-       | /accounts/:id/devices/policy/fallback_domains |
|`GET`   |-       |`PUT`   |-       |-       | /accounts/:id/devices/policy/include |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/devices/posture |
|`GET`   |`POST`  |-       |`PATCH` |`DELETE`| /accounts/:id/devices/posture/integration |
|-       |`POST`  |-       |-       |-       | /accounts/:id/devices/revoke |
|`GET`   |-       |`PUT`   |-       |-       | /accounts/:id/devices/settings |
|-       |`POST`  |-       |-       |-       | /accounts/:id/devices/unrevoke |
|`GET`   |-       |-       |-       |-       | /accounts/:id/dex/colos |
|`GET`   |-       |-       |-       |-       | /accounts/:id/dex/fleet-status/devices |
|`GET`   |-       |-       |-       |-       | /accounts/:id/dex/fleet-status/live |
|`GET`   |-       |-       |-       |-       | /accounts/:id/dex/fleet-status/over-time |
|`GET`   |-       |-       |-       |-       | /accounts/:id/dex/http-tests |
|`GET`   |-       |-       |-       |-       | /accounts/:id/dex/http-tests/:id/percentiles |
|`GET`   |-       |-       |-       |-       | /accounts/:id/dex/tests |
|`GET`   |-       |-       |-       |-       | /accounts/:id/dex/tests/unique-devices |
|`GET`   |-       |-       |-       |-       | /accounts/:id/dex/traceroute-test-results/:id/network-path |
|`GET`   |-       |-       |-       |-       | /accounts/:id/dex/traceroute-tests |
|`GET`   |-       |-       |-       |-       | /accounts/:id/dex/traceroute-tests/:id/network-path |
|`GET`   |-       |-       |-       |-       | /accounts/:id/dex/traceroute-tests/:id/percentiles |
|-       |`POST`  |-       |-       |-       | /accounts/:id/diagnostics/traceroute |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/dlp/datasets |
|-       |`POST`  |-       |-       |-       | /accounts/:id/dlp/datasets/:id/upload |
|-       |`POST`  |-       |-       |-       | /accounts/:id/dlp/patterns/validate |
|`GET`   |-       |`PUT`   |-       |-       | /accounts/:id/dlp/payload_log |
|`GET`   |-       |-       |-       |-       | /accounts/:id/dlp/profiles |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/dlp/profiles/custom |
|`GET`   |-       |`PUT`   |-       |-       | /accounts/:id/dlp/profiles/predefined |
|`GET`   |`POST`  |-       |`PATCH` |`DELETE`| /accounts/:id/dns_firewall |
|`GET`   |-       |-       |-       |-       | /accounts/:id/dns_firewall/:id/dns_analytics/report |
|`GET`   |-       |-       |-       |-       | /accounts/:id/dns_firewall/:id/dns_analytics/report/bytime |
|`GET`   |`POST`  |-       |-       |`DELETE`| /accounts/:id/email/routing/addresses |
|`GET`   |`POST`  |-       |`PATCH` |`DELETE`| /accounts/:id/firewall/access_rules/rules |
|`GET`   |`POST`  |-       |-       |-       | /accounts/:id/gateway |
|`GET`   |-       |-       |-       |-       | /accounts/:id/gateway/app_types |
|`GET`   |-       |`PUT`   |-       |-       | /accounts/:id/gateway/audit_ssh_settings |
|`GET`   |-       |-       |-       |-       | /accounts/:id/gateway/categories |
|`GET`   |-       |`PUT`   |`PATCH` |-       | /accounts/:id/gateway/configuration |
|`GET`   |`POST`  |`PUT`   |`PATCH` |`DELETE`| /accounts/:id/gateway/lists |
|`GET`   |-       |-       |-       |-       | /accounts/:id/gateway/lists/:id/items |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/gateway/locations |
|`GET`   |-       |`PUT`   |-       |-       | /accounts/:id/gateway/logging |
|`GET`   |`POST`  |-       |`PATCH` |`DELETE`| /accounts/:id/gateway/proxy_endpoints |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/gateway/rules |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/hyperdrive/configs |
|`GET`   |`POST`  |-       |`PATCH` |`DELETE`| /accounts/:id/images/v1 |
|`GET`   |-       |-       |-       |-       | /accounts/:id/images/v1/:id/blob |
|`GET`   |-       |-       |-       |-       | /accounts/:id/images/v1/keys |
|`GET`   |-       |-       |-       |-       | /accounts/:id/images/v1/stats |
|`GET`   |`POST`  |-       |`PATCH` |`DELETE`| /accounts/:id/images/v1/variants |
|`GET`   |-       |-       |-       |-       | /accounts/:id/images/v2 |
|-       |`POST`  |-       |-       |-       | /accounts/:id/images/v2/direct_upload |
|`GET`   |-       |-       |-       |-       | /accounts/:id/intel/asn |
|`GET`   |-       |-       |-       |-       | /accounts/:id/intel/asn/:id/subnets |
|`GET`   |-       |-       |-       |-       | /accounts/:id/intel/dns |
|`GET`   |-       |-       |-       |-       | /accounts/:id/intel/domain |
|`GET`   |-       |-       |-       |-       | /accounts/:id/intel/domain-history |
|`GET`   |-       |-       |-       |-       | /accounts/:id/intel/domain/bulk |
|`GET`   |`POST`  |-       |-       |-       | /accounts/:id/intel/indicator-feeds |
|`GET`   |-       |-       |-       |-       | /accounts/:id/intel/indicator-feeds/:id/data |
|-       |-       |`PUT`   |-       |-       | /accounts/:id/intel/indicator-feeds/:id/snapshot |
|-       |-       |`PUT`   |-       |-       | /accounts/:id/intel/indicator-feeds/permissions/add |
|-       |-       |`PUT`   |-       |-       | /accounts/:id/intel/indicator-feeds/permissions/remove |
|`GET`   |-       |-       |-       |-       | /accounts/:id/intel/indicator-feeds/permissions/view |
|`GET`   |-       |-       |-       |-       | /accounts/:id/intel/ip |
|`GET`   |-       |-       |-       |-       | /accounts/:id/intel/ip-list |
|-       |`POST`  |-       |-       |-       | /accounts/:id/intel/miscategorization |
|`GET`   |-       |-       |-       |-       | /accounts/:id/intel/sinkholes |
|`GET`   |-       |-       |-       |-       | /accounts/:id/intel/whois |
|`GET`   |`POST`  |`PUT`   |`PATCH` |`DELETE`| /accounts/:id/load_balancers/monitors |
|-       |`POST`  |-       |-       |-       | /accounts/:id/load_balancers/monitors/:id/preview |
|`GET`   |-       |-       |-       |-       | /accounts/:id/load_balancers/monitors/:id/references |
|`GET`   |`POST`  |`PUT`   |`PATCH` |`DELETE`| /accounts/:id/load_balancers/pools |
|`GET`   |-       |-       |-       |-       | /accounts/:id/load_balancers/pools/:id/health |
|-       |`POST`  |-       |-       |-       | /accounts/:id/load_balancers/pools/:id/preview |
|`GET`   |-       |-       |-       |-       | /accounts/:id/load_balancers/pools/:id/references |
|`GET`   |-       |-       |-       |-       | /accounts/:id/load_balancers/preview |
|`GET`   |-       |-       |-       |-       | /accounts/:id/load_balancers/regions |
|`GET`   |-       |-       |-       |-       | /accounts/:id/load_balancers/search |
|`GET`   |-       |-       |-       |-       | /accounts/:id/logpush/datasets/:id/fields |
|`GET`   |-       |-       |-       |-       | /accounts/:id/logpush/datasets/:id/jobs |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/logpush/jobs |
|-       |`POST`  |-       |-       |-       | /accounts/:id/logpush/ownership |
|-       |`POST`  |-       |-       |-       | /accounts/:id/logpush/ownership/validate |
|-       |`POST`  |-       |-       |-       | /accounts/:id/logpush/validate/destination/exists |
|-       |`POST`  |-       |-       |-       | /accounts/:id/logpush/validate/origin |
|`GET`   |`POST`  |-       |-       |`DELETE`| /accounts/:id/logs/control/cmb/config |
|`GET`   |-       |`PUT`   |-       |-       | /accounts/:id/magic/cf_interconnects |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/magic/gre_tunnels |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/magic/ipsec_tunnels |
|-       |`POST`  |-       |-       |-       | /accounts/:id/magic/ipsec_tunnels/:id/psk_generate |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/magic/routes |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/members |
|`GET`   |`POST`  |`PUT`   |`PATCH` |`DELETE`| /accounts/:id/mnm/config |
|`GET`   |-       |-       |-       |-       | /accounts/:id/mnm/config/full |
|`GET`   |`POST`  |`PUT`   |`PATCH` |`DELETE`| /accounts/:id/mnm/rules |
|-       |-       |-       |`PATCH` |-       | /accounts/:id/mnm/rules/:id/advertisement |
|`GET`   |`POST`  |-       |-       |`DELETE`| /accounts/:id/mtls_certificates |
|`GET`   |-       |-       |-       |-       | /accounts/:id/mtls_certificates/:id/associations |
|`GET`   |`POST`  |-       |`PATCH` |`DELETE`| /accounts/:id/pages/projects |
|`GET`   |`POST`  |-       |-       |`DELETE`| /accounts/:id/pages/projects/:id/deployments |
|`GET`   |-       |-       |-       |-       | /accounts/:id/pages/projects/:id/deployments/:id/history/logs |
|-       |`POST`  |-       |-       |-       | /accounts/:id/pages/projects/:id/deployments/:id/retry |
|-       |`POST`  |-       |-       |-       | /accounts/:id/pages/projects/:id/deployments/:id/rollback |
|`GET`   |`POST`  |-       |`PATCH` |`DELETE`| /accounts/:id/pages/projects/:id/domains |
|-       |`POST`  |-       |-       |-       | /accounts/:id/pages/projects/:id/purge_build_cache |
|`GET`   |`POST`  |-       |-       |-       | /accounts/:id/pcaps |
|`GET`   |-       |-       |-       |-       | /accounts/:id/pcaps/:id/download |
|`GET`   |`POST`  |-       |-       |`DELETE`| /accounts/:id/pcaps/ownership |
|-       |`POST`  |-       |-       |-       | /accounts/:id/pcaps/ownership/validate |
|`GET`   |`POST`  |-       |-       |`DELETE`| /accounts/:id/r2/buckets |
|`GET`   |-       |`PUT`   |-       |-       | /accounts/:id/registrar/domains |
|-       |`POST`  |-       |-       |-       | /accounts/:id/request-tracer/trace |
|`GET`   |-       |-       |-       |-       | /accounts/:id/roles |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/rules/lists |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/rules/lists/:id/items |
|`GET`   |-       |-       |-       |-       | /accounts/:id/rules/lists/bulk_operations |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/rulesets |
|-       |`POST`  |-       |`PATCH` |`DELETE`| /accounts/:id/rulesets/:id/rules |
|`GET`   |-       |-       |-       |`DELETE`| /accounts/:id/rulesets/:id/versions |
|`GET`   |-       |-       |-       |-       | /accounts/:id/rulesets/:id/versions/:id/by_tag |
|`GET`   |-       |`PUT`   |-       |-       | /accounts/:id/rulesets/phases/:id/entrypoint |
|`GET`   |-       |-       |-       |-       | /accounts/:id/rulesets/phases/:id/entrypoint/versions |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/rum/site_info |
|`GET`   |-       |-       |-       |-       | /accounts/:id/rum/site_info/list |
|-       |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/rum/v2/:id/rule |
|`GET`   |`POST`  |-       |-       |-       | /accounts/:id/rum/v2/:id/rules |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/secondary_dns/acls |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/secondary_dns/peers |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/secondary_dns/tsigs |
|`GET`   |-       |-       |-       |-       | /accounts/:id/storage/analytics |
|`GET`   |-       |-       |-       |-       | /accounts/:id/storage/analytics/stored |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/storage/kv/namespaces |
|-       |-       |`PUT`   |-       |`DELETE`| /accounts/:id/storage/kv/namespaces/:id/bulk |
|`GET`   |-       |-       |-       |-       | /accounts/:id/storage/kv/namespaces/:id/keys |
|`GET`   |-       |-       |-       |-       | /accounts/:id/storage/kv/namespaces/:id/metadata |
|`GET`   |-       |`PUT`   |-       |`DELETE`| /accounts/:id/storage/kv/namespaces/:id/values |
|`GET`   |`POST`  |-       |-       |`DELETE`| /accounts/:id/stream |
|`GET`   |-       |-       |`PATCH` |`DELETE`| /accounts/:id/stream/:id/audio |
|-       |`POST`  |-       |-       |-       | /accounts/:id/stream/:id/audio/copy |
|`GET`   |-       |`PUT`   |-       |`DELETE`| /accounts/:id/stream/:id/captions |
|`GET`   |`POST`  |-       |-       |`DELETE`| /accounts/:id/stream/:id/downloads |
|`GET`   |-       |-       |-       |-       | /accounts/:id/stream/:id/embed |
|-       |`POST`  |-       |-       |-       | /accounts/:id/stream/:id/token |
|-       |`POST`  |-       |-       |-       | /accounts/:id/stream/clip |
|-       |`POST`  |-       |-       |-       | /accounts/:id/stream/copy |
|-       |`POST`  |-       |-       |-       | /accounts/:id/stream/direct_upload |
|`GET`   |`POST`  |-       |-       |`DELETE`| /accounts/:id/stream/keys |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/stream/live_inputs |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/stream/live_inputs/:id/outputs |
|`GET`   |-       |-       |-       |-       | /accounts/:id/stream/storage-usage |
|`GET`   |`POST`  |-       |-       |`DELETE`| /accounts/:id/stream/watermarks |
|`GET`   |-       |`PUT`   |-       |`DELETE`| /accounts/:id/stream/webhook |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/subscriptions |
|`GET`   |`POST`  |-       |`PATCH` |`DELETE`| /accounts/:id/teamnet/routes |
|`GET`   |-       |-       |-       |-       | /accounts/:id/teamnet/routes/ip |
|`GET`   |`POST`  |-       |`PATCH` |`DELETE`| /accounts/:id/teamnet/virtual_networks |
|`GET`   |-       |-       |-       |-       | /accounts/:id/tunnels |
|`GET`   |`POST`  |-       |-       |-       | /accounts/:id/urlscanner/scan |
|`GET`   |-       |-       |-       |-       | /accounts/:id/urlscanner/scan/:id/har |
|`GET`   |-       |-       |-       |-       | /accounts/:id/urlscanner/scan/:id/screenshot |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/vectorize/indexes |
|-       |`POST`  |-       |-       |-       | /accounts/:id/vectorize/indexes/:id/insert |
|-       |`POST`  |-       |-       |-       | /accounts/:id/vectorize/indexes/:id/query |
|-       |`POST`  |-       |-       |-       | /accounts/:id/vectorize/indexes/:id/upsert |
|`GET`   |`POST`  |-       |`PATCH` |`DELETE`| /accounts/:id/warp_connector |
|`GET`   |-       |-       |-       |-       | /accounts/:id/warp_connector/:id/token |
|`GET`   |-       |`PUT`   |-       |-       | /accounts/:id/workers/account-settings |
|`GET`   |-       |-       |-       |-       | /accounts/:id/workers/deployments/by-script |
|`GET`   |-       |-       |-       |-       | /accounts/:id/workers/deployments/by-script/:id/detail |
|`GET`   |-       |`PUT`   |-       |`DELETE`| /accounts/:id/workers/dispatch/namespaces/:id/scripts |
|`GET`   |-       |`PUT`   |-       |-       | /accounts/:id/workers/dispatch/namespaces/:id/scripts/:id/content |
|`GET`   |-       |-       |`PATCH` |-       | /accounts/:id/workers/dispatch/namespaces/:id/scripts/:id/settings |
|`GET`   |-       |`PUT`   |-       |`DELETE`| /accounts/:id/workers/domains |
|`GET`   |-       |-       |-       |-       | /accounts/:id/workers/durable_objects/namespaces |
|`GET`   |-       |-       |-       |-       | /accounts/:id/workers/durable_objects/namespaces/:id/objects |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/workers/queues |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /accounts/:id/workers/queues/:id/consumers |
|`GET`   |-       |`PUT`   |-       |`DELETE`| /accounts/:id/workers/scripts |
|-       |-       |`PUT`   |-       |-       | /accounts/:id/workers/scripts/:id/content |
|`GET`   |-       |-       |-       |-       | /accounts/:id/workers/scripts/:id/content/v2 |
|`GET`   |-       |`PUT`   |-       |-       | /accounts/:id/workers/scripts/:id/schedules |
|`GET`   |-       |-       |`PATCH` |-       | /accounts/:id/workers/scripts/:id/settings |
|`GET`   |`POST`  |-       |-       |`DELETE`| /accounts/:id/workers/scripts/:id/tails |
|`GET`   |-       |`PUT`   |-       |-       | /accounts/:id/workers/scripts/:id/usage-model |
|`GET`   |-       |`PUT`   |-       |-       | /accounts/:id/workers/services/:id/environments/:id/content |
|`GET`   |-       |-       |`PATCH` |-       | /accounts/:id/workers/services/:id/environments/:id/settings |
|`GET`   |-       |`PUT`   |-       |-       | /accounts/:id/workers/subdomain |
|`GET`   |-       |-       |`PATCH` |-       | /accounts/:id/zerotrust/connectivity_settings |
|`GET`   |`POST`  |-       |-       |`DELETE`| /certificates |
|`GET`   |-       |-       |-       |-       | /ips |
|`GET`   |-       |`PUT`   |-       |`DELETE`| /memberships |
|`GET`   |-       |-       |-       |-       | /radar/annotations/outages |
|`GET`   |-       |-       |-       |-       | /radar/annotations/outages/locations |
|`GET`   |-       |-       |-       |-       | /radar/as112/summary/dnssec |
|`GET`   |-       |-       |-       |-       | /radar/as112/summary/edns |
|`GET`   |-       |-       |-       |-       | /radar/as112/summary/ip_version |
|`GET`   |-       |-       |-       |-       | /radar/as112/summary/protocol |
|`GET`   |-       |-       |-       |-       | /radar/as112/summary/query_type |
|`GET`   |-       |-       |-       |-       | /radar/as112/summary/response_codes |
|`GET`   |-       |-       |-       |-       | /radar/as112/timeseries |
|`GET`   |-       |-       |-       |-       | /radar/as112/timeseries_groups/dnssec |
|`GET`   |-       |-       |-       |-       | /radar/as112/timeseries_groups/edns |
|`GET`   |-       |-       |-       |-       | /radar/as112/timeseries_groups/ip_version |
|`GET`   |-       |-       |-       |-       | /radar/as112/timeseries_groups/protocol |
|`GET`   |-       |-       |-       |-       | /radar/as112/timeseries_groups/query_type |
|`GET`   |-       |-       |-       |-       | /radar/as112/timeseries_groups/response_codes |
|`GET`   |-       |-       |-       |-       | /radar/as112/top/locations |
|`GET`   |-       |-       |-       |-       | /radar/as112/top/locations/dnssec |
|`GET`   |-       |-       |-       |-       | /radar/as112/top/locations/edns |
|`GET`   |-       |-       |-       |-       | /radar/as112/top/locations/ip_version |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer3/summary/bitrate |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer3/summary/duration |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer3/summary/ip_version |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer3/summary/protocol |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer3/summary/vector |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer3/timeseries |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer3/timeseries_groups/bitrate |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer3/timeseries_groups/duration |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer3/timeseries_groups/industry |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer3/timeseries_groups/ip_version |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer3/timeseries_groups/protocol |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer3/timeseries_groups/vector |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer3/timeseries_groups/vertical |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer3/top/attacks |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer3/top/industry |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer3/top/locations/origin |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer3/top/locations/target |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer3/top/vertical |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer7/summary/http_method |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer7/summary/http_version |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer7/summary/ip_version |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer7/summary/managed_rules |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer7/summary/mitigation_product |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer7/timeseries |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer7/timeseries_groups/http_method |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer7/timeseries_groups/http_version |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer7/timeseries_groups/industry |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer7/timeseries_groups/ip_version |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer7/timeseries_groups/managed_rules |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer7/timeseries_groups/mitigation_product |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer7/timeseries_groups/vertical |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer7/top/ases/origin |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer7/top/attacks |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer7/top/industry |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer7/top/locations/origin |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer7/top/locations/target |
|`GET`   |-       |-       |-       |-       | /radar/attacks/layer7/top/vertical |
|`GET`   |-       |-       |-       |-       | /radar/bgp/hijacks/events |
|`GET`   |-       |-       |-       |-       | /radar/bgp/leaks/events |
|`GET`   |-       |-       |-       |-       | /radar/bgp/routes/moas |
|`GET`   |-       |-       |-       |-       | /radar/bgp/routes/pfx2as |
|`GET`   |-       |-       |-       |-       | /radar/bgp/routes/stats |
|`GET`   |-       |-       |-       |-       | /radar/bgp/timeseries |
|`GET`   |-       |-       |-       |-       | /radar/bgp/top/ases |
|`GET`   |-       |-       |-       |-       | /radar/bgp/top/ases/prefixes |
|`GET`   |-       |-       |-       |-       | /radar/bgp/top/prefixes |
|`GET`   |-       |-       |-       |-       | /radar/connection_tampering/summary |
|`GET`   |-       |-       |-       |-       | /radar/connection_tampering/timeseries_groups |
|`GET`   |-       |-       |-       |-       | /radar/datasets |
|-       |`POST`  |-       |-       |-       | /radar/datasets/download |
|`GET`   |-       |-       |-       |-       | /radar/dns/top/ases |
|`GET`   |-       |-       |-       |-       | /radar/dns/top/locations |
|`GET`   |-       |-       |-       |-       | /radar/email/security/summary/arc |
|`GET`   |-       |-       |-       |-       | /radar/email/security/summary/dkim |
|`GET`   |-       |-       |-       |-       | /radar/email/security/summary/dmarc |
|`GET`   |-       |-       |-       |-       | /radar/email/security/summary/malicious |
|`GET`   |-       |-       |-       |-       | /radar/email/security/summary/spam |
|`GET`   |-       |-       |-       |-       | /radar/email/security/summary/spf |
|`GET`   |-       |-       |-       |-       | /radar/email/security/summary/threat_category |
|`GET`   |-       |-       |-       |-       | /radar/email/security/timeseries_groups/arc |
|`GET`   |-       |-       |-       |-       | /radar/email/security/timeseries_groups/dkim |
|`GET`   |-       |-       |-       |-       | /radar/email/security/timeseries_groups/dmarc |
|`GET`   |-       |-       |-       |-       | /radar/email/security/timeseries_groups/malicious |
|`GET`   |-       |-       |-       |-       | /radar/email/security/timeseries_groups/spam |
|`GET`   |-       |-       |-       |-       | /radar/email/security/timeseries_groups/spf |
|`GET`   |-       |-       |-       |-       | /radar/email/security/timeseries_groups/threat_category |
|`GET`   |-       |-       |-       |-       | /radar/email/security/top/ases |
|`GET`   |-       |-       |-       |-       | /radar/email/security/top/ases/arc |
|`GET`   |-       |-       |-       |-       | /radar/email/security/top/ases/dkim |
|`GET`   |-       |-       |-       |-       | /radar/email/security/top/ases/dmarc |
|`GET`   |-       |-       |-       |-       | /radar/email/security/top/ases/malicious |
|`GET`   |-       |-       |-       |-       | /radar/email/security/top/ases/spam |
|`GET`   |-       |-       |-       |-       | /radar/email/security/top/ases/spf |
|`GET`   |-       |-       |-       |-       | /radar/email/security/top/locations |
|`GET`   |-       |-       |-       |-       | /radar/email/security/top/locations/arc |
|`GET`   |-       |-       |-       |-       | /radar/email/security/top/locations/dkim |
|`GET`   |-       |-       |-       |-       | /radar/email/security/top/locations/dmarc |
|`GET`   |-       |-       |-       |-       | /radar/email/security/top/locations/malicious |
|`GET`   |-       |-       |-       |-       | /radar/email/security/top/locations/spam |
|`GET`   |-       |-       |-       |-       | /radar/email/security/top/locations/spf |
|`GET`   |-       |-       |-       |-       | /radar/entities/asns |
|`GET`   |-       |-       |-       |-       | /radar/entities/asns/:id/rel |
|`GET`   |-       |-       |-       |-       | /radar/entities/asns/ip |
|`GET`   |-       |-       |-       |-       | /radar/entities/ip |
|`GET`   |-       |-       |-       |-       | /radar/entities/locations |
|`GET`   |-       |-       |-       |-       | /radar/http/summary/bot_class |
|`GET`   |-       |-       |-       |-       | /radar/http/summary/device_type |
|`GET`   |-       |-       |-       |-       | /radar/http/summary/http_protocol |
|`GET`   |-       |-       |-       |-       | /radar/http/summary/http_version |
|`GET`   |-       |-       |-       |-       | /radar/http/summary/ip_version |
|`GET`   |-       |-       |-       |-       | /radar/http/summary/os |
|`GET`   |-       |-       |-       |-       | /radar/http/summary/tls_version |
|`GET`   |-       |-       |-       |-       | /radar/http/timeseries_groups/bot_class |
|`GET`   |-       |-       |-       |-       | /radar/http/timeseries_groups/browser |
|`GET`   |-       |-       |-       |-       | /radar/http/timeseries_groups/browser_family |
|`GET`   |-       |-       |-       |-       | /radar/http/timeseries_groups/device_type |
|`GET`   |-       |-       |-       |-       | /radar/http/timeseries_groups/http_protocol |
|`GET`   |-       |-       |-       |-       | /radar/http/timeseries_groups/http_version |
|`GET`   |-       |-       |-       |-       | /radar/http/timeseries_groups/ip_version |
|`GET`   |-       |-       |-       |-       | /radar/http/timeseries_groups/os |
|`GET`   |-       |-       |-       |-       | /radar/http/timeseries_groups/tls_version |
|`GET`   |-       |-       |-       |-       | /radar/http/top/ases |
|`GET`   |-       |-       |-       |-       | /radar/http/top/ases/bot_class |
|`GET`   |-       |-       |-       |-       | /radar/http/top/ases/device_type |
|`GET`   |-       |-       |-       |-       | /radar/http/top/ases/http_protocol |
|`GET`   |-       |-       |-       |-       | /radar/http/top/ases/http_version |
|`GET`   |-       |-       |-       |-       | /radar/http/top/ases/ip_version |
|`GET`   |-       |-       |-       |-       | /radar/http/top/ases/os |
|`GET`   |-       |-       |-       |-       | /radar/http/top/ases/tls_version |
|`GET`   |-       |-       |-       |-       | /radar/http/top/browser_families |
|`GET`   |-       |-       |-       |-       | /radar/http/top/browsers |
|`GET`   |-       |-       |-       |-       | /radar/http/top/locations |
|`GET`   |-       |-       |-       |-       | /radar/http/top/locations/bot_class |
|`GET`   |-       |-       |-       |-       | /radar/http/top/locations/device_type |
|`GET`   |-       |-       |-       |-       | /radar/http/top/locations/http_protocol |
|`GET`   |-       |-       |-       |-       | /radar/http/top/locations/http_version |
|`GET`   |-       |-       |-       |-       | /radar/http/top/locations/ip_version |
|`GET`   |-       |-       |-       |-       | /radar/http/top/locations/os |
|`GET`   |-       |-       |-       |-       | /radar/http/top/locations/tls_version |
|`GET`   |-       |-       |-       |-       | /radar/netflows/timeseries |
|`GET`   |-       |-       |-       |-       | /radar/netflows/top/ases |
|`GET`   |-       |-       |-       |-       | /radar/netflows/top/locations |
|`GET`   |-       |-       |-       |-       | /radar/quality/iqi/summary |
|`GET`   |-       |-       |-       |-       | /radar/quality/iqi/timeseries_groups |
|`GET`   |-       |-       |-       |-       | /radar/quality/speed/histogram |
|`GET`   |-       |-       |-       |-       | /radar/quality/speed/summary |
|`GET`   |-       |-       |-       |-       | /radar/quality/speed/top/ases |
|`GET`   |-       |-       |-       |-       | /radar/quality/speed/top/locations |
|`GET`   |-       |-       |-       |-       | /radar/ranking/domain |
|`GET`   |-       |-       |-       |-       | /radar/ranking/timeseries_groups |
|`GET`   |-       |-       |-       |-       | /radar/ranking/top |
|`GET`   |-       |-       |-       |-       | /radar/search/global |
|`GET`   |-       |-       |-       |-       | /radar/traffic_anomalies |
|`GET`   |-       |-       |-       |-       | /radar/traffic_anomalies/locations |
|`GET`   |-       |-       |-       |-       | /radar/verified_bots/top/bots |
|`GET`   |-       |-       |-       |-       | /radar/verified_bots/top/categories |
|`GET`   |-       |-       |`PATCH` |-       | /user |
|`GET`   |-       |-       |-       |-       | /user/audit_logs |
|`GET`   |`POST`  |-       |`PATCH` |`DELETE`| /user/firewall/access_rules/rules |
|`GET`   |-       |-       |`PATCH` |-       | /user/invites |
|`GET`   |`POST`  |`PUT`   |`PATCH` |`DELETE`| /user/load_balancers/monitors |
|-       |`POST`  |-       |-       |-       | /user/load_balancers/monitors/:id/preview |
|`GET`   |-       |-       |-       |-       | /user/load_balancers/monitors/:id/references |
|`GET`   |`POST`  |`PUT`   |`PATCH` |`DELETE`| /user/load_balancers/pools |
|`GET`   |-       |-       |-       |-       | /user/load_balancers/pools/:id/health |
|-       |`POST`  |-       |-       |-       | /user/load_balancers/pools/:id/preview |
|`GET`   |-       |-       |-       |-       | /user/load_balancers/pools/:id/references |
|`GET`   |-       |-       |-       |-       | /user/load_balancers/preview |
|`GET`   |-       |-       |-       |-       | /user/load_balancing_analytics/events |
|`GET`   |-       |-       |-       |`DELETE`| /user/organizations |
|`GET`   |-       |`PUT`   |-       |`DELETE`| /user/subscriptions |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /user/tokens |
|-       |-       |`PUT`   |-       |-       | /user/tokens/:id/value |
|`GET`   |-       |-       |-       |-       | /user/tokens/permission_groups |
|`GET`   |-       |-       |-       |-       | /user/tokens/verify |
|`GET`   |`POST`  |-       |`PATCH` |`DELETE`| /zones |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /zones/:id/access/apps |
|`GET`   |`POST`  |-       |-       |`DELETE`| /zones/:id/access/apps/:id/ca |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /zones/:id/access/apps/:id/policies |
|-       |`POST`  |-       |-       |-       | /zones/:id/access/apps/:id/revoke_tokens |
|`GET`   |-       |-       |-       |-       | /zones/:id/access/apps/:id/user_policy_checks |
|`GET`   |-       |-       |-       |-       | /zones/:id/access/apps/ca |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /zones/:id/access/certificates |
|`GET`   |-       |`PUT`   |-       |-       | /zones/:id/access/certificates/settings |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /zones/:id/access/groups |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /zones/:id/access/identity_providers |
|`GET`   |`POST`  |`PUT`   |-       |-       | /zones/:id/access/organizations |
|-       |`POST`  |-       |-       |-       | /zones/:id/access/organizations/revoke_user |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /zones/:id/access/service_tokens |
|`GET`   |`POST`  |-       |-       |-       | /zones/:id/acm/total_tls |
|-       |-       |`PUT`   |-       |-       | /zones/:id/activation_check |
|`GET`   |-       |-       |-       |-       | /zones/:id/analytics/latency |
|`GET`   |-       |-       |-       |-       | /zones/:id/analytics/latency/colos |
|`GET`   |-       |`PUT`   |-       |-       | /zones/:id/api_gateway/configuration |
|`GET`   |-       |-       |-       |-       | /zones/:id/api_gateway/discovery |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/api_gateway/discovery/operations |
|`GET`   |`POST`  |-       |-       |`DELETE`| /zones/:id/api_gateway/operations |
|`GET`   |-       |`PUT`   |-       |-       | /zones/:id/api_gateway/operations/:id/schema_validation |
|-       |-       |-       |`PATCH` |-       | /zones/:id/api_gateway/operations/schema_validation |
|`GET`   |-       |-       |-       |-       | /zones/:id/api_gateway/schemas |
|`GET`   |-       |`PUT`   |`PATCH` |-       | /zones/:id/api_gateway/settings/schema_validation |
|`GET`   |`POST`  |-       |`PATCH` |`DELETE`| /zones/:id/api_gateway/user_schemas |
|`GET`   |-       |-       |-       |-       | /zones/:id/api_gateway/user_schemas/:id/operations |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/argo/smart_routing |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/argo/tiered_caching |
|`GET`   |-       |-       |-       |-       | /zones/:id/available_plans |
|`GET`   |-       |-       |-       |-       | /zones/:id/available_rate_plans |
|`GET`   |-       |`PUT`   |-       |-       | /zones/:id/bot_management |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/cache/cache_reserve |
|`GET`   |`POST`  |-       |-       |-       | /zones/:id/cache/cache_reserve_clear |
|`GET`   |-       |`PUT`   |-       |-       | /zones/:id/cache/origin_post_quantum_encryption |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/cache/regional_tiered_cache |
|`GET`   |-       |-       |`PATCH` |`DELETE`| /zones/:id/cache/tiered_cache_smart_topology_enable |
|`GET`   |-       |-       |`PATCH` |`DELETE`| /zones/:id/cache/variants |
|`GET`   |-       |`PUT`   |-       |-       | /zones/:id/certificate_authorities/hostname_associations |
|`GET`   |`POST`  |-       |`PATCH` |`DELETE`| /zones/:id/client_certificates |
|`GET`   |`POST`  |-       |`PATCH` |`DELETE`| /zones/:id/custom_certificates |
|-       |-       |`PUT`   |-       |-       | /zones/:id/custom_certificates/prioritize |
|`GET`   |`POST`  |-       |`PATCH` |`DELETE`| /zones/:id/custom_hostnames |
|`GET`   |-       |`PUT`   |-       |`DELETE`| /zones/:id/custom_hostnames/fallback_origin |
|`GET`   |-       |`PUT`   |-       |-       | /zones/:id/custom_ns |
|`GET`   |-       |`PUT`   |-       |-       | /zones/:id/custom_pages |
|`GET`   |-       |-       |-       |-       | /zones/:id/dcv_delegation/uuid |
|`GET`   |-       |-       |-       |-       | /zones/:id/dns_analytics/report |
|`GET`   |-       |-       |-       |-       | /zones/:id/dns_analytics/report/bytime |
|`GET`   |`POST`  |`PUT`   |`PATCH` |`DELETE`| /zones/:id/dns_records |
|`GET`   |-       |-       |-       |-       | /zones/:id/dns_records/export |
|-       |`POST`  |-       |-       |-       | /zones/:id/dns_records/import |
|-       |`POST`  |-       |-       |-       | /zones/:id/dns_records/scan |
|`GET`   |-       |-       |`PATCH` |`DELETE`| /zones/:id/dnssec |
|`GET`   |-       |-       |-       |-       | /zones/:id/email/routing |
|-       |`POST`  |-       |-       |-       | /zones/:id/email/routing/disable |
|`GET`   |-       |-       |-       |-       | /zones/:id/email/routing/dns |
|-       |`POST`  |-       |-       |-       | /zones/:id/email/routing/enable |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /zones/:id/email/routing/rules |
|`GET`   |-       |`PUT`   |-       |-       | /zones/:id/email/routing/rules/catch_all |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /zones/:id/filters |
|`GET`   |`POST`  |-       |`PATCH` |`DELETE`| /zones/:id/firewall/access_rules/rules |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /zones/:id/firewall/lockdowns |
|`GET`   |`POST`  |`PUT`   |`PATCH` |`DELETE`| /zones/:id/firewall/rules |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /zones/:id/firewall/ua_rules |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /zones/:id/firewall/waf/overrides |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/firewall/waf/packages |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/firewall/waf/packages/:id/groups |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/firewall/waf/packages/:id/rules |
|`GET`   |`POST`  |`PUT`   |`PATCH` |`DELETE`| /zones/:id/healthchecks |
|`GET`   |`POST`  |-       |-       |`DELETE`| /zones/:id/healthchecks/preview |
|`GET`   |`POST`  |-       |-       |`DELETE`| /zones/:id/hold |
|`GET`   |-       |`PUT`   |-       |`DELETE`| /zones/:id/hostnames/settings |
|`GET`   |`POST`  |-       |`PATCH` |`DELETE`| /zones/:id/keyless_certificates |
|`GET`   |`POST`  |`PUT`   |`PATCH` |`DELETE`| /zones/:id/load_balancers |
|`GET`   |-       |-       |-       |-       | /zones/:id/logpush/datasets/:id/fields |
|`GET`   |-       |-       |-       |-       | /zones/:id/logpush/datasets/:id/jobs |
|`GET`   |`POST`  |-       |-       |-       | /zones/:id/logpush/edge |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /zones/:id/logpush/jobs |
|-       |`POST`  |-       |-       |-       | /zones/:id/logpush/ownership |
|-       |`POST`  |-       |-       |-       | /zones/:id/logpush/ownership/validate |
|-       |`POST`  |-       |-       |-       | /zones/:id/logpush/validate/destination/exists |
|-       |`POST`  |-       |-       |-       | /zones/:id/logpush/validate/origin |
|`GET`   |`POST`  |-       |-       |-       | /zones/:id/logs/control/retention/flag |
|`GET`   |-       |-       |-       |-       | /zones/:id/logs/rayids |
|`GET`   |-       |-       |-       |-       | /zones/:id/logs/received |
|`GET`   |-       |-       |-       |-       | /zones/:id/logs/received/fields |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/managed_headers |
|`GET`   |`POST`  |-       |-       |`DELETE`| /zones/:id/origin_tls_client_auth |
|`GET`   |-       |`PUT`   |-       |-       | /zones/:id/origin_tls_client_auth/hostnames |
|`GET`   |`POST`  |-       |-       |`DELETE`| /zones/:id/origin_tls_client_auth/hostnames/certificates |
|`GET`   |-       |`PUT`   |-       |-       | /zones/:id/origin_tls_client_auth/settings |
|`GET`   |-       |`PUT`   |-       |-       | /zones/:id/page_shield |
|`GET`   |-       |-       |-       |-       | /zones/:id/page_shield/connections |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /zones/:id/page_shield/policies |
|`GET`   |-       |-       |-       |-       | /zones/:id/page_shield/scripts |
|`GET`   |`POST`  |`PUT`   |`PATCH` |`DELETE`| /zones/:id/pagerules |
|`GET`   |-       |-       |-       |-       | /zones/:id/pagerules/settings |
|-       |`POST`  |-       |-       |-       | /zones/:id/purge_cache |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /zones/:id/rate_limits |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /zones/:id/rulesets |
|-       |`POST`  |-       |`PATCH` |`DELETE`| /zones/:id/rulesets/:id/rules |
|`GET`   |-       |-       |-       |`DELETE`| /zones/:id/rulesets/:id/versions |
|`GET`   |-       |`PUT`   |-       |-       | /zones/:id/rulesets/phases/:id/entrypoint |
|`GET`   |-       |-       |-       |-       | /zones/:id/rulesets/phases/:id/entrypoint/versions |
|-       |`POST`  |-       |-       |-       | /zones/:id/secondary_dns/force_axfr |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /zones/:id/secondary_dns/incoming |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /zones/:id/secondary_dns/outgoing |
|-       |`POST`  |-       |-       |-       | /zones/:id/secondary_dns/outgoing/disable |
|-       |`POST`  |-       |-       |-       | /zones/:id/secondary_dns/outgoing/enable |
|-       |`POST`  |-       |-       |-       | /zones/:id/secondary_dns/outgoing/force_notify |
|`GET`   |-       |-       |-       |-       | /zones/:id/secondary_dns/outgoing/status |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/0rtt |
|`GET`   |-       |-       |-       |-       | /zones/:id/settings/advanced_ddos |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/always_online |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/always_use_https |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/automatic_https_rewrites |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/automatic_platform_optimization |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/brotli |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/browser_cache_ttl |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/browser_check |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/cache_level |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/challenge_ttl |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/ciphers |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/development_mode |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/early_hints |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/email_obfuscation |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/fonts |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/h2_prioritization |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/hotlink_protection |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/http2 |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/http3 |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/image_resizing |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/ip_geolocation |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/ipv6 |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/min_tls_version |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/minify |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/mirage |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/mobile_redirect |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/nel |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/opportunistic_encryption |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/opportunistic_onion |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/orange_to_orange |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/origin_error_page_pass_thru |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/origin_max_http_version |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/polish |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/prefetch_preload |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/proxy_read_timeout |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/pseudo_ipv4 |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/response_buffering |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/rocket_loader |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/security_header |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/security_level |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/server_side_exclude |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/sort_query_string_for_cache |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/ssl |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/ssl_recommender |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/tls_1_3 |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/tls_client_auth |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/true_client_ip_header |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/waf |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/webp |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/settings/websockets |
|`GET`   |-       |`PUT`   |-       |-       | /zones/:id/settings/zaraz/v2/config |
|`GET`   |-       |-       |-       |-       | /zones/:id/settings/zaraz/v2/default |
|`GET`   |-       |-       |-       |-       | /zones/:id/settings/zaraz/v2/export |
|`GET`   |-       |`PUT`   |-       |-       | /zones/:id/settings/zaraz/v2/history |
|`GET`   |-       |-       |-       |-       | /zones/:id/settings/zaraz/v2/history/configs |
|-       |`POST`  |-       |-       |-       | /zones/:id/settings/zaraz/v2/publish |
|`GET`   |-       |`PUT`   |-       |-       | /zones/:id/settings/zaraz/v2/workflow |
|`GET`   |-       |`PUT`   |-       |`DELETE`| /zones/:id/snippets |
|`GET`   |-       |-       |-       |-       | /zones/:id/snippets/:id/content |
|`GET`   |-       |`PUT`   |-       |-       | /zones/:id/snippets/snippet_rules |
|`GET`   |-       |-       |-       |-       | /zones/:id/spectrum/analytics/aggregate/current |
|`GET`   |-       |-       |-       |-       | /zones/:id/spectrum/analytics/events/bytime |
|`GET`   |-       |-       |-       |-       | /zones/:id/spectrum/analytics/events/summary |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /zones/:id/spectrum/apps |
|`GET`   |-       |-       |-       |-       | /zones/:id/speed_api/availabilities |
|`GET`   |-       |-       |-       |-       | /zones/:id/speed_api/pages |
|`GET`   |`POST`  |-       |-       |`DELETE`| /zones/:id/speed_api/pages/:id/tests |
|`GET`   |-       |-       |-       |-       | /zones/:id/speed_api/pages/:id/trend |
|`GET`   |`POST`  |-       |-       |`DELETE`| /zones/:id/speed_api/schedule |
|-       |`POST`  |-       |-       |-       | /zones/:id/ssl/analyze |
|`GET`   |-       |-       |`PATCH` |`DELETE`| /zones/:id/ssl/certificate_packs |
|-       |`POST`  |-       |-       |-       | /zones/:id/ssl/certificate_packs/order |
|`GET`   |-       |-       |-       |-       | /zones/:id/ssl/certificate_packs/quota |
|`GET`   |-       |-       |-       |-       | /zones/:id/ssl/recommendation |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/ssl/universal/settings |
|`GET`   |-       |-       |`PATCH` |-       | /zones/:id/ssl/verification |
|`GET`   |`POST`  |`PUT`   |-       |-       | /zones/:id/subscription |
|`GET`   |-       |`PUT`   |-       |-       | /zones/:id/url_normalization |
|`GET`   |`POST`  |`PUT`   |`PATCH` |`DELETE`| /zones/:id/waiting_rooms |
|`GET`   |`POST`  |`PUT`   |`PATCH` |`DELETE`| /zones/:id/waiting_rooms/:id/events |
|`GET`   |-       |-       |-       |-       | /zones/:id/waiting_rooms/:id/events/:id/details |
|`GET`   |`POST`  |`PUT`   |`PATCH` |`DELETE`| /zones/:id/waiting_rooms/:id/rules |
|`GET`   |-       |-       |-       |-       | /zones/:id/waiting_rooms/:id/status |
|-       |`POST`  |-       |-       |-       | /zones/:id/waiting_rooms/preview |
|`GET`   |-       |`PUT`   |`PATCH` |-       | /zones/:id/waiting_rooms/settings |
|`GET`   |`POST`  |-       |`PATCH` |`DELETE`| /zones/:id/web3/hostnames |
|`GET`   |-       |`PUT`   |-       |-       | /zones/:id/web3/hostnames/:id/ipfs_universal_path/content_list |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /zones/:id/web3/hostnames/:id/ipfs_universal_path/content_list/entries |
|`GET`   |`POST`  |`PUT`   |-       |`DELETE`| /zones/:id/workers/routes |

