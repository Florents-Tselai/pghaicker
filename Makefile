PYTHON ?= python3
PANDOC ?= pandoc
PGHAICKER = pghaicker
THREADS = 2626029

# Rule to download the HTML thread
threads/html/%.html:
	curl -sL "https://postgrespro.com/list/thread-id/$*" -o $@

# Rule to convert HTML to Markdown
threads/md/%.md: threads/html/%.html
	$(PANDOC) --from=html --to=markdown $< -o $@

# Rule to summarize the Markdown thread
threads/summary/%.md: threads/md/%.md
	cat $^ | $(PGHAICKER) summarize $* > $@

# Top-level rule
all: threads/md/$(THREADS).md threads/summary/$(THREADS).md

# Clean rule
clean:
	-rm -f threads/html/*.html threads/md/*.md threads/summary/*.md