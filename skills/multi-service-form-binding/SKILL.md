---
name: multi-service-form-binding
description: Patterns for managing complex parent-child relationships in multi-service forms with dynamic service group resolution, scoped sequential numbering, and automatic parent assignment.
---

# Multi-Service Form Binding Patterns

This skill guides the implementation of complex multi-service form sub-resources (such as Firewall rules, database credentials, Kafka topics, and routing declarations) attached to individual microservices.

---

## 1. Core Patterns

1. **Dynamic Service Group Resolution**:
   - Do not rely on hardcoded feature flags to group sub-resources.
   - Dynamically create service group containers for any entry containing a valid `serviceName`.
   - Pre-populate groups for all declared parent services while creating an orphan container (`__orphan__`) only for genuinely unassigned entries.

2. **Scoped Sequence vs. Global Array Indexing**:
   - **Display Index**: Reset rule numbers per service (`Rule #1`, `Rule #2`, `Rule #3` for Service A; `Rule #1`, `Rule #2` for Service B).
   - **Mutation Index**: Pass the underlying array index (`idx`) to update/delete mutations to ensure accurate array manipulations.

3. **Auto-Assignment on Item Creation**:
   - When adding a new item from a specific service group header, automatically set `serviceName: targetService`.
   - When adding an item from global toolbars, default to the first available service instead of an empty string.

---

## 2. Implementation Template

```typescript
// 1. Dynamic Grouping Algorithm
function groupEntriesByService<T extends { serviceName?: string }>(
  entries: T[] | undefined,
  allServiceNames: string[]
): { serviceName: string; items: { entry: T; idx: number }[] }[] {
  const list = entries || [];
  const groups: { serviceName: string; items: { entry: T; idx: number }[] }[] = [];
  const idxMap = new Map<string, number>();

  allServiceNames.forEach(name => {
    const trimmed = (name || '').trim();
    if (trimmed && !idxMap.has(trimmed)) {
      idxMap.set(trimmed, groups.length);
      groups.push({ serviceName: trimmed, items: [] });
    }
  });

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

  return groups.filter(g => g.items.length > 0 || (g.serviceName !== '' && allServiceNames.includes(g.serviceName)));
}

// 2. React Rendering with Scoped Indexing
{serviceGroups.map(group => (
  <div key={group.serviceName || '__orphan__'}>
    <h3>Service: {group.serviceName || 'ยังไม่ระบุ service'}</h3>
    {group.items.map(({ entry: item, idx: globalIdx }, scopedIdx) => (
      <div key={globalIdx} className="item-card">
        {/* Scoped badge for user display */}
        <span className="badge">Item #{scopedIdx + 1}</span>
        
        {/* Mutations target global index */}
        <button onClick={() => removeArrayField('items', globalIdx)}>ลบ</button>
      </div>
    ))}
  </div>
))}
```

---

## 3. Checklist for Implementation

- [ ] Adding a new sub-resource auto-selects the active service.
- [ ] UI displays localized sequence numbers (`Rule #1`, `Rule #2`) per group.
- [ ] Deleting an item removes the correct element from the global state array.
- [ ] Service dropdown allows reassigning an item to another service seamlessly.
