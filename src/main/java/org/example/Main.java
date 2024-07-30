package org.example;

import com.linecorp.armeria.common.HttpRequest;
import com.linecorp.armeria.common.HttpResponse;
import com.linecorp.armeria.common.HttpStatus;
import com.linecorp.armeria.common.MediaType;
import com.linecorp.armeria.server.HttpService;
import com.linecorp.armeria.server.Server;
import com.linecorp.armeria.server.ServerBuilder;
import com.linecorp.armeria.server.ServiceRequestContext;
import com.linecorp.armeria.server.annotation.Get;

public class Main {
    static Server newServer(int port) {
        final ServerBuilder sb = Server.builder();
        sb.http(port);

        sb.baseContextPath("/api")
          .contextPath("/a1", "/a2")
          .contextPath("/b1")
          .annotatedService(new Object() {
              @Get("/svc1")
              public HttpResponse hello() {
                  return HttpResponse.of(HttpStatus.OK, MediaType.PLAIN_TEXT_UTF_8, "svc1");
              }
          })
          .contextPath("/c1")
          .contextPath("/d1")
          .service("/svc2", new HttpService() {
              @Override
              public HttpResponse serve(ServiceRequestContext ctx, HttpRequest req) {
                  return HttpResponse.of(HttpStatus.OK, MediaType.PLAIN_TEXT_UTF_8, "svc2");
              }
          })
          .contextPath("/e1", "/e2")
          .service("/svc3", new HttpService() {
              @Override
              public HttpResponse serve(ServiceRequestContext ctx, HttpRequest req) {
                  return HttpResponse.of(HttpStatus.OK, MediaType.PLAIN_TEXT_UTF_8, "svc3");
              }
          })
          .service("/svc4", new HttpService() {
              @Override
              public HttpResponse serve(ServiceRequestContext ctx, HttpRequest req) {
                  return HttpResponse.of(HttpStatus.OK, MediaType.PLAIN_TEXT_UTF_8, "svc4");
              }
          })
          .contextPath("/f1")
          .contextPath("/g1")
          .contextPath("/h1")
          .service("/svc5", new HttpService() {
              @Override
              public HttpResponse serve(ServiceRequestContext ctx, HttpRequest req) {
                  return HttpResponse.of(HttpStatus.OK, MediaType.PLAIN_TEXT_UTF_8, "svc5");
              }
          })
          .before()
          .contextPath("/i1")
          .service("/svc6", new HttpService() {
              @Override
              public HttpResponse serve(ServiceRequestContext ctx, HttpRequest req) {
                  return HttpResponse.of(HttpStatus.OK, MediaType.PLAIN_TEXT_UTF_8, "svc6");
              }
          })
          .and()
          .contextPath("/second")
          .service("/svc7", new HttpService() {
              @Override
              public HttpResponse serve(ServiceRequestContext ctx, HttpRequest req) {
                  return HttpResponse.of(HttpStatus.OK, MediaType.PLAIN_TEXT_UTF_8, "svc7");
              }
          });


        return sb.build();
    }


    public static void main(String[] args) {
        Server server = newServer(8080);
        server.closeOnJvmShutdown();
        server.start().join();

    }
}
