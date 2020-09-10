/**
 * Copyright 2020 VMware, Inc.
 * SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.security.config;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.vmware.osis.platform.AppEnv;
import com.vmware.osis.platform.security.PlatformUserDetailsService;
import com.vmware.osis.security.jwt.JwtAuthenticationProvider;
import com.vmware.osis.security.jwt.extractor.JwtHeaderTokenExtractor;
import com.vmware.osis.security.jwt.login.LoginAuthenticationFailureHandler;
import com.vmware.osis.security.jwt.login.LoginAuthenticationProvider;
import com.vmware.osis.security.jwt.login.LoginAuthenticationSuccessHandler;
import com.vmware.osis.security.jwt.JwtTokenFactory;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

@Configuration
@ConditionalOnProperty(value = "security.jwt.enabled",
        havingValue = "true",
        matchIfMissing = true)
public class OsisJwtBeans {

    @Bean
    protected BCryptPasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    protected LoginAuthenticationProvider loginAuthenticationProvider(PlatformUserDetailsService userService, BCryptPasswordEncoder encoder) {
        return new LoginAuthenticationProvider(userService, encoder);
    }

    @Bean
    protected JwtAuthenticationProvider jwtAuthenticationProvider(AppEnv appEnv) {
        return new JwtAuthenticationProvider(appEnv);
    }

    @Bean
    protected JwtHeaderTokenExtractor jwtHeaderTokenExtractor() {
        return new JwtHeaderTokenExtractor();
    }

    @Bean
    protected JwtTokenFactory jwtTokenFactory(AppEnv appEnv) {
        return new JwtTokenFactory(appEnv);
    }

    @Bean
    protected LoginAuthenticationFailureHandler loginAuthenticationFailureHandler(ObjectMapper objectMapper) {
        return new LoginAuthenticationFailureHandler(objectMapper);
    }

    @Bean
    protected LoginAuthenticationSuccessHandler loginAuthenticationSuccessHandler(ObjectMapper objectMapper, JwtTokenFactory jwtTokenFactory) {
        return new LoginAuthenticationSuccessHandler(objectMapper, jwtTokenFactory);
    }
}
