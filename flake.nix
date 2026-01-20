{
  description = "Nix flake to set up the development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python312; # Default Python version
        pythonPkgs = pkgs.python312Packages;
      in {
        devShells.default = pkgs.mkShell {

          buildInputs = with pkgs; [
            python
            git
          ];

          shellHook = ''
            if [ ! -d .venv ]; then
              echo "Creating Python virtual environment (.venv)..."
              python -m venv .venv
              . .venv/bin/activate
              python -m pip install --upgrade pip setuptools wheel
              echo "Installing project dependencies..."
              python -m pip install -r requirements.txt
            else
              . .venv/bin/activate
            fi

            echo "Virtualenv .venv activated. Run your app with: python main.py"
          '';
        };
      }
    );
}