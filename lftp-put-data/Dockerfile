FROM debian:latest
MAINTAINER Book <styshoo@163.com>
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections && apt-get update && apt install vim lftp curl wget jq -y && apt-get clean

COPY .lftprc /root
COPY lftp-send.bash /root

CMD ["/bin/bash", "/root/lftp-send.bash"]