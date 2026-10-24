# AGENTS.md — hamradio-source (the blog)

The Jekyll source for my amateur radio site, published at
`hatandspecs.github.io/hamradio/`. It is a peer of my project repositories and
gets updated alongside them, so a project advance and its write-up land together.

## Layout

| Path | Holds |
|---|---|
| `_articles/<slug>.md` | One article each, with YAML front matter |
| `assets/images/<slug>/` | That article's images |
| `_config.yml` | `baseurl: /hamradio`, permalink `/articles/:name/` |
| `PUBLISHING.md` | How it gets built and published |

Reference images with the Jekyll helper, not a bare path:
`{{ '/assets/images/<slug>/<file>' | relative_url }}`.

## Things that cost a lot to rediscover

- **Do not rewrite a published article's narrative.** Add a dated update
  section instead. The wrong turns are why these are worth reading, and
  quietly correcting them removes the value.
- **When the update contradicts something earlier in the piece, say so
  explicitly.** Do not silently edit the earlier claim, and do not leave the
  contradiction standing unremarked.
- **No British spellings.** `cspell.json` is in the repository.
- **Check every image before adding it.** Phone numbers appear in radio screens
  and log captures; coordinates appear in beacon lines and aprs.fi station
  pages; backgrounds show rooms. Redact and say what you redacted.
- **Beacon coordinates in this project are the center of a 6-character grid
  square**, deliberately rounded. Do not add anything that undoes that — two
  precise distances and bearings to known stations will triangulate a house.
- **cspell runs in CI over every `**/*.md`**, so it reads image filenames too.
  A slug fragment that is not a word — `vna` in `vna-20m-beach.jpg`, for
  instance — fails the build until it is added to `cspell.json`.

## Articles and their projects

Each write-up has a repository: the APRS iGate, the cyberdeck, the FTX-1 tuner
sweep, and several WSPR analyses. Keep claims in an article consistent with the
design document in the matching repository, and prefer the more conservative of
the two when they disagree.

## How I work — standing preferences

These are the same in every repository of mine. They are restated in each one
so that any assistant reads them, not only the one configured on my machine.

**Git is mine.** Never run `git commit` or `git push`, in any repository, for
any reason. Reading history is encouraged — `log`, `diff`, `status`, `show` —
and so is telling me when a good commit point has been reached, or drafting a
commit message for me to use. Finish the work, leave it uncommitted, and say
what changed and where.

**Hardware is mine.** Do not build SD-card images, `rsync` to a device, open an
`ssh` session to one, or run anything on a Raspberry Pi or the cyberdeck unless
I ask in that message. Hand me the exact commands to copy and paste — one block
per step, in order — say what each should print, and stop. I will run them and
paste the output back. Local work in the repository needs no such restraint.

**Writing.** No British spellings; US throughout. Design documents are
declarative: no hero's-journey narrative, no second-person "you", and never
state something as fact and then refute it a few lines later. For an article
already published, add a dated update section rather than rewriting the
narrative — the wrong turns are part of why it is worth reading. Do not repeat
a warning I have already acknowledged.

**Images.** Look at any photograph or screenshot before adding it to an
article, a slide deck, or a repository. Phone numbers show up in radio screens
and log captures, coordinates show up in beacon lines and station pages, and
backgrounds show rooms. Say what you found and redact it rather than guess.

**Destructive commands.** `/dev/sdX` stays a placeholder in any flashing or
disk-writing instructions. Never substitute a real device node.

**Amateur radio.** Test traffic uses my own callsign and its SSIDs — never
another operator's call, unless I explicitly ask for one.

**Working style.** I start fresh sessions often rather than carrying one for
weeks, so assume no memory of previous conversations. Everything you need
should be in this file or in the documents it points at.

**Keeping this file true is part of the work.** Anything dated here records
what was true on that date, not what is true now — check it against the
repository before relying on it, and correct it when it is wrong. When a
session has changed how the project works, turned up a gotcha worth the next
session not rediscovering, or outdated something in a "where it stands"
section, propose the edit to this file before the session ends. Do not wait to
be asked, and do not save it for a tidy-up later: the next session starts cold,
and this file is most of what it gets.
