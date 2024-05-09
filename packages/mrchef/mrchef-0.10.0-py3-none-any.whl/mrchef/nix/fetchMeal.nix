/*
Get meal upstream git code.

Most args come from the combination of a meal data from `mrchef.toml` and
`.mrchef.freezer.toml`. Extra args are:

- `optimizeMealFetch`: Use better builtin fetchers that require nix flakes to
  work. It is set to `false` automatically if you're disabling flakes.
- `returnAttr`: If set, return the attribute name of the fetched sources.
*/
{
  branch,
  nar_hash ? null,
  optimizeMealFetch ? builtins ? getFlake,
  pkgs ? import <nixpkgs> {},
  returnAttr ? null,
  rev,
  url,
  ...
}: let
  inherit (builtins) elemAt fetchGit fetchTree match stringLength substring;

  githubParts = match "https://github.com/([^/]+)/([^/]+)" url;
  gitlabParts = match "https://gitlab.com/(.+)/([^/]+)" url;
  gitHttp = match "https?://.*" url;
  dotGitEnd = str: (match ".*[.]git" str) != null;
  rstripDotGit = str:
    if dotGitEnd str
    then substring 0 ((stringLength str) - 4) str
    else str;
  builtinFetcherCommonArgs =
    {inherit rev;}
    // (
      if nar_hash == null
      then {}
      else {narHash = nar_hash;}
    );
  # fetchGit is slow because it fetches the entire git history. However, it's
  # the onlly one that performs SSH cloning, reusing user's SSH agent.
  fallbackFetcher = fetchGit (builtinFetcherCommonArgs
    // {
      inherit url;
      ref = branch;
      # TODO When https://github.com/NixOS/nix/issues/5119 is fixed, see if
      # we still need other options, or fetchGit becomes good enough.
      shallow = true;
    });
  sources =
    # If we're not returning an attribute and we have a NAR hash already, it
    # means we're asking for the sources. Thus, we can attempt to use fetch
    # derivations from nixpkgs that are more efficient because they are
    # deferred until build time, and don't block evaluation.
    # DOCS https://jade.fyi/blog/nix-evaluation-blocking/#builtin-fetchers
    if returnAttr == null && nar_hash != null
    then
      # TODO When some of these issues are fixed, we should be able to
      # rely only on builtin fetchers:
      # HACK https://github.com/NixOS/nix/issues/5119
      # HACK https://github.com/NixOS/nix/issues/9077
      # HACK https://github.com/NixOS/nix/issues/10104
      if githubParts != null
      then
        pkgs.fetchFromGitHub {
          inherit rev;
          owner = elemAt githubParts 0;
          repo = rstripDotGit (elemAt githubParts 1);
          hash = nar_hash;
        }
      else if gitlabParts != null
      then
        pkgs.fetchFromGitLab {
          inherit rev;
          owner = elemAt gitlabParts 0;
          repo = rstripDotGit (elemAt gitlabParts 1);
          hash = nar_hash;
        }
      else if gitHttp != null
      then
        pkgs.fetchgit {
          inherit url rev;
          hash = nar_hash;
        }
      else fallbackFetcher
    else if optimizeMealFetch && githubParts != null
    then
      fetchTree (builtinFetcherCommonArgs
        // {
          type = "github";
          owner = elemAt githubParts 0;
          repo = rstripDotGit (elemAt githubParts 1);
        })
    else if optimizeMealFetch && gitlabParts != null
    then
      fetchTree (builtinFetcherCommonArgs
        // {
          type = "gitlab";
          owner = elemAt gitlabParts 0;
          repo = rstripDotGit (elemAt gitlabParts 1);
        })
    else fallbackFetcher;
in
  if returnAttr == null
  then sources
  else sources.${returnAttr}
