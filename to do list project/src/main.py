import sys
import argparse
from src import cli

def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--cli', action='store_true', help="Run in CLI mode")
    args, unknown = parser.parse_known_args()

    if args.cli or len(sys.argv) > 1:
        # Pass control to CLI module if --cli is present or any other args are provided
        # We need to remove --cli from sys.argv so argparse in cli.py doesn't complain, 
        # but actually cli.py uses its own parser. 
        # However, since we used parse_known_args, we can just call cli.run_cli() 
        # but we need to ensure sys.argv is clean or passed explicitly.
        # Actually, simpler: if --cli or subcommands exist, run CLI.
        # if no args, run GUI.
        
        # Let's adjust logic:
        # if arguments exist (other than script name), treat as CLI.
        # except if it's just --gui (if we had one) or similar.
        # But per plan: "Default to GUI if no args provided".
        
        cli.run_cli()
    else:
        try:
            from src import gui
            gui.run_gui()
        except ImportError:
            # Fallback if GUI not implemented yet or fails
            print("GUI module not found or failed to load. Running CLI help.")
            sys.argv.append("--help")
            cli.run_cli()
        except Exception as e:
            print(f"Error launching GUI: {e}")
            input("Press Entry to exit...")

if __name__ == "__main__":
    main()
