{
  config,
  dream2nix,
  lib,
  ...
}: rec {
  imports = [
    dream2nix.modules.dream2nix.pip
  ];

  inherit (mkDerivation.passthru.pyproject.project) name version;

  deps = {nixpkgs, ...}: {
    inherit (nixpkgs) makeBinaryWrapper nix-filter;
    binDeps = [
      nixpkgs.git
      config.pip.drvs.git-autoshare.public
    ];
    python = nixpkgs.python311;
  };

  # HACK https://github.com/nix-community/dream2nix/issues/601
  paths.lockFile = "${config.deps.stdenv.system}.lock";

  mkDerivation = {
    passthru = {
      binDepsPath = lib.makeBinPath config.deps.binDeps;
      pyproject = lib.importTOML (config.paths.projectRoot + /pyproject.toml);
    };

    src = config.deps.nix-filter.filter {
      root = config.paths.projectRoot;
      include = [
        "MANIFEST.in"
        "mrchef"
        "pyproject.toml"
        "README.md"
        "tests"
      ];
      exclude = [
        # These are tested in flake checks; when they change, they shouldn't
        # trigger a rebuild of Mr. Chef
        "tests/nix"
      ];
    };

    buildInputs = [config.deps.makeBinaryWrapper];
    propagatedBuildInputs = config.deps.binDeps;

    doCheck = true;
    checkPhase = ''
      runHook preCheck

      export GIT_AUTOSHARE_CACHE_DIR=$TMPDIR
      pytest -m "not impure"

      runHook postCheck
    '';
    nativeCheckInputs =
      config.deps.binDeps
      ++ [
        config.pip.drvs.pytest-xdist.public
      ];

    # Make sure Mr. Chef always has its binary dependencies available
    postFixup = ''
      wrapProgram $out/bin/mrchef \
        --suffix PATH : ${mkDerivation.passthru.binDepsPath}
    '';

    meta = {
      description = "👨‍🍳 Meta-Repo Chef";
      longDescription = ''
        Culinary git helper to work with code buffets.
      '';
      homepage = "https://gitlab.com/moduon/mrchef";
      license = lib.licenses.gpl3Plus;
      maintainers = [lib.maintainers.yajo];
    };
  };

  buildPythonPackage = {
    format = "pyproject";
    pythonImportsCheck = [name];
  };

  pip = {
    pypiSnapshotDate = "2024-01-30";
    flattenDependencies = true;
    requirementsList = with mkDerivation.passthru.pyproject;
      build-system.requires
      ++ project.dependencies
      ++ project.optional-dependencies.dev;
  };
}
