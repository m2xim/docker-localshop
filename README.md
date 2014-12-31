# docker-localshop

Recipe for building a [Localshop pypi registry](https://github.com/mvantellingen/localshop) docker container.

Link: [ardeois/docker-localshop](https://registry.hub.docker.com/u/ardeois/docker-localshop/)

## Start localshop

    docker run -d -p 8000:8000 ardeois/docker-localshop
This image includes `EXPOSE 8000` (the localshop port).

## Environment Variables

The Localshop image uses several environment variables that may significantly aid you customize it.

### Superuser

* `LOCALSHOP_USERNAME` *localshop*
* `LOCALSHOP_PASSWORD` *localshop*
* `LOCALSHOP_EMAIL` *admin@localshop.example.org*

Locashop is built upon the [Django](https://www.djangoproject.com/) framework, and requires to set up a ``superuser``. As a default this recipe
will create a ``localshop`` superuser with ``localshop`` password. However, if you'd wanna tune it a little bit setup these environment variables to change the default.
Note that if the username already exists in the database, it won't be modified, meaning that the password will not be overriden.

### Runtime parameters

* `LOCALSHOP_GUNICORN_ARGS` *-w 4 -t 60*
* `LOCALSHOP_CELERYD_ARGS` *-B -E*

You can override here the default parameters given to gunicorn and celeryd. This allows you to modify the timeout, the number of workers or anything gunicorn and celeryd supports as a parameter.

### Credentials

* `LOCALSHOP_ACCESS_KEY`
* `LOCALSHOP_SECRET_KEY`

If you want to publish or download artifacts from localshop, you will have to setup theses environment variables. Note that this must be an UUID string.
No default as be set to these.

### CIDR

* `LOCALSHOP_CIDR_VALUE` *0.0.0.0/0*
* `LOCALSHOP_CIDR_REQUIRE_CREDENTIALS` *1* 
* `LOCALSHOP_CIDR_LABEL` *everyone*

By default, localshop blocks any non-authenticated requests to its repository. You can change the cidr settings with these. If `LOCALSHOP_CIDR_REQUIRE_CREDENTIALS` is set to `0`, any request with no access/secret key will be allowed.
Note that the docker image creates the cidr entry in the database, and will override any manual change at every startup of the container. 

### Database settings

* `LOCALSHOP_DATABASE_ENGINE` *django.db.backends.sqlite3*
* `LOCALSHOP_DATABASE_NAME` */home/localshop/.localshop/localshop.db*
* `LOCALSHOP_DATABASE_USER`
* `LOCALSHOP_DATABASE_PASSWORD`
* `LOCALSHOP_DATABASE_HOST`
* `LOCALSHOP_DATABASE_PORT`

Localshop uses sqlite3 by default but you can also connect it to a mysql instance by changing the engine and associated configs.
For example you can link the localshop container with a mysql container and setup the variables as :

    docker run -d -p 8000:8000 --link mysql:db \ 
        -e "LOCALSHOP_DATABASE_ENGINE=django.db.backends.mysql" \
        -e "LOCALSHOP_DATABASE_NAME=database_name" \
        -e "LOCALSHOP_DATABASE_USER=localshop" \
        -e "LOCALSHOP_DATABASE_PASSWORD=password" \
        -e "LOCALSHOP_DATABASE_HOST=db" \
        -e "LOCALSHOP_DATABASE_PORT=3306"\
         ardeois/docker-localshop 


### Timezone
* `LOCALSHOP_TIMEZONE` *America/Montreal*

### Delete files
* `LOCALSHOP_DELETE_FILES` *0*

If set to `1` files will be cleaned up after deleting a package or release from the localshop.


## License

Copyright (c) 2013, Theo Crevon. All rights reserved.


Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.


## Contribute

Localshop container builder is far from perfect, and could be easily enhanced or fixed, don't restrain yourself
just follow the path:

1. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
2. Fork the repository on Github to start making your changes to the master branch.
3. Send a pull request and bug the maintainer until it gets merged and published.
4. Make sure to add yourself to AUTHORS.


*Please note that these instructions were lazily copied from [Kenneth reitz requests](https://github.com/kennethreitz/requests)*

