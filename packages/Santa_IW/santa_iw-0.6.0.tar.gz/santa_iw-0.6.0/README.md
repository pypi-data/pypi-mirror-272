"Santa Is Watching" is a network monitoring tool intended for homelab use. It continuously cycles through a set of tests
on your computers, disks, and network hardware, based upon configuration files describing your system. Santa runs on a
single Linux computer which needs ssh keys to run diagnostic commands on other computers in your system. Simple ping
only testing is available for nodes without ssh access. Santa is not a direct replacement for Nagios, but it addresses a
similar problem space.

A network discovery tool called MakeList is also provided. It takes a list of start and stop network addresses to scan
and tries to determine what tests are appropriate for each node it finds. Any computer which responds to a network ping
becomes a candidate for ping testing. If Santa can make an ssh connection to the node, it will:

* look at temperature and other data reported by lm-sensors
* look for drives listed in /etc/fstab and check for disk free space
* look for drives supported by smartctl and report SMART status on them
* look for zfs pools and check for status and free space
* look for zfs volumes which seem to be getting frequent snapshots (or are listed in pyznap's config file) and monitor
  the age of the last snapshot
* look for failed services reported by systemctl --failed

Santa is written in Python and its configuration files are all editable json. It ships with 20+ built in test types and
can load additional user written tests or plugins from user directories. An example plugin is provided to use a Phillips
Hue color changing light bulb to provide a GREEN/YELLOW/RED status light.

A web based interface lets the user navigate up and down the hierarchy of node groups, nodes and tests to see various
levels of detail. Tests can record numeric data where appropriate. Running averages are displayed and values over time
can be graphed or extracted for offline processing.

----

Santa has been developed and tested on a Linux platform. It has been run on RHEL, Fedora and Debian platforms (including
Raspberry Pi 3). It is written in pure Python, but calls out to many Linux/Posix command line utilities. It is plausible
that it might someday work on other Posix compliant platforms (Macos or BSD), but that is out of scope for the current
effort. Santa will probably never run natively on Windows, and there are not presently any tests designed to exercise
Windows nodes beyond a simple ping.

Santa is intended for homelab use on an internal network. It does not yet have any robust authentication system and
should
not be exposed on the internet.

The code for Santa is pretty much ready for an initial 1.0.0 release, but documentation is still alpha stage.
If you are reading this, you are a little bit early to the party, but feel free to look around. Installation
instructions are on the wiki if you are interested in a test drive. I think I have a week or two of documentation tasks
to complete before I feel comfortable posting to social media in search of beta testers.

----
Key links:

* [Santa Homepage](https://gitlab.com/SRG_gitlab/santa-is-watching)
* [Santa Wiki](https://gitlab.com/SRG_gitlab/santa-is-watching/-/wikis/home)
* [Santa API](https://srg_gitlab.gitlab.io/santa-is-watching/index.html)
* [Santa Issues](https://gitlab.com/SRG_gitlab/santa-is-watching/-/issues)
* [Libsrg Wiki](https://gitlab.com/SRG_gitlab/libsrg/-/wikis/home)