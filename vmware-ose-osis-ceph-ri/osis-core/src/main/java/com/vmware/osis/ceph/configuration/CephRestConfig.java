/**
 *Copyright 2020 VMware, Inc.
 *SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.ceph.configuration;


import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.ClientHttpRequestFactory;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.twonote.rgwadmin4j.RgwAdmin;
import org.twonote.rgwadmin4j.RgwAdminBuilder;

@Configuration
public class CephRestConfig {

    @Value("${osis.ceph.rgw.access-key}")
    private String rgwAccessKey;

    @Value("${osis.ceph.rgw.secret-key}")
    private String rgwSecretKey;

    @Value("${osis.ceph.rgw.endpoint}")
    private String rgwEndpoint;

    @Bean
    public ClientHttpRequestFactory simpleClientHttpRequestFactory() {
        SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
        factory.setReadTimeout(10000);
        factory.setConnectTimeout(10000);
        return factory;
    }

    @Bean
    public RgwAdmin getRgwAdmin() {
        return new RgwAdminBuilder()
                .accessKey(rgwAccessKey)
                .secretKey(rgwSecretKey)
                .endpoint(rgwEndpoint)
                .build();
    }
}
