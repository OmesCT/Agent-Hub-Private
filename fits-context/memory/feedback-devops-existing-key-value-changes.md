---
name: feedback-devops-existing-key-value-changes
description: "Changing the value of a config key that already exists in the OCP manifest (appsettings.json, .env.example, Dockerfile ENV) does not reach the pod; DevOps must change it in Vault, so tell them"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b51447ab-922e-401e-ac78-e04468240da4
  modified: 2026-10-05T06:58:16.708Z
---

DevOps told the user on 2026-10-05 (relayed): "ถ้ามีแก้ค่า value ที่ appsetting แต่ key เดิมที่มีอยู่แล้ว บอกพี่นะ มันจะไม่ได้ ต้องมาแก้ใน vault เอา". When a change in this repo alters the value of a key that already exists in the generated manifest (ConfigMap or Secret, values from Vault), the new value never reaches the pod; DevOps has to change it in Vault and re-run CD.

**Why:** the pod environment is the image ENV overridden by the ConfigMap/Secret, so every key listed in `fits_manifest/configuration/dev/int/{configmap,secret}/fits-api.yml` wins over `appsettings.json`, `.env.example` and Dockerfile ENV (checked in a container: an empty runtime value overrides an image ENV, issue #150). Seen with `Database__ApplyMigrations` (issue #152): the Secret held `false` whatever `appsettings.json` says. A running pod also reads Secret/ConfigMap values only at container start.

**How to apply:** whenever I change `appsettings.json`, `.env.example` or a Dockerfile `ENV`, state explicitly whether the key already exists in the manifest; if it does, give the user the exact key and new value to hand to DevOps ("แก้ใน Vault") instead of promising the change works. Keys known to exist (manifest 1.0.28/1.0.29): ConfigMap `Authentication__Aaa__Authority`, `Authentication__Authority`, `Authentication__Audience`, `Authentication__Oidc__Authority`, `Authentication__Oidc__ClientId`, `Authentication__RoleMapping__DeptHeadGroupPrefix`, `Authentication__LdapFallback__Server`, `__ServiceUser`, `__BaseDn`; Secret (per docs/OPENSHIFT_GITOPS.md) `ConnectionStrings__BudgetDb`, `Database__ApplyMigrations`, `Database__LockTimeoutMilliseconds`. The authoritative list is the two manifest files, which the user's GitLab account cannot read. A key that is not in the manifest (`ASPNETCORE_ENVIRONMENT` in alpha03) can use an image default, but the generator reads `.env.example`, so a later CD run could add it. Related: [[project-jenkins-awx-pipeline-rules]], [[feedback-dev-ohm-issue-first-no-mr]].
