# Copyright (c) 2013 theo crevon
#
# See the file LICENSE for copying permission.

FROM ubuntu:14.04
MAINTAINER cardeois@iweb.com

# make sure the package repository is up to date
RUN apt-get update

# Install dependencies
RUN apt-get install -y libc6-dev build-essential pkg-config
RUN apt-get install -y sqlite3 fabric
RUN apt-get install -y python-dev python-pip python-setuptools python-virtualenv libmysqlclient-dev


# Configure a localshop user
# Prepare user and directories
RUN addgroup --system localshop
RUN adduser --system --shell /bin/bash --gecos 'localshop operator' --uid 4000 --disabled-password --home /home/localshop localshop
RUN adduser localshop localshop


# Create it's virtualenv
RUN virtualenv /home/localshop/venv
RUN mkdir /home/localshop/.localshop
RUN mkdir /home/localshop/data/
RUN chown -R localshop:localshop /home/localshop
RUN chmod -R 775 /home/localshop


# Set up environement variables for proper setup
ENV HOME /home/localshop

# Proceed to installation
ADD ./context /home/localshop/
ADD ./fabfile /home/localshop/fabfile
ADD ./run_localshop.sh /home/localshop/run_localshop.sh
RUN cd /home/localshop && fab localshop_install

# Ensure localshop sources directory is writable
RUN mkdir /home/localshop/source
RUN chown -R localshop:localshop /home/localshop/source
RUN chmod -R 775 /home/localshop/source

RUN chown localshop:localshop /home/localshop/run_localshop.sh
RUN chmod 775 /home/localshop/run_localshop.sh

#Forward ports
EXPOSE 8000

# Let's run
CMD ["su", "localshop", "-c", "/home/localshop/run_localshop.sh"]

