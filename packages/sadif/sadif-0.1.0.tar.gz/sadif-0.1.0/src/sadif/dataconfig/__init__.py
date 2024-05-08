from importlib import resources

package = __name__
config_variables_file = resources.files(package) / "variables.json"
