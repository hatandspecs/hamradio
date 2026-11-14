#!/usr/bin/env bash
# Local preview of the site, in a container running the same Ruby as CI.
#
# Fedora's system Ruby moved to 4.0, which the github-pages gem tree cannot
# resolve against: bundler silently backtracks to github-pages 8 from 2014 and
# the ancient C extensions fail to compile. publish.yml builds on Ruby 3.4, so
# previews run on Ruby 3.4 too. See PUBLISHING.md.
#
#   ./preview.sh           serve at http://127.0.0.1:4000/hamradio/, drafts included
#   ./preview.sh public    same, but only what visitors would see
#   ./preview.sh build     one-shot build into _site/ and exit
#   ./preview.sh install   (re)install the locked gems into vendor/bundle/
set -euo pipefail

IMAGE=docker.io/library/ruby:3.4-slim
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUNTIME=$(command -v podman || command -v docker) || {
    echo "need podman or docker" >&2; exit 1; }

run() { "$RUNTIME" run --rm "$@" -v "$REPO":/srv/jekyll:z -w /srv/jekyll \
        -e PAGES_REPO_NWO=hatandspecs/hamradio -e DEBIAN_FRONTEND=noninteractive \
        "$IMAGE" bash -lc "$CMD"; }

serve_cmd() {  # $1 is "--unpublished" or empty
    # A previous run left running would hold port 4000 and the failure message
    # from the network layer does not say so.
    if "$RUNTIME" ps --format '{{.Names}}' | grep -qx jekyll-preview; then
        echo "stopping a preview already running..."
        "$RUNTIME" stop jekyll-preview >/dev/null 2>&1 || true
        sleep 1
    fi
    echo "http://127.0.0.1:4000/hamradio/   (ctrl-c to stop)"
    CMD="bundle config set --local path vendor/bundle >/dev/null &&
         bundle exec jekyll serve --host 0.0.0.0 --livereload $1"
    # 127.0.0.1, not localhost: the container publishes IPv4 only, and localhost
    # resolves to ::1 first, which fails with a connection reset.
    run -it --name jekyll-preview \
        -p 127.0.0.1:4000:4000 -p 127.0.0.1:35729:35729
}

case "${1:-serve}" in
  install)
    CMD='apt-get update -qq >/dev/null 2>&1 &&
         apt-get install -y -qq build-essential git >/dev/null 2>&1 &&
         bundle config set --local path vendor/bundle && bundle install --jobs 4'
    run ;;
  build)
    CMD='bundle config set --local path vendor/bundle >/dev/null &&
         bundle exec jekyll build --unpublished --trace'
    run ;;
  serve)  serve_cmd --unpublished ;;
  public) serve_cmd "" ;;
  *)
    echo "usage: $0 [serve|public|build|install]" >&2; exit 1 ;;
esac
