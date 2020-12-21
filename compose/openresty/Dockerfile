FROM node:10 as stage-build

WORKDIR /data

COPY ./frontend /data
RUN yarn install && yarn build

FROM openresty/openresty:centos

COPY --from=stage-build /data/lina /opt/lina

COPY ./openresty/conf.d/site-enabled /etc/nginx/conf.d/site-enabled
COPY ./openresty/conf.d/nginx.conf /usr/local/openresty/nginx/conf/nginx.conf
COPY ./openresty/yum.repos.d/openresty.repo /etc/yum.repos.d/openresty.repo
COPY ./openresty/luarocks/config-5.1.lua /usr/local/etc/luarocks/config-5.1.lua
COPY ./openresty/lua /etc/nginx/lua
COPY ./openresty/whitelist.conf /etc/nginx/whitelist.conf

RUN yum update -y \
  && yum install -y diffutils gcc epel-release

RUN yum install -y inotify-tools

RUN luarocks install lua-resty-auto-ssl  \
  && luarocks install lua-resty-iputils \
  && luarocks install lua-cjson



CMD ["/usr/local/openresty/bin/openresty", "-g", "daemon off;"]