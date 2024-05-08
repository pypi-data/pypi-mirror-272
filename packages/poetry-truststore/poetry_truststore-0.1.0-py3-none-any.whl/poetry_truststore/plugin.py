from cleo.io.io import IO

from poetry.plugins.plugin import Plugin
from poetry.poetry import Poetry
import truststore


class TrustStorePlugin(Plugin):

    def activate(self, poetry: Poetry, io: IO):
        io.write_line("Enabling Truststore")
        poetry.package.readme = "README.md"
        truststore.inject_into_ssl()