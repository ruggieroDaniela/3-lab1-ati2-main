# syntax=docker/dockerfile:1

FROM public.ecr.aws/docker/library/python:3.10-buster

# Don’t delete the downloaded apt packages
RUN rm -f /etc/apt/apt.conf.d/docker-clean

# Install apt packages, keep a cache
RUN --mount=type=cache,target=/var/cache/apt \
  apt-get update && apt-get install -yqq --no-install-recommends \
  gettext && rm -rf /var/lib/apt/lists/*
