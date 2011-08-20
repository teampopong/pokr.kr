#!/usr/bin/env bash
# popong -- The command-line interface to popong
# Usage: popong COMMAND [ARG]...
#
# Generator: ShellKit (https://github.com/netj/shellkit)
# Generated: 2011-08-20
set -eu

# Detect where popong is installed
Self=`readlink -f "$0" || echo "$0"`
Here=`dirname "$Self"`

# set POPONG_SVCROOT to current directory if not defined
: ${POPONG_SVCROOT:=$PWD}
export POPONG_SVCROOT

# Setup some environment
export POPONG_HOME=${Here%/@POPONG_BINDIR@}
export POPONG_BINDIR="$POPONG_HOME/@POPONG_BINDIR@"
export POPONG_LIBDIR="$POPONG_HOME/@POPONG_LIBDIR@"
export POPONG_TOOLSDIR="$POPONG_HOME/@POPONG_TOOLSDIR@"
export POPONG_WWWDIR="$POPONG_HOME/@POPONG_WWWDIR@"
export POPONG_DATADIR="$POPONG_HOME/@POPONG_DATADIR@"
export POPONG_DOCDIR="$POPONG_HOME/@POPONG_DOCDIR@"

export PATH="$POPONG_TOOLSDIR:$POPONG_HOME/lib/shellkit:$PATH"


# Process input arguments
[ $# -gt 0 ] || usage "$0" "No COMMAND given"
Cmd=$1; shift


# Check it is a valid command
exe=popong-"$Cmd"
if type "$exe" &>/dev/null; then
    set -- "$exe" "$@"
else
    error "$Cmd: Unknown popong command" || true
    echo "Try \`popong help' for usage."
    false
fi


# Run given command under this environment
exec "$@"
