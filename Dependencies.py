def check_module(required):
    # Import
    import sys
    import subprocess
    import pkg_resources

    # Get set all modules in system
    installed = {pkg.key for pkg in pkg_resources.working_set}
    # Get set of missing modules
    missing = required - installed

    if missing:     # If any module is missing
        print("Missing modules are",missing)

        # Ask Permissing to install modle
        if input("You have to install it to continue (Y/n): ").lower() == "y":
            # Iterate througth each missing module
            for module in missing:

                # Install
                try:
                    print("Installing Module "+module+".....", end="\r")
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', module], 
                                            stdout=subprocess.DEVNULL)
                    print("\rModule "+module+" is installed successfully....")

                except:
                    print("Unexpected error occured while installing",
                            module,
                            "\n\t Please solve the issue, then run again")
                    exit(0)
        else:
            print("Sorry, all Dependencies are not satisfied....")
            exit(0)
