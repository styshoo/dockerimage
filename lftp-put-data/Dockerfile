FROM debian:latest
MAINTAINER Book <styshoo@163.com>
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections && apt-get update && apt install vi lftp curl wget jq -y && apt-get clean
