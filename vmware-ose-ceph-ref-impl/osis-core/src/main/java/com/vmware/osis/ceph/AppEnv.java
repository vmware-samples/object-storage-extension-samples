/**
 *Copyright 2020 program was created by VMware.
 *SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.ceph;

import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Component;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

import static com.vmware.osis.ceph.utils.CephConstants.COMMA;

@Component
public class AppEnv {

    @Autowired
    private Environment env;

    public String getRgwEndpoint() {
        return  env.getProperty("osis.ceph.rgw.endpoint");
    }

    public String getRgwAccessKey() {
        return env.getProperty("osis.ceph.rgw.access-key");
    }

    public String getRgwSecretKey() {
        return env.getProperty("osis.ceph.rgw.secret-key");
    }

    public String getS3Endpoint() {
        return env.getProperty("osis.ceph.s3.endpoint");
    }

    public String getConsoleEndpoint() {
        return env.getProperty("osis.ceph.console.endpoint");
    }

    public List<String> getStorageInfo() {
        String storageInfo = env.getProperty("osis.ceph.storage-classes");
        if(StringUtils.isBlank(storageInfo)) {
            return Collections.singletonList("standard");
        }
        return Arrays.stream(StringUtils.split(storageInfo, COMMA)).
                map(String::trim).collect(Collectors.toList());
    }

    public List<String> getRegionInfo() {
        String regionInfo =  env.getProperty("osis.ceph.region");
        if(StringUtils.isBlank(regionInfo)) {
            return Collections.singletonList("default");
        }
        return Arrays.stream(StringUtils.split(regionInfo, COMMA))
                .map(String::trim).collect(Collectors.toList());
    }

    public String getPlatformName() {
        return env.getProperty("osis.ceph.name");
    }

    public String getPlatformVersion() {
        return env.getProperty("osis.ceph.version");
    }

    public String getApiVersion() {
        return env.getProperty("osis.api.version");
    }

    public boolean isApiTokenEnabled() {
        return Boolean.parseBoolean(env.getProperty("security.jwt.enabled"));
    }

    public String getTokenIssuer() {
        return env.getProperty("security.jwt.token-issuer");
    }

    public int getAccessTokenExpirationTime() {
        return Integer.parseInt(env.getProperty("security.jwt.access-token-expiration-time"));
    }

    public String getTokenSigningKey() {
        return env.getProperty("security.jwt.token-signing-key");
    }

    public int getRefreshTokenExpirationTime() {
        return Integer.parseInt(env.getProperty("security.jwt.refresh_token_expiration_time"));
    }
}
