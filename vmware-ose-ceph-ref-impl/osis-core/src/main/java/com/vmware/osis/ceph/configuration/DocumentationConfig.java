/**
 *Copyright 2020 program was created by VMware.
 *SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.ceph.configuration;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import org.springframework.hateoas.client.LinkDiscoverer;
import org.springframework.hateoas.client.LinkDiscoverers;
import org.springframework.hateoas.mediatype.collectionjson.CollectionJsonLinkDiscoverer;
import org.springframework.plugin.core.SimplePluginRegistry;
import springfox.documentation.builders.ApiInfoBuilder;
import springfox.documentation.builders.PathSelectors;
import springfox.documentation.builders.RequestHandlerSelectors;
import springfox.documentation.service.ApiInfo;
import springfox.documentation.spi.DocumentationType;
import springfox.documentation.spring.web.plugins.Docket;
import springfox.documentation.swagger2.annotations.EnableSwagger2;

import java.util.ArrayList;
import java.util.List;

@Configuration
@EnableSwagger2
public class DocumentationConfig {
    private static final String DOC_TITLE = "Object Storage Interoperability Services API";
    private static final String DOC_DESCRIRTION = "This is VMware Cloud Director Object Storage Interoperability Services API." +
            " Once storage platform vendor implements REST APIs complying with this specification, " +
            "Object Storage Extension can integrate with the platform without coding effort." ;
    private static final String DOC_VERSION = "1.0.0";
    private static final String PROJECT_BASE = "com.vmware.osis.ceph.api";

    ApiInfo apiInfo() {
        return new ApiInfoBuilder()
            .title(DOC_TITLE)
            .description(DOC_DESCRIRTION)
            .version(DOC_VERSION)
            .build();
    }

    @Bean
    public LinkDiscoverers discoverers() {
        List<LinkDiscoverer> plugins = new ArrayList<>();
        plugins.add(new CollectionJsonLinkDiscoverer());
        return new LinkDiscoverers(SimplePluginRegistry.create(plugins));

    }

    @Bean
    public Docket customImplementation(){
        return new Docket(DocumentationType.SWAGGER_2)
                .apiInfo(apiInfo())
                .enable(true)
                .select()
                .apis(RequestHandlerSelectors.basePackage(PROJECT_BASE))
                .paths(PathSelectors.any())
                .build();
    }
}
