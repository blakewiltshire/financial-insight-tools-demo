# 📄 UX Components — Timeframe Handling Canonical Design

---

## 🧠 System Governance Rule: Timeframe Selector and Slicing Logic

The **Financial Insight Tools Economic Exploration Suite** applies a strict,
frequency-neutral framework for handling timeframes across all modules.

This is governed through the components located in:

- `timeframe_selector.py` (User Interface Logic)
- `timeframe_slicer.py` (Dataframe Row Slicing Logic)

---

### 🔧 Timeframe Selector Interface

The user-facing selector always presents period-agnostic labels:

| Label | Slice Applied |
|---|---|
| 📉 Latest | `df.tail(1)` |
| 📊 Last 3 Periods | `df.tail(3)` |
| 📊 Last 6 Periods | `df.tail(6)` |
| 📈 Last 12 Periods | `df.tail(12)` |
| 🗂 Full History | Full Dataset |

- No references to calendar time (months/quarters/years) are embedded.
- The system remains fully compatible across quarterly, monthly, weekly, or mixed datasets.
- Slicing is row-count based, fully agnostic to the underlying data frequency.

---

### 🔒 Macro Signal Stability

All downstream components — including:

- Macro Signal Summaries
- AI Bundle Exports
- DSS Scoring Systems
- Insight Panels
- Macro Interaction Tools

— operate on the `df_primary_slice` dataframe derived from this slicing rule.

- If insufficient rows exist, defensive logic returns `"Insufficient Data"` gracefully without system failure.
- Bias scoring remains structurally intact across all themes, countries, and datasets.

---

### ⚙ Data Pipeline Canonical Flow

1️⃣ **Dataset Load (Full Historical Cleaned DataFrame)**
> `df_primary`

2️⃣ **Timeframe Selection Applied via UX Components**
> `df_primary_slice = slice_data_by_timeframe(df_primary, selected_timeframe)`

3️⃣ **Signal Functions Execute on Sliced Dataset**

4️⃣ **Macro Signal Summary + AI Export Build**

---

### 🔬 Governance Benefits

- 🔐 Modular and fully deterministic system behavior
- 🔐 No calendar-based recalibrations required per country or dataset
- 🔐 Enables multi-frequency, mixed-sample datasets across themes
- 🔐 Compatible with real-time streaming augmentation in future system phases

---

### 🧭 Forward Expansion Path

If calendar-based slicing (e.g., "last 12 months") is desired in future development stages:

- This will be introduced via a controlled upgrade to `timeframe_slicer.py`.
- Dataset indexes must carry valid `datetime` fields to allow date-filter slicing.
- Signal function architecture requires no changes — receives pre-filtered dataframes as now.

---

✅ **This logic is formally locked as a Canonical Platinum System Rule.**
