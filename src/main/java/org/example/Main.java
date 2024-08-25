package org.example;

import java.util.Set;

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
          .contextPath("/context-path/a1", "/context-path/a2")
          .nestedContext()
          .contextPaths(Set.of("/b1", "/b2"), ctx1 -> ctx1
                  .annotatedService(new Object() {
                      @Get("/svc1")
                      public HttpResponse hello1() {
                          return HttpResponse.of(HttpStatus.OK, MediaType.PLAIN_TEXT_UTF_8,
                                                 "/api/context-path/[a1|a2]/[b1|b2]/svc1");
                      }

                      @Get("/svc2")
                      public HttpResponse hello2() {
                          return HttpResponse.of(HttpStatus.OK, MediaType.PLAIN_TEXT_UTF_8,
                                                 "/api/context-path/[a1|a2]/[b1|b2]/svc2");
                      }

                  })
                  .service("/my-service", new HttpService() {
                      @Override
                      public HttpResponse serve(ServiceRequestContext ctx, HttpRequest req) throws Exception {
                          return HttpResponse.of(HttpStatus.OK, MediaType.PLAIN_TEXT_UTF_8,
                                                 "/api/context-path/[a1|a2]/[b1|b2]/my-service");
                      }
                  })
                  .contextPaths(Set.of("/c1", "/c2"), ctx2 -> ctx2
                          .service("/my-service1", new HttpService() {
                              @Override
                              public HttpResponse serve(ServiceRequestContext ctx, HttpRequest req)
                                      throws Exception {
                                  return HttpResponse.of(HttpStatus.OK, MediaType.PLAIN_TEXT_UTF_8,
                                                         "/api/context-path/[a1|a2]/[b1|b2]/[c1|c2]/my-service1");
                              }
                          })
                          .service("/my-service2", new HttpService() {
                              @Override
                              public HttpResponse serve(ServiceRequestContext ctx, HttpRequest req)
                                      throws Exception {
                                  return HttpResponse.of(HttpStatus.OK, MediaType.PLAIN_TEXT_UTF_8,
                                                         "/api/context-path/[a1|a2]/[b1|b2]/[c1|c2]/my-service2");
                              }
                          })));

        sb.virtualHost("foo.com")
          .contextPath("/virtual-foo")
          .nestedContext()
          .contextPaths(Set.of("/a1", "/a2"), ctx -> ctx
                  .service("/my-service1", new HttpService() {
                      @Override
                      public HttpResponse serve(ServiceRequestContext ctx, HttpRequest req)
                              throws Exception {
                          return HttpResponse.of(HttpStatus.OK, MediaType.PLAIN_TEXT_UTF_8,
                                                 "foo.com /virtual-foo/[a1|a2]/my-service1");
                      }
                  })
                  .service("/my-service2", new HttpService() {
                      @Override
                      public HttpResponse serve(ServiceRequestContext ctx, HttpRequest req)
                              throws Exception {
                          return HttpResponse.of(HttpStatus.OK, MediaType.PLAIN_TEXT_UTF_8,
                                                 "foo.com /virtual-foo/[a1|a2]/my-service2");
                      }
                  })
                  .annotatedService(new Object() {
                      @Get("/svc1")
                      public HttpResponse hello1() {
                          return HttpResponse.of(HttpStatus.OK, MediaType.PLAIN_TEXT_UTF_8,
                                                 "foo.com /virtual-foo/[a1|a2]/svc1");
                      }

                      @Get("/svc2")
                      public HttpResponse hello2() {
                          return HttpResponse.of(HttpStatus.OK, MediaType.PLAIN_TEXT_UTF_8,
                                                 "foo.com /virtual-foo/[a1|a2]/svc2");
                      }}
                  )
                  .contextPaths(Set.of("/b1", "/b2"), ctx2 -> ctx2
                          .service("/my-service", new HttpService() {
                              @Override
                              public HttpResponse serve(ServiceRequestContext ctx, HttpRequest req)
                                      throws Exception {
                                  return HttpResponse.of(HttpStatus.OK, MediaType.PLAIN_TEXT_UTF_8,
                                                         "foo.com /virtual-foo/[a1|a2]/[b1|b2]/my-service");
                              }
                          }))
          );

        sb.virtualHost("bar.com")
          .contextPath("/virtual-foo")
          .nestedContext()
          .contextPaths(Set.of("/a1", "/a2"), ctx -> ctx
                  .service("/my-service1", new HttpService() {
                      @Override
                      public HttpResponse serve(ServiceRequestContext ctx, HttpRequest req)
                              throws Exception {
                          return HttpResponse.of(HttpStatus.OK, MediaType.PLAIN_TEXT_UTF_8,
                                                 "bar.com /virtual-foo/[a1|a2]/my-service1");
                      }
                  })
                  .service("/my-service2", new HttpService() {
                      @Override
                      public HttpResponse serve(ServiceRequestContext ctx, HttpRequest req)
                              throws Exception {
                          return HttpResponse.of(HttpStatus.OK, MediaType.PLAIN_TEXT_UTF_8,
                                                 "bar.com /virtual-foo/[a1|a2]/my-service2");
                      }
                  })
                  .annotatedService(new Object() {
                      @Get("/svc1")
                      public HttpResponse hello1() {
                          return HttpResponse.of(HttpStatus.OK, MediaType.PLAIN_TEXT_UTF_8,
                                                 "bar.com /virtual-foo/[a1|a2]/svc1");
                      }

                      @Get("/svc2")
                      public HttpResponse hello2() {
                          return HttpResponse.of(HttpStatus.OK, MediaType.PLAIN_TEXT_UTF_8,
                                                 "bar.com /virtual-foo/[a1|a2]/svc2");
                      }}
                  )
                  .contextPaths(Set.of("/b1", "/b2"), ctx2 -> ctx2
                          .service("/my-service", new HttpService() {
                              @Override
                              public HttpResponse serve(ServiceRequestContext ctx, HttpRequest req)
                                      throws Exception {
                                  return HttpResponse.of(HttpStatus.OK, MediaType.PLAIN_TEXT_UTF_8,
                                                         "bar.com /virtual-foo/[a1|a2]/[b1|b2]/my-service");
                              }
                          }))
          );

        return sb.build();
    }



    public static void main(String[] args) {
        Server server = newServer(8080);
        server.closeOnJvmShutdown();
        server.start().join();

    }
}
