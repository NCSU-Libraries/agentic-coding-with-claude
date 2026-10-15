// Scenes for tools/record-tour.mjs: the study-room activity, step by step.
// Words in the terminal follow instructor/rehearsals/study-rooms-run.md, shortened to fit. Pages come from
// tools/tour/pages/ (rehearsal output). Keep prompts identical to the activity page and the slides.
export default ({ S, js, sleep, moveTo, hoverText, evaluate }) => {
  const type = async (text, delay = 22) => { await S(`await stage.term.type(${js(text)}, ${delay})`); await sleep(350); await S('await stage.term.submit()'); };
  const shell = async (text) => { await S(`await stage.term.type(${js(text)}, 30)`); await sleep(300); await S(`await stage.term.submit('shell')`); };
  const lines = (items, gap = 420) => S(`await stage.term.lines(${js(items)}, ${gap})`);
  const cap = (t) => S(`stage.caption(${js(t)})`);
  const step = (t) => S(`stage.step(${js(t)})`);
  const mode = (m) => S(`stage.term.mode(${js(m)})`);
  const layout = (l) => S(`stage.layout(${js(l)})`);
  // zoom: how far the page is scaled to fit the browser frame (wide frame ~0.9, half-width frame ~0.55)
  const page = (file, label = 'study-rooms/' + file, zoom = 0.9) =>
    S(`await stage.browser.load(${js('pages/' + file)}, ${js('file:///Users/you/Desktop/' + label)}, ${zoom})`);
  const cursor = (on) => S(`document.body.classList.toggle('carded', ${!on})`);
  const box = (html) => S(`stage.term.box(${js(html)})`);
  const opts = (q, options, sel) => box(`<div class="q">${q}</div>` + options.map((o, i) => `<div class="opt${i === sel ? ' sel' : ''}">${o}</div>`).join(''));

  return [
    ['intro', async () => {
      await cursor(false);
      await S(`stage.card('Agentic Coding with Claude', 'From a messy spreadsheet to a dashboard you can trust', { points: ['Read', 'Plan', 'Act', 'Check'], instant: true })`);
      await sleep(3600);
      await S('stage.card(null)');
      await sleep(700);
    }],
    ['install', async () => {
      await step('Set up');
      await S(`stage.term.title('Terminal')`);
      await cap('Install Claude Code with one line');
      await shell('curl -fsSL https://claude.ai/install.sh | bash');
      await lines([['dim', 'No progress bar: wait for the prompt to come back.']], 900);
      await cap('Open a new terminal, and check it worked');
      await shell('claude --version');
      await lines([['', '2.1.299 (Claude Code)']], 1600);
    }],
    ['start', async () => {
      await cap('Start it inside the starter folder');
      await shell('cd ~/Desktop/study-rooms');
      await shell('claude');
      await sleep(500);
      await S('stage.term.clear()');
      await S(`stage.term.add('<div class="welcome"><b>✻</b> Welcome to <b>Claude Code</b><br><span style="color:#999">~/Desktop/study-rooms</span></div>', '')`);
      await sleep(500);
      await opts('Do you trust the files in this folder?', ['Yes, I trust this folder', 'No, exit'], 0);
      await sleep(1800);
      await mode('auto');
      await sleep(600);
    }],
    ['read', async () => {
      await step('1 · Read');
      await cap('Ask what’s there before anything else');
      await type("What's in this folder? Give me a quick summary of the data. Don't change anything yet.");
      await lines([
        ['tool', '<b>Read</b>(README.md)'], ['res', 'Read 32 lines'],
        ['tool', '<b>Bash</b>(wc -l room_bookings.csv)'], ['res', '10280 room_bookings.csv'],
        ['tool', '<b>Bash</b>(cut -d, -f1 room_bookings.csv | sort | uniq -d | wc -l)'], ['res', '349'],
      ], 520);
      await cap('It opens the files itself');
      await lines([
        ['say', '10,279 rows, but only <b>9,930 real bookings</b>: 349 rows appear twice.'],
        ['say', '213 rows say <b>Rm 204</b> instead of <b>Room 204</b>, all in 2024.'],
        ['say', 'Tell me what you want built, and whether to fix those first.'],
      ], 900);
      await cap('…and finds real problems in the data');
      await sleep(2200);
    }],
    ['note', async () => {
      await cap('Your supervisor’s rule. Claude can’t see it.');
      await S(`stage.note('<span class="from">From your supervisor</span>Everything we report uses the <b>fiscal year, July 1 to June 30</b>. FY2026 = July 2025 to June 2026.')`);
      await sleep(3200);
      await cap('The prompt won’t mention it. Will Claude ask, or assume?');
      await sleep(3000);
      await S('stage.note(null)');
    }],
    ['plan', async () => {
      await step('2 · Plan');
      await cap('Ask for a plan before anything gets built');
      await type('/plan Build a one-page dashboard, dashboard.html, for my supervisor: total bookings per year, the busiest days and hours, and the most popular rooms. Make it a single file I can open by double-clicking.', 14);
      await mode('plan');
      await lines([['tool', '<b>Bash</b>(awk -F, … room_bookings.csv | sort | uniq -c)'], ['res', '2024 3107 · 2025 3696 · 2026 3127']], 600);
      await opts('“Per year”: calendar years? The data stops on Sep 30, 2026.', ['Calendar years, 2026 marked Jan–Sep  (default)', 'Type something else'], 0);
      await cap('It asks, but its default is calendar years');
      await sleep(3000);
      await cap('You know the rule. Catch it now, before any code exists.');
      await type('We report by fiscal year: July 1 to June 30, named for the year it ends (FY2026 is July 2025 to June 2026). Use fiscal years.', 16);
      await lines([['say', 'Updated: bookings per <b>fiscal year</b>. FY2025 and FY2026 are complete; FY2024 and FY2027 are partial and labelled so.']], 900);
      await opts('Would you like to proceed?', ['1. Yes, and use auto mode', '2. Yes, manually approve edits', '3. No, keep planning'], 1);
      await sleep(2600);
    }],
    ['act', async () => {
      await step('3 · Act');
      await mode('manual');
      await cap('Approve the first edits and read them');
      await lines([['tool', '<b>Write</b>(dashboard.html)'], ['res', 'Wrote the page: layout, cleaning rules, charts']], 900);
      await cap('Then Shift+Tab to auto mode, and let it build');
      await sleep(900);
      await mode('auto');
      await lines([
        ['tool', '<b>Bash</b>(cat room_bookings.csv >> dashboard.html)'], ['res', 'Data pasted in, not retyped'],
        ['tool', '<b>Bash</b>(cksum … embedded rows vs room_bookings.csv)'], ['res', 'Identical'],
        ['say', 'Done. Open dashboard.html: FY2026 should read <b>4,351</b> bookings.'],
      ], 700);
      await sleep(1200);
    }],
    ['dashboard', async () => {
      await layout('browser');
      await step('3 · Act');
      await page('dashboard.html');
      await cursor(true);
      await cap('The real result, from a rehearsal run');
      await sleep(1600);
      await hoverText('FY2026', 900);
      await sleep(1200);
      await S('await stage.browser.scroll(520, 1600)');
      await sleep(1400);
      await S('await stage.browser.scroll(1100, 1600)');
      await sleep(1600);
      await S('await stage.browser.scroll(0, 1200)');
    }],
    ['check', async () => {
      await step('4 · Check');
      await cap('Check one number against the official answer');
      await S(`stage.answer('Official FY2026 bookings', '4,351')`);
      await hoverText('4,351', 900);
      await sleep(2800);
      await S('stage.answer(null)');
      await cursor(false);
      await layout('split');
      await cap('Then make Claude prove it with /goal');
      await type('/goal dashboard.html shows FY2026 = 4,351 bookings, the official count. If it doesn\'t, explain why before changing anything. Prove the final number by counting the CSV yourself, and don\'t hard-code it. Stop after 5 turns.', 10);
      await lines([
        ['goal', '◎ /goal active'],
        ['tool', '<b>Bash</b>(cut -d, -f1,2 room_bookings.csv | … 2025-07-01 to 2026-06-30 | sort -u | wc -l)'], ['res', '4351'],
        ['say', 'Goal met: the page shows <b>4,351</b>, counted when it opens, not typed in.'],
        ['say', 'Counting rows instead gives 4,513: 162 rows repeat an ID already counted.'],
        ['goal', '◎ Goal met'],
      ], 800);
      await sleep(1800);
    }],
    ['remember', async () => {
      await step('5 · Remember');
      await layout('term');
      await cap('Write down what it can’t know');
      await type('Add our reporting rules to CLAUDE.md: we use fiscal years (July 1 to June 30, named for the year they end), and each booking_id counts once.', 14);
      await lines([['tool', '<b>Write</b>(CLAUDE.md)']], 600);
      await S(`stage.file('CLAUDE.md', ${js(await evaluate("fetch('pages/CLAUDE.md').then(r => r.text())"))})`);
      await sleep(3800);
      await S('stage.file(null)');
      await cap('After /clear, a fresh conversation still knows the rule');
      await S('stage.term.clear()');
      await type('/clear', 30);
      await type('Which fiscal year had the most bookings, and how much did it grow over the year before?', 18);
      await lines([['say', '<b>FY2026</b>: 4,351 bookings, up <b>40%</b> from FY2025 (3,109).']], 900);
      await sleep(2200);
    }],
    ['skill', async () => {
      await step('6 · Skill');
      await layout('split');
      await page('dashboard.html', 'study-rooms/dashboard.html', 0.55);
      await cap('Turn your house style into a skill');
      await type('Create a skill called house-style that gives any web page we make the NC State look: Wolfpack Red #CC0000 for highlights, dark gray text on white, Arial or Helvetica, a red header bar with the page title, and a footer that says "Synthetic data made for a workshop." Use it whenever you create or restyle a web page.', 6);
      await lines([['tool', '<b>Write</b>(.claude/skills/house-style/SKILL.md)']], 700);
      await cap('Load it once, then run it like a command');
      await type('/reload-skills', 30);
      await lines([['res', 'Skills reloaded: house-style added']], 500);
      await type('/house-style dashboard.html', 30);
      await lines([['tool', '<b>Skill</b>(house-style)'], ['tool', '<b>Edit</b>(dashboard.html)']], 700);
      await page('dashboard-styled.html', 'study-rooms/dashboard.html', 0.55);
      await sleep(2400);
      await cap('Ask for something new: does it reach for the skill on its own?');
      await type("Make a one-page summary for the library's dean, summary.html, with the three numbers that matter most.", 16);
      await lines([['tool', '<b>Skill</b>(house-style)'], ['tool', '<b>Write</b>(summary.html)'], ['say', 'Followed the house-style skill. 4,351 in FY2026, +40% overall, +6% in the original rooms.']], 700);
      await page('summary.html', 'study-rooms/summary.html', 0.55);
      await sleep(2800);
    }],
    ['undo', async () => {
      await step('7 · Undo');
      await cap('Everyone makes a change they regret');
      await type('Make dashboard.html rainbow-colored, with Comic Sans everywhere.', 22);
      await lines([['tool', '<b>Edit</b>(dashboard.html)']], 500);
      await page('dashboard-rainbow.html', 'study-rooms/dashboard.html', 0.55);
      await sleep(2400);
      await cap('/rewind puts back what Claude edited');
      await type('/rewind', 30);
      await opts('Rewind to before “Make dashboard.html rainbow-colored…”', ['Restore code and conversation', 'Restore conversation only', 'Restore code only'], 0);
      await sleep(1400);
      await page('dashboard-styled.html', 'study-rooms/dashboard.html', 0.55);
      await sleep(2000);
    }],
    ['share', async () => {
      await step('8 · Share');
      await layout('term');
      await cap('Share a live link (Pro plan or higher)');
      await type('Publish dashboard.html as an artifact.', 26);
      await lines([['tool', '<b>Artifact</b>(publish dashboard.html)'], ['res', 'https://claude.ai/code/artifact/…  (private until you share it)']], 800);
      await sleep(2600);
    }],
    ['outro', async () => {
      await S('stage.caption(null); stage.step(null)');
      await S(`stage.card('Your finish line', null, { list: ['Claude Code installed and signed in', 'A dashboard built from a messy spreadsheet', 'One wrong assumption caught in the plan', 'The key number checked against the official answer', 'A CLAUDE.md that remembers, and a skill you keep', 'A link you can share'], url: 'ncsu-libraries.github.io/agentic-coding-with-claude' })`);
      await sleep(5200);
    }],
  ];
};
