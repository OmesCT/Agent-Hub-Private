---
name: sticky-stepper-validation
description: Design and implementation patterns for sticky multi-step form navigation, real-time validity status indicators, and persistent top/bottom validation docking.
---

# Sticky Stepper Navigation & Dual Validation Docking

This skill defines the UX and frontend architecture for multi-step enterprise onboarding forms where long scrolling requires persistent navigation and accessible validation triggers.

---

## 1. Architectural Components

1. **Sticky Segmented Stepper Header**:
   - Anchored at `position: sticky; top: 0; z-index: 100;`.
   - Tracks current active step, completion status, and field validity per tab.
   - Status indicators:
     - `Active`: Highlighted accent border + subtle blue background.
     - `Valid`: Clean green checkmark glyph (`✓`).
     - `Error`: Subtle amber or rose warning glyph (`!`).

2. **Top-Level Format Checking Trigger**:
   - Embedded directly in the sticky navigation bar (`.btn-stepper-check-format`).
   - Allows users to run format checks immediately at any point in tall forms without scrolling to the bottom.

3. **Bottom Validation Dock**:
   - Dedicated validation summary at the foot of each form tab (`.tab-validation-footer`).
   - Displays clear contextual status (e.g. "ทุกฟิลด์ถูกต้องครบถ้วน" vs. "พบ X จุดที่ต้องแก้ไข").
   - Includes primary Next / Submit CTA buttons.

---

## 2. CSS Specification

```css
.onboarding-stepper-sticky-wrapper {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--bg-card);
  border-bottom: 1px solid var(--border-color);
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
}

.tab-validation-footer {
  margin-top: 2rem;
  padding: 1.25rem 1.5rem;
  background: var(--surface-subtle);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}
```

---

## 3. Checklist for Deep Forms

- [ ] Sticky stepper tracks active tab smoothly on scroll.
- [ ] Format check can be initiated from both top sticky header and bottom dock.
- [ ] Invalid tab badges update immediately when validation errors occur.
- [ ] Clicking an invalid tab navigates directly to the target tab.
