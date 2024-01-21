import re


class PyReverseClient:

    def __init__(self):
        self.pkg_fan_in = {}
        self.pkg_fan_out = {}

    def get_coupling(self, dot_path):

        # Sample DOT line format:
        #   "requests" -> "requests.api" [arrowhead="open", arrowtail="none"];
        # In the above line, the module "requests" has dependency (is coupled to) the module "requests.api"

        # Use regex to find lines that match the coupling line pattern (like the example)
        coupling_line_pattern = r'\"(\w.+)\"\s->\s\"([\w.]+)\"'

        dot_file = open(dot_path)

        print("Module Dependency Output: ")
        for line in dot_file:
            if '->' in line:
                coupling_line = re.search(coupling_line_pattern, line)
                if coupling_line:
                    module_src, module_dst = coupling_line.group(1).strip(), coupling_line.group(2).strip()

                    print(' - module {} is dependent on {}'.format(module_src, module_dst))

                    # Keep track of number of fan in/out (dependency) per module
                    fan_out = self.pkg_fan_out.get(module_src, 0)
                    self.pkg_fan_out.update({module_src: fan_out + 1})

                    fan_in = self.pkg_fan_in.get(module_dst, 0)
                    self.pkg_fan_in.update({module_dst: fan_in + 1})

        # Create some visual spacing in the output
        print()
        print("----------")
        print("Module Dependency Frequencies: ")
        print()

        # Using fan_in as coupling metric.
        for k, v in self.pkg_fan_in.items():
            print(v)


if __name__ == '__main__':
    print()
    # Input dot file
    PACKAGE_FILE = input("Enter packages_xxx.dot file path: ")
    print()
    print("Packages Dot File: " + PACKAGE_FILE)
    print("----------")
    print()

    # Create a client object.
    pyreverse_client = PyReverseClient()

    # Print out coupling for all modules.
    pyreverse_client.get_coupling(dot_path=PACKAGE_FILE)
