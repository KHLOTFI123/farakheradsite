# syntax=docker/dockerfile:1

FROM public.ecr.aws/nginx/nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY dist /usr/share/nginx/html
EXPOSE 80
