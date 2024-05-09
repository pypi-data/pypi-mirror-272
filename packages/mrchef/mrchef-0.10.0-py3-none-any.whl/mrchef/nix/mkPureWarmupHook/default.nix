{
  cacert,
  coreutils,
  git,
  lib,
  makeSetupHook,
  mrchef,
  mrchefLib,
  stdenv,
  writeScript,
  ...
}:
/*
Generate a warmup build hook that uses pure inputs.

Args:

- `src`: Same as the end derivation's src. It must contain `./mrchef.toml`
  and `./.mrchef.freezer.toml` files.
  Currently, there's no support for `srcs` or multiple `mrchef.toml` files.

- `unpackedSrcDir`: The hook will run on `postUnpack` phase. Here you can indicate
  where to find the unpacked sources in the build directory. Usually, the default
  value will be enough. It can be any bash code that fits inside a variable
  declaration.

Roadmap / known issues:
- TODO Support multiple kitchens.
- TODO Support `srcs`.
*/
{
  src,
  unpackedSrcDir ? "$(stripHash $src)", # Just in case src unpacks in a weird place
}: let
  # Purify MrChef inputs
  originalConf = mrchefLib.config src;
  originalFreezer = mrchefLib.freezer src;
  pureMeals =
    builtins.mapAttrs
    (name: value: mrchefLib.fetchMeal (value // originalFreezer.meals.${name}))
    originalConf.meals;
  pureMealsJSON = mrchefLib.toJSONFile "pureMeals" pureMeals;
in
  makeSetupHook rec {
    name = "mkPureWarmupHook";
    meta = {
      description = "Automatic Mr. Chef nix kitchen warmer";
      longDescription = ''
        Add this dependency to `buildInputs` in a derivation whose `src` is
        a Mr. Chef kitchen and it will warm up that kitchen automatically.
      '';
      license = lib.licenses.gpl3Plus;
      homepage = "https://gitlab.com/moduon/mrchef";
    };
    substitutions = {
      mrchefPython = mrchef.config.deps.python.withPackages (ps: [mrchef.config.package-func.result]);
      pureMealsVar = lib.toShellVar "pureMealsJSON" pureMealsJSON;
      gitVar = lib.toShellVar "GIT_AUTOSHARE_GIT_BIN" "${git}/bin/git";
      certsVar = lib.toShellVar "NIX_SSL_CERT_FILE" "${cacert}/etc/ssl/certs/ca-bundle.crt";
    };
  }
  # Automatic hook for derivations that depend on this one
  (writeScript "mkPureWarmupHook.sh" ''
    pureWarmupHook() {
      (
        export @certsVar@
        export @gitVar@
        export @pureMealsVar@
        export EMAIL="nixbld@localhost" # For git commits
        export PATH=$PATH:${mrchef.config.mkDerivation.passthru.binDepsPath}
        export unpackedSrcDir=${unpackedSrcDir}
        @mrchefPython@/bin/python ${./builder.py}
      )
    }

    postUnpackHooks+=(pureWarmupHook)
  '')
