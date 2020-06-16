FROM redis

RUN apt-get update && apt-get install ruby-dev -y \
    && apt-get install make -y \
    && apt-get install gcc -y \
    && apt-get install procps -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# RUN gem sources -a http://ruby.taobao.org/
RUN gem install redis-dump -V