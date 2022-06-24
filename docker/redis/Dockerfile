# Altered copy of https://github.com/RedisLabsModules/redismod/blob/master/Dockerfile
# with only redisearch and rejson

FROM redislabs/redisearch:latest as redisearch
FROM redislabs/rejson:latest as rejson
FROM redis:latest

ENV LD_LIBRARY_PATH /usr/lib/redis/modules

WORKDIR /data
RUN apt-get update -qq
RUN apt-get upgrade -y
RUN rm -rf /var/cache/apt

COPY --from=redisearch ${LD_LIBRARY_PATH}/redisearch.so ${LD_LIBRARY_PATH}/
COPY --from=rejson ${LD_LIBRARY_PATH}/*.so ${LD_LIBRARY_PATH}/

ENTRYPOINT ["redis-server"]
CMD ["/etc/redis/redis.conf", \
    "--loadmodule", "/usr/lib/redis/modules/redisearch.so", \
    "--loadmodule", "/usr/lib/redis/modules/rejson.so"]