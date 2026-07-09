---
name: Verify an agent's 'needs a restart/reload' diagnosis before accepting it -- check live state directly
description: deploy-agent blamed a missing HA entity on needing an HA restart; real cause was a missing object_id in MQTT discovery causing a different auto-generated entity_id -- always verify a restart-theory diagnosis against live state first
type: feedback
---

A deploy-agent reported an HA MQTT-discovered entity as 'not yet appearing, needs HA restart or MQTT integration reload' when the real cause was a missing 'object_id' in the discovery payload — HA auto-slugs entity_id from device name + entity name when object_id is absent, producing sensor.shop_switch_shop_switch instead of the intended sensor.unifi_vision_shop_switch, so a states lookup by the expected entity_id returned 'not found' even though the entity existed under a different id.

Lesson: when an agent says 'X needs a restart/reload to take effect' for something that should be event-driven (MQTT discovery, config reload, live subscriptions), verify directly before accepting the diagnosis -- check the actual live state (grep all entities for a fuzzy match, subscribe to the raw topic through the target app's own connection) rather than trusting the restart theory. In this case, listing all HA states and grep'ing for the switch's name/model immediately revealed the real (differently-named) entity, disproving the restart theory in under a minute.
