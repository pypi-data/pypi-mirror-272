{
  lib,
  mrchefLib,
  nix-filter,
  yj,
  stdenv,
}:
/*
A derivation that creates a warmed-up source tree.

Arguments:
- mealsToWarmup: a list of meals to warm up; if null, all meals are warmed up.
- src: the source tree to warm up; it should be filtered to include only files relevant
  to Mr. Chef, for better caching.
*/
{
  mealsToWarmup ? null,
  src,
}: let
  suffix =
    if mealsToWarmup == null
    then "all"
    else
      # The _ separator allows displaying name properly; other separators make
      # nix take the meal name as a version if it starts with a number
      "meals_"
      + builtins.replaceStrings ["-" "."] ["_" "_"] (
        lib.strings.sanitizeDerivationName (builtins.toString mealsToWarmup)
      );

  # Reuse the warmup hook to produce the final source tree; no need to further
  # filter the meals, because the whole configs were already filtered
  pureWarmupHook = mrchefLib.mkPureWarmupHook {
    inherit src;
  };
in
  stdenv.mkDerivation {
    inherit src;
    name = "mrchef-warmed-up-src-${suffix}";
    mealsToWarmup = builtins.toJSON mealsToWarmup;
    buildInputs = [pureWarmupHook];
    installPhase = ''
      runHook preInstall

      warm=$PWD
      cd ..
      mv $warm $out

      runHook postInstall
    '';

    # Disable stuff that makes no sense for this kind of derivation
    dontBuild = true;
    dontConfigure = true;
    dontFixup = true;
    dontPatch = true;
    dontPatchELF = true;
    dontPatchShebangs = true;
    dontStrip = true;

    # You should have the sources already locally
    preferLocalBuild = true;
  }
