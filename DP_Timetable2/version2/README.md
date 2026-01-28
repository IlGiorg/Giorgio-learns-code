# DP Subject Scheduler

**Automated bracket optimization for IB Diploma Programme subject scheduling**

## 🎯 What it does

This algorithm optimizes subject scheduling by:
- Minimizing student conflicts (students with 2+ subjects in the same time slot)
- Using greedy assignment + simulated annealing optimization
- Generating dynamic HTML visualization automatically

## 📊 Current Results

- **18/26 students satisfied (69.2%)**
- **8 conflicts remaining** (require manual resolution)
- 3 optimized time slots

## 🚀 How to use

### 1. Update student data

Edit the `raw_data` variable in `dp_scheduler_english.py` with your student choices:

```python
raw_data = """Computer Science;Physics;Business;Computer Science;Spanish;Business;..."""
```

Format: Each student's 3 subjects separated by semicolons

### 2. Run the optimizer

```bash
python dp_scheduler_english.py
```

### 3. View results

The script will:
1. Print optimization results to console
2. Generate `dp_schedule_results.html` with interactive visualization

Open the HTML file in any browser to see:
- 📊 Success statistics
- 🗓️ Optimized schedule with all subjects
- ⚠️ List of students with conflicts
- 💡 Helpful notes and recommendations

## 🔧 How it works

1. **Greedy Assignment**: Places subjects into slots to minimize conflicts
2. **Simulated Annealing**: Fine-tunes the solution by trying random swaps
3. **Conflict Detection**: Identifies students with scheduling conflicts
4. **HTML Generation**: Creates dynamic visualization with real data

## 📝 Subject Categories

- **Sciences**: Computer Science, Physics, Biology, Chemistry, ESS
- **Humanities**: Business, Economics, Politics, History, Geography, GeoPolitics
- **Arts**: Visual Arts, Music
- **Languages**: Spanish, French
- **Online**: Psychology (Timetabled Online)

## ⚙️ Customization

You can adjust:
- `iterations` parameter in simulated annealing (default: 5000)
- `temperature` parameter for optimization aggressiveness
- Subject categories in the category dictionaries

## 📋 Requirements

- Python 3.6+
- NumPy (optional, for simulated annealing)

If NumPy is not available, the script will use greedy algorithm only.

## 💡 Tips

- **Psychology (Online)** can potentially be scheduled flexibly since it's online
- Students with invalid combinations (not 2+1 or 1+2) are flagged automatically
- The algorithm may not achieve 100% satisfaction - manual adjustments may be needed for remaining conflicts
- Run the script multiple times - simulated annealing may find different solutions

## 🎨 Example Output

```
📚 SLOT 1: Biology, ESS, Physics
📚 SLOT 2: Computer Science, Chemistry, Politics, History, GeoPolitics  
📚 SLOT 3: Business, Spanish, French, Psychology (Online), Visual Arts

✅ 18/26 students satisfied (69.2%)
❌ 8 conflicts remaining
```

---

**Made with ❤️ for better student scheduling**
