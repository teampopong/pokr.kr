# Shell script for setting up POPONG development environment
# 
# Source this file into your interactive shell using for development:
# 
#     . Developer.sh
# 
# Or, with an equivalent command:
# 
#     source Developer.sh
# 
# You can now use installed commands on the stage, as well as the commands used
# for building them.
#
# Author: Jaeho Shin <netj@sparcs.org>
# Created: 2011-08-20

# Remember where root of the source tree was
export POPONG_SRCROOT=$PWD
export POPONG_SVCROOT="$PWD/test/svcroot"

# PATH for testing and building
export PATH="$POPONG_SRCROOT/.stage/bin:$POPONG_SRCROOT/buildkit:$PATH"

# convenience command for invoking make from anywhere
m() { (cd "$POPONG_SRCROOT" && make "$@"); }

# TODO shell command competion
