POPONG source tree
==================

Layout
------
 * web/     contains the source code of the web site.
 * shell/   contains the source code of the tools behind it.
 * test/    contains stuffs for testing.

 * .stage/      is where everything gets installed when you run `make`.
 * buildkit/    is the build system that helps use make.
 * shellkit/    is a library that helps shape our tools.


Prerequisites
-------------

### for running service

    sudo apt-get install coreutils bash lighttpd  procmail grep debianutils 

### for development

    sudo apt-get install make


Development and Testing
-----------------------
### Import developer stuffs into your shell

    . Developer.sh

### Start the POPONG system

    popong start

### Concentrate on your work and testing

    # work work work
    m
    # test



Installation
------------
### Install system

    sudo make install PREFIX=/popong/system

or

    system=/popong/system
    sudo mkdir -p $system
    sudo tar xvzf popong-system-*.tar.gz -C $system


### Initialize service root

    svcroot=/popong/svcroot
    sudo mkdir -p $svcroot
    sudo chown $LOGNAME $svcroot
    cd $svcroot
    /popong/system/bin/popong init


### To start service on system boots

Put the following lines in the service user's crontab:

    @reboot     cd /popong/svcroot && Port=1234 /popong/system/bin/popong start


### To configure Apache to proxy/reverse-proxy URLs to the webserver

Create a file at `/etc/apache2/conf.d/popong.conf` looking like this:

    # Reverse Proxy Config for POPONG Service
    # Author: Jaeho Shin <netj@sparcs.org>
    # Created: 2011-08-20
    <Proxy *>
    Order deny,allow
    Allow from all
    </Proxy>
    ProxyPass        /popong/       http://localhost:1234/popong/
    ProxyPassReverse /popong/       http://localhost:1234/popong/
    RedirectTemp     /popong        /popong/


Then enable Apache module by running:

    sudo a2enmod proxy_http


Finally, restart the server:

    sudo invoke-rc.d apache2 reload

