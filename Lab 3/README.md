# Beyond the Numbers: Benchmarking Ghana's Economic Journey

## What I Built

I created an economic analysis pipeline that connects to the World Bank API to investigate Ghana's economic performance from 2000-2023. But here's the thing I learned: **numbers without context can tell you whatever story you want to hear**.

My goal wasn't just to show Ghana's GDP going up (spoiler: it does). It was to figure out what that *actually means* by comparing Ghana to similar countries and the world average. A line trending upward looks amazing—until you realize everyone else's line is going up even faster.

The end result was this econcomic dashboard showcasing the development of Ghana's economy
<img width="799" height="440" alt="Screenshot 2026-01-23 at 4 37 56 PM" src="https://github.com/user-attachments/assets/5530e42e-8b2e-4c10-8660-cdbd6232a43e" />

This project taught me to always ask: "Compared to what?"

---

## How I Built It

### Step 1: Getting My Hands Dirty with Real Data

I manually coded the entire data pipeline—no shortcuts. Here's what that looked like:

**Connecting to the World Bank API**
- Used `wbgapi` to pull economic data for Ghana, Lower Middle Income countries, and the world average
- Grabbed 12 key indicators: GDP, inflation, unemployment, trade, fiscal data—the works
- Set up automatic data retrieval so I could update the analysis anytime

**Wrestling with MultiIndex DataFrames**
This was honestly the hardest part. The World Bank API returns data in this wild MultiIndex format that I had to:
- Transpose from wide to long format (manually, because I needed to understand what was happening)
- Clean up messy year labels (removing "YR" prefixes)
- Rename cryptic codes like "NY.GDP.PCAP.KD" to human-readable names like "GDP_Per_Capita_Const"
- Extract Ghana's data into its own DataFrame for detailed calculations

**Creating New Economic Metrics**
I calculated four additional indicators to dig deeper:
1. **Natural Rate of Unemployment**: A 5-year moving average to smooth out the noise
2. **Labor Productivity**: How much each worker produces (GDP ÷ Labor Force)
3. **Net Capital Outflow**: Are we exporting more than importing?
4. **Budget Balance**: Is the government spending more than it's taking in?

### Step 2: Building the Story Through Visuals

**The Narrow View (The Trap)**
First, I plotted just Ghana's GDP per capita. It looked impressive! The line went up consistently. Success, right?

**The Full Picture (The Reality Check)**
Then I added the Lower Middle Income average and World average to the same chart. Suddenly, Ghana's "impressive" growth didn't look so impressive anymore. We were growing—but falling behind our peers.

That moment hit me hard. It's not enough to grow; you have to grow *faster than your competition*.

**Six Lenses on Ghana's Economy**
I created visualizations for:
- **Wealth & Growth**: How big is our economy vs. how well are people actually living?
- **Labor Market**: Who's working, who's not, and why?
- **Inflation**: Is our currency stable or are prices going crazy?
- **Savings vs. Investment**: Can we fund our own growth, or do we need foreign money?
- **Trade**: Are we exporting our way to prosperity or importing our way to debt?
- **Fiscal Health**: Is the government spending responsibly?

### Step 3: Learning What NOT to Do

I deliberately created two misleading charts to understand how people manipulate data:

**"The Ugly" - The Truncated Axis Trick**
I made a bar chart comparing Ghana to the Lower Middle Income average, but started the Y-axis at $4,000 instead of zero. Visually, Ghana looked tiny compared to peers—way more dramatic than reality.

**Lesson learned**: Always check if the axis starts at zero. If it doesn't, ask why.

**"The Bad" - The Meaningless Pie Chart**
I used a pie chart to show GDP per capita. This is nonsense. Pie charts show parts of a whole—GDP per capita isn't a "share" of anything.

**Lesson learned**: Chart type matters. Use the wrong one, and you're either incompetent or trying to mislead someone.

These weren't mistakes—I made them on purpose to train myself to spot when others do it (intentionally or not).

### Step 4: Bringing It All Together

After building all the pieces manually, I used AI to help me create a comprehensive 2×3 executive dashboard. Think of it like this: I learned to build the engine by hand, then used power tools to assemble the car.

The dashboard shows Ghana's complete economic picture at a glance—growth, stability, trade, fiscal health, all on one screen with a professional dark theme.

---

## What I Discovered

### The Benchmarking Reality Check

Ghana's GDP per capita grew from about $4,200 in 2000 to $4,600 in 2023. In isolation, that's progress.

But here's the uncomfortable truth:
- **Lower Middle Income average** jumped from ~$7,000 to ~$11,000 (57% growth)
- **World average** rose from ~$7,500 to ~$11,500 (53% growth)
- **Ghana's growth**: Only ~9.5% over 23 years

We didn't just grow slower—we fell *further behind*. That's the gap that matters.

### The Investment Puzzle

Ghana consistently invests more than we save domestically. That means we rely on foreign capital to fund our growth. It's not necessarily bad, but it creates dependency and vulnerability to global capital flows.

### The Fiscal Challenge

Government spending regularly exceeds tax revenue. We're running structural deficits, which limits our ability to respond to crises or invest in long-term development.

### The Labor Market Story

Unemployment is volatile with no clear improvement trend. Productivity is growing, but slowly. We're putting in the work, but not seeing proportional returns.

---

## Why This Matters to Me

This project changed how I look at economic data. I used to think "line go up = good." Now I know that's only half the story.

As someone looking to work in data analysis and economics, I need to:
- **Always ask for context**: Compared to what? Relative to when?
- **Question the visualization**: Is this chart designed to inform or persuade?
- **Think critically**: What story is the data *actually* telling vs. what someone *wants* it to tell?

This mindset applies beyond economics. Whether I'm analyzing user behavior, financial performance, or machine learning model results—context and comparison are everything.

---

## Technical Skills I Developed

- **API Integration**: Automated data pipelines from World Bank
- **Advanced Pandas**: MultiIndex manipulation, pivoting, cross-sections, rolling windows
- **Data Visualization**: Matplotlib, Seaborn, subplot composition, styling
- **Economic Analysis**: Comparative benchmarking, derived metric calculation
- **Critical Thinking**: Identifying misleading visualizations and data manipulation
- **Strategic AI Use**: Manual mastery first, automation second

---

## What's Next: Interactive Dashboard

I'm currently building an **interactive Streamlit web app** to make this analysis accessible to anyone—no Python required.

**Planned Features:**
- **Choose your country**: Select Ghana or any other developing nation
- **Pick your benchmarks**: Compare to regional groups, income levels, or custom peer sets
- **Adjust the timeline**: Slider to focus on specific periods
- **Drill down**: Click any indicator for detailed analysis
- **Live data**: Automatically updates from World Bank API
- **Share insights**: Export charts and download data tables
- **Mobile-friendly**: Access on any device

**Why Streamlit?**
I want policymakers, investors, and students to explore this data without needing to code. An interactive dashboard democratizes economic analysis and turns my project from a school assignment into a practical tool for decision-makers.

**Current Status:**
Static analysis is complete. I'm now building the web interface and planning deployment on Streamlit Cloud for public access. The goal is to have a live, shareable link I can include in my portfolio.

---

## The Bigger Picture

This project represents my approach to data science: understand the fundamentals deeply, build things manually first, then scale with tools and automation. 

I didn't just learn to fetch data and make charts. I learned to think critically about what data means, how it can mislead, and how to tell honest stories with numbers.

That's the skill I want to bring to any team I join: the ability to find truth in data, communicate it clearly, and build tools that help others do the same.
