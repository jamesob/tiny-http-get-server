
# tiny-http-get-server

A single-file, dependency free way to create a simple webserver that responds to
GET requests with Python 3 stdlib. Oddly enough, `http.server` doesn't provide an
easy way to do this out of the box.

## Install and usage

1. Copy this file
2. Modify `MyReqHandler.get_content()` - and whatever else you'd like!

## Example usages

- Making a simple, dependency free [Prometheus
  exporter](https://github.com/prometheus/docs/blob/main/content/docs/instrumenting/exposition_formats.md).
