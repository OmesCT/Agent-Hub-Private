---
name: calm-form-ergonomics
description: Standard patterns and principles for refactoring dense enterprise forms: eliminating horizontal scroll, multi-tier card layouts, per-service scoped numbering, auto-assignment, and persistent validation docking.
---

# Calm Form Ergonomics: Dense Enterprise Form Patterns

This skill provides architectural patterns, layout strategies, and UX rules for building and refactoring complex enterprise forms (such as network security rules, database provisioning, storage matrices, and routing declarations) to ensure maximum readability, zero horizontal scroll, and clear data entry ergonomics.

---

## 1. Core Principles

1. **Eliminate Horizontal Scroll (`overflow-x`)**:
   - Spreadsheets with 10+ columns force horizontal scrolling, truncating long strings (IPs, CIDRs, hostnames, timestamps) and degrading UX.
   - Replace wide spreadsheet tables with structured, responsive Form Cards or proportional grid layouts (100% container width).

2. **Per-Service Isolation & Dynamic Scoped Numbering**:
   - In microservice workflows, group entries by their associated `serviceName`.
   - Number rules locally per service (`Rule #1`, `Rule #2`, ...) rather than using global array indices.
   - Automatically assign the active service when adding new items instead of leaving entries unassigned.

3. **Multi-Tier Semantic Grouping**:
   - Group related fields logically (e.g. Source attributes, Destination & Protocol attributes, Schedule & Purpose).
   - Use dedicated form columns (3 columns on desktop, 1 column on mobile) with full-width inputs to prevent text truncation.

4. **Persistent Navigation & Live Format Checking**:
   - Use sticky steppers that track progress across deep form sections.
   - Provide an accessible "Check Format" action in the sticky header and validation dock at the bottom of active tabs.

5. **Strict Visual Calmness**:
   - Avoid aggressive spreadsheet alert colors. Use subtle neutral borders, calm background tints, and precise status badges (`badge-success`, `badge-danger`).
   - Strictly avoid emojis or decorative stickers in UI labels, badges, or error messages.

---

## 2. Component Implementation Patterns

### Pattern A: Service Group Resolution & Isolation

```typescript
function groupEntriesByService<T extends { serviceName?: string }>(
  entries: T[] | undefined,
  relevantServices: string[]
): { serviceName: string; items: { entry: T; idx: number }[] }[] {
  const list = entries || [];
  const groups: { serviceName: string; items: { entry: T; idx: number }[] }[] = [];
  const idxMap = new Map<string, number>();

  // Pre-seed known service groups
  relevantServices.forEach(name => {
    const trimmed = (name || '').trim();
    if (trimmed && !idxMap.has(trimmed)) {
      idxMap.set(trimmed, groups.length);
      groups.push({ serviceName: trimmed, items: [] });
    }
  });

  // Assign items to matching group or create dynamically
  list.forEach((entry, idx) => {
    const sn = (entry.serviceName || '').trim();
    if (sn) {
      if (!idxMap.has(sn)) {
        idxMap.set(sn, groups.length);
        groups.push({ serviceName: sn, items: [] });
      }
      const gi = idxMap.get(sn)!;
      groups[gi].items.push({ entry, idx });
    } else {
      if (!idxMap.has('__orphan__')) {
        idxMap.set('__orphan__', groups.length);
        groups.push({ serviceName: '', items: [] });
      }
      const gi = idxMap.get('__orphan__')!;
      groups[gi].items.push({ entry, idx });
    }
  });

  return groups.filter(g => g.items.length > 0 || (g.serviceName !== '' && relevantServices.includes(g.serviceName)));
}
```

### Pattern B: Responsive Form Card Architecture

```tsx
<div className="firewall-rules-container">
  {serviceGroups.map(group => (
    <div key={group.serviceName || '__orphan__'} className="firewall-service-group">
      <div className="firewall-service-group-header">
        <div className="firewall-service-group-title">
          <span className="firewall-service-name">
            Service: <strong>{group.serviceName || 'ยังไม่ระบุ service'}</strong>
          </span>
          <span className="firewall-service-count">{group.items.length} รายการ</span>
        </div>
        <button
          type="button"
          className="btn btn-secondary btn-sm"
          onClick={() => handleAddRule(group.serviceName)}
        >
          + เพิ่ม Rule ให้กับ {group.serviceName || 'Service นี้'}
        </button>
      </div>

      <div className="firewall-rule-cards-list">
        {group.items.map(({ entry: item, idx: globalIdx }, ruleIdx) => (
          <div key={globalIdx} className="firewall-rule-card">
            {/* Header: Scoped Rule #, Service Selector, Action, Environment, Delete */}
            <div className="firewall-rule-card-header">
              <div className="firewall-rule-card-header-left">
                <span className="firewall-rule-badge">Rule #{ruleIdx + 1}</span>
                <span className={`badge ${item.action === 'Deny' ? 'badge-danger' : 'badge-success'}`}>
                  {item.action || 'Allow'}
                </span>
              </div>
              <div className="firewall-rule-card-header-right">
                <button
                  type="button"
                  className="btn-row-delete"
                  onClick={() => removeArrayField('items', globalIdx)}
                  aria-label="ลบ"
                >
                  ลบ
                </button>
              </div>
            </div>

            {/* Body Grid: 3 Logical Columns */}
            <div className="firewall-rule-card-grid">
              <div className="firewall-rule-col">
                <span className="firewall-col-title">1. ต้นทาง (Source)</span>
                {/* Full-width inputs */}
              </div>
              <div className="firewall-rule-col">
                <span className="firewall-col-title">2. ปลายทาง (Destination & Port)</span>
                {/* Full-width inputs + inline errors */}
              </div>
              <div className="firewall-rule-col">
                <span className="firewall-col-title">3. ระยะเวลาใช้งาน (Schedule)</span>
                {/* Datetime inputs + quick fill actions */}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  ))}
</div>
```

---

## 3. Checklist for Enterprise Form Refactoring

- [ ] All tables with more than 6 columns converted to proportional widths or responsive cards.
- [ ] No explicit `min-width` on tables exceeding standard viewport width.
- [ ] Grouped headers count items correctly and allow targeted `+ Add` actions per group.
- [ ] Rule index labels reset per group (`Rule #1`, `Rule #2`).
- [ ] Array mutation handlers preserve global array indices.
- [ ] Field errors render directly below target inputs without breaking grid alignment.
- [ ] Sticky stepper navigation provides one-click validation trigger.
- [ ] Zero emojis used in labels, status indicators, or error messages.
