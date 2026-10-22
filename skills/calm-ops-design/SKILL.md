---
name: calm-ops-design
description: Enterprise UI/UX design standards for internal tools and operations consoles with strict no-emoji enforcement, purposeful typography, and a calm status color system.
---

# Calm Operations Design Standard

This skill establishes visual design, typography, and color palette standards for enterprise internal consoles and operations platforms.

---

## 1. Absolute No-Emoji Policy

1. **Strict Exclusion**:
   - Zero emojis, emoticons, or decorative stickers in UI text, status badges, modal titles, commit messages, code comments, or documentation.
   - Use plain, precise technical text or standard unicode geometric glyphs (e.g. `✓` for valid, `!` for alert, `+` for add, `-` for remove, `→` for transition).

2. **Technical Labeling**:
   - Replace playful icons with descriptive typography (e.g. use `DEV Workspace`, `Service: payment-gateway`, `Status: Active`).

---

## 2. Calm Operations Color Palette

Enterprise platforms should avoid bright, saturated warning colors across regular forms. Use calm, high-contrast tokens:

- **Primary Actions**: Deep Blue / Calm Navy (`#1d4ed8` or `#0284c7`) with subtle border.
- **Success / Valid**: Forest Slate / Deep Emerald (`#15803d` / `#166534`, background `#f0fdf4`, border `#bbf7d0`).
- **Warning / Unsaved**: Warm Ochre / Subtle Amber (`#b45309`, background `#fffbeb`, border `#fde68a`).
- **Danger / Delete**: Deep Rose / Crimson Slate (`#b91c1c`, background `#fef2f2`, border `#fecaca`).
- **Surface Neutrals**: Neutral Slate (`#f8fafc`, `#f1f5f9`, border `#e2e8f0`).

---

## 3. Button Hierarchy Tokens

```css
/* Standardized Action Buttons */
.btn-header-ghost {
  color: var(--text-muted);
  background: transparent;
  border: 1px solid var(--border-color);
}

.btn-header-save {
  color: #1d4ed8;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
}

.btn-header-submit {
  color: #ffffff;
  background: #1d4ed8;
  border: 1px solid #1e40af;
}

.btn-header-danger {
  color: #b91c1c;
  background: #fef2f2;
  border: 1px solid #fecaca;
}
```

---

## 4. Checklist for Code Reviews

- [ ] Zero emoji characters found via regex search `[\u{1F300}-\u{1FAFF}]`.
- [ ] Status indicators use clear text labels with semantic CSS classes.
- [ ] Backgrounds and borders maintain accessible contrast ratios (WCAG AA).
- [ ] No fluorescent or harsh warning yellows across persistent form headers.
