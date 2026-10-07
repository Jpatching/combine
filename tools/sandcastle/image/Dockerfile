FROM python:3.10.19-bookworm@sha256:44325b079a3c59b1dd0704471fc9ffccd98f13789f00f30bdbdaa99dce03bcc7 AS python
FROM node:24.10.0-bookworm@sha256:06e54ecf113a30f0ff9a1d309866a5924d3bda4389eab11a0e1e92f3251d915d
COPY --from=python /usr/local/lib/libpython3.10.so* /usr/local/lib/
COPY --from=python /usr/local/lib/python3.10 /usr/local/lib/python3.10
COPY --from=python /usr/local/bin/python3.10 /usr/local/bin/python3.10
RUN ln -sf /usr/local/bin/python3.10 /usr/local/bin/python3 && ldconfig
ARG AGENT_UID=1000
ARG AGENT_GID=1000
RUN groupmod -o -g ${AGENT_GID} node && usermod -o -u ${AGENT_UID} -g ${AGENT_GID} -d /home/agent -m -l agent node
RUN npm install -g --ignore-scripts @openai/codex@0.160.1 typescript@6.0.3
USER ${AGENT_UID}:${AGENT_GID}
WORKDIR /home/agent
ENTRYPOINT ["sleep", "infinity"]
