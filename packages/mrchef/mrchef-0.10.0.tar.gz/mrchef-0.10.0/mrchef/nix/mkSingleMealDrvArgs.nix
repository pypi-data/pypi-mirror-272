{
  lib,
  mrchefLib,
  writeText,
}:
/*
Generate mkDerivation arguments to imitate the behavior of Mr. Chef with Nix.

Only useful to warm up a single meal.

This is faster than using `mkPureWarmupHook` and allows Nix to benefit more of
caching and avoid unnecessary rebuilds.

However, it could be more buggy because it doesn't reuse the same code as Mr.
Chef. Instead, it is an alternate implementation in pure Nix.
*/
fullSrc: mealName: let
  config = mrchefLib.config fullSrc;
  freezer = mrchefLib.freezer fullSrc;
  patchContents =
    lib.attrVals
    (config.meals.${mealName}.spices or [])
    (freezer.spices or {});
in {
  src = mrchefLib.fetchMeal (config.meals.${mealName} // freezer.meals.${mealName});
  patches = builtins.map (writeText "mrchef-patch") patchContents;
}
